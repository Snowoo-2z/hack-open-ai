#!/usr/bin/env python3
"""Pilote semi-automatique pour nos tests Bugcrowd OpenAI autorises.

Principe : ce script se connecte, EN LOCAL (127.0.0.1), a un Chrome que tu as
lance toi-meme avec --remote-debugging-port, dans lequel tu t'es connecte
manuellement a ton compte de test. Il execute ensuite une "mission" (fichier
JSON relu avant execution) composee uniquement d'actions en liste blanche :
naviguer vers une URL en-scope, attendre, decrire la page, capture d'ecran,
extraire le texte visible (sanitise), verifier la presence/absence d'un mot,
cliquer un texte visible (toujours avec ta confirmation), pause manuelle.

Garde-fous inscrits dans le code :
- domaines limites a openai.com / openai.org / chatgpt.com (et sous-domaines) ;
- aucun mot de passe, aucune saisie de formulaire, aucun JavaScript arbitraire ;
- chaque action demande ta validation (touche Entree), sauf flag --yes qui ne
  couvre jamais les clics ;
- journal reseau reduit a methode + origine + chemin + code HTTP (les
  parametres d'URL, donc les jetons eventuels, sont entierement retires) ;
- textes extraits sanitises (emails, cles sk-/sess-, Bearer, JWT masques).
  Les captures d'ecran, elles, ne sont PAS modifiees : relis-les avant envoi.

Usage :
  python3 pilot.py missions/exemple-verif-connexion.json
  python3 pilot.py missions/t01-partie-B.json --validate-only   (sans navigateur)
Prerequis : pip install playwright  (aucun autre navigateur a telecharger :
le script pilote TON Chrome via le port de debug local).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOST_SUFFIXES = ("openai.com", "openai.org", "chatgpt.com")
ALLOWED_ACTIONS = {
    "goto", "wait", "page_info", "screenshot", "extract_text",
    "check_text", "click_text", "wait_for_user",
}
MAX_STEPS = 50
MAX_WAIT_SECONDS = 30.0
MIN_DELAY_AFTER_GOTO = 1.0

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SECRET_RES = [
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{8,}"),
    re.compile(r"sess-[A-Za-z0-9_-]{8,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{4,}"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._-]{8,}"),
]


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[EMAIL]", text)
    for pat in SECRET_RES:
        text = pat.sub(lambda m: (m.group(1) + "REDACTED") if m.groups() else "REDACTED", text)
    return text


def host_allowed(url: str) -> bool:
    if url == "about:blank":
        return True
    host = (urlparse(url).hostname or "").lower()
    return any(host == s or host.endswith("." + s) for s in ALLOWED_HOST_SUFFIXES)


def safe_network_url(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}{p.path}" if p.scheme and p.netloc else "(url masquee)"


def validate_mission(mission: dict) -> tuple[list[str], list[str]]:
    """Retourne (erreurs, avertissements). Aucune connexion navigateur ici."""
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(mission, dict):
        return ["La mission doit etre un objet JSON."], warnings
    if not mission.get("nom"):
        errors.append("Champ 'nom' manquant.")
    port = mission.get("port", 9222)
    if port not in (9222, 9223):
        errors.append(f"Port {port} refuse : seuls 9222 (compte A) et 9223 (compte B) sont autorises.")
    steps = mission.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append("Champ 'steps' manquant ou vide.")
        return errors, warnings
    if len(steps) > MAX_STEPS:
        errors.append(f"Trop d'etapes ({len(steps)} > {MAX_STEPS}).")
    for i, step in enumerate(steps, 1):
        if not isinstance(step, dict):
            errors.append(f"Etape {i} : format invalide.")
            continue
        action = step.get("action")
        if action not in ALLOWED_ACTIONS:
            errors.append(f"Etape {i} : action '{action}' hors liste blanche.")
            continue
        if action == "goto":
            url = str(step.get("url", ""))
            if "__" in url:
                warnings.append(f"Etape {i} : URL a personnaliser avant execution ({url}).")
            elif not host_allowed(url):
                errors.append(f"Etape {i} : domaine hors perimetre autorise ({url}).")
        if action == "wait":
            secs = float(step.get("secondes", 1))
            if secs < 0 or secs > MAX_WAIT_SECONDS:
                errors.append(f"Etape {i} : attente {secs}s hors bornes (0-{MAX_WAIT_SECONDS}s).")
        if action == "check_text" and not step.get("texte"):
            errors.append(f"Etape {i} : check_text sans champ 'texte'.")
        if action == "click_text" and not step.get("texte"):
            errors.append(f"Etape {i} : click_text sans champ 'texte'.")
    return errors, warnings


class Report:
    def __init__(self, outdir: Path, mission_name: str):
        self.outdir = outdir
        self.path = outdir / "resultat.md"
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._w(f"# Resultat de mission : {mission_name}\n\nDebut (UTC) : {stamp}\n")

    def _w(self, text: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(text + "\n")

    def log(self, text: str) -> None:
        text = redact(text)
        print(text)
        self._w(text)


def confirm(prompt: str, auto: bool, always: bool = False) -> bool:
    if auto and not always:
        return True
    try:
        answer = input(f">>> {prompt}  [Entree = executer, q = arreter] ").strip().lower()
    except EOFError:
        return False
    return answer != "q"


def slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", text).strip("-")[:60] or "mission"


def run(mission: dict, auto: bool, out_base: Path) -> int:
    from playwright.sync_api import sync_playwright  # import tardif : --validate-only n'en a pas besoin

    port = mission.get("port", 9222)
    outdir = out_base / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{slug(mission['nom'])}"
    outdir.mkdir(parents=True, exist_ok=True)
    report = Report(outdir, mission["nom"])
    network: list[str] = []

    endpoint = f"http://127.0.0.1:{port}"
    report.log(f"Connexion a TON Chrome local via {endpoint} (compte {'A' if port == 9222 else 'B'})...")
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.connect_over_cdp(endpoint, timeout=15000)
    except Exception as exc:  # connexion impossible : on explique et on sort
        report.log(f"ERREUR de connexion : {exc}")
        report.log("Verifie : 1) Chrome lance avec la commande du README (bon port), "
                   "2) aucun autre Chrome avec le meme profil, 3) tu es connecte a ton compte de test.")
        return 2

    try:
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.pages[-1] if context.pages else context.new_page()

        def on_response(resp):  # journal reseau minimal, sans query-string
            if len(network) < 500:
                network.append(f"{resp.request.method} {resp.status} {safe_network_url(resp.url)}")

        page.on("response", on_response)

        for i, step in enumerate(mission["steps"], 1):
            action = step["action"]
            desc = f"[{i}/{len(mission['steps'])}] {action} {step.get('note', '')}".strip()
            if not confirm(desc, auto, always=(action == "click_text")):
                report.log(f"- {desc} -> ARRETE par l'utilisateur.")
                break
            try:
                if action == "goto":
                    url = step["url"]
                    if "__" in url:
                        report.log(f"- {desc} -> URL non personnalisee, etape ignoree. Edite la mission chez toi.")
                        continue
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    time.sleep(MIN_DELAY_AFTER_GOTO)
                    report.log(f"- {desc} -> page atteinte : {page.url} | titre : {page.title()}")
                elif action == "wait":
                    secs = float(step.get("secondes", 1))
                    time.sleep(secs)
                    report.log(f"- {desc} -> attente {secs}s.")
                elif action == "page_info":
                    report.log(f"- {desc} -> URL : {page.url} | titre : {page.title()}")
                elif action == "screenshot":
                    name = slug(str(step.get("fichier", f"capture-{i}"))) + ".png"
                    page.screenshot(path=str(outdir / name))
                    report.log(f"- {desc} -> capture : {name} (A RELIRE avant envoi : emails/avatars visibles possibles)")
                elif action == "extract_text":
                    text = page.inner_text("body", timeout=10000)
                    clean = redact(text)[:6000]
                    name = slug(str(step.get("fichier", f"texte-{i}"))) + ".txt"
                    (outdir / name).write_text(clean, encoding="utf-8")
                    report.log(f"- {desc} -> texte visible sanitise ({len(clean)} car.) : {name}")
                elif action == "check_text":
                    needle = str(step["texte"])
                    text = page.inner_text("body", timeout=10000)
                    found = needle in text
                    report.log(f"- {desc} -> texte « {needle} » : {'TROUVE' if found else 'ABSENT'} sur la page.")
                elif action == "click_text":
                    label = str(step["texte"])
                    page.get_by_text(label, exact=bool(step.get("exact", False))).first.click(timeout=8000)
                    time.sleep(1.0)
                    report.log(f"- {desc} -> clique sur « {label} ». URL : {page.url}")
                elif action == "wait_for_user":
                    msg = str(step.get("message", "Fais l'action manuelle demandee, puis Entree."))
                    input(f">>> PAUSE MANUELLE : {msg} [Entree quand c'est fait] ")
                    report.log(f"- {desc} -> action manuelle confirmee par l'utilisateur.")
            except Exception as exc:
                report.log(f"- {desc} -> ECHEC : {exc} (on continue la mission)")

        if network:
            (outdir / "reseau.txt").write_text("\n".join(redact("\n".join(network))), encoding="utf-8")
            report.log(f"Journal reseau minimal : reseau.txt ({len(network)} reponses, sans parametres d'URL).")
        report.log("\nMission terminee. A me renvoyer : resultat.md (+ .txt), et les captures APRES relecture.")
    finally:
        try:
            browser.close()  # detache la session CDP, ne ferme pas ton Chrome
        except Exception:
            pass
        pw.stop()
    print(f"\nDossier resultats : {outdir}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Pilote semi-automatique (tests autorises, compte personnel de test).")
    ap.add_argument("mission", help="Fichier JSON de mission")
    ap.add_argument("--yes", action="store_true",
                    help="Ne pas confirmer les etapes en lecture seule (les clics restent confirmes)")
    ap.add_argument("--validate-only", action="store_true",
                    help="Valider le fichier mission sans navigateur")
    ap.add_argument("--out", default=str(Path(__file__).parent / "resultats"),
                    help="Dossier de sortie des resultats")
    args = ap.parse_args()

    mission_path = Path(args.mission)
    try:
        mission = json.loads(mission_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Impossible de lire la mission {mission_path} : {exc}")
        return 1
    errors, warnings = validate_mission(mission)
    for w in warnings:
        print(f"AVERTISSEMENT : {w}")
    if errors:
        for e in errors:
            print(f"ERREUR : {e}")
        return 1
    print(f"Mission valide : {mission['nom']} ({len(mission['steps'])} etapes, port {mission.get('port', 9222)})")
    if args.validate_only:
        return 0
    return run(mission, auto=args.yes, out_base=Path(args.out))


if __name__ == "__main__":
    raise SystemExit(main())
