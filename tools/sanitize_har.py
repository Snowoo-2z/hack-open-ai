#!/usr/bin/env python3
"""Nettoie un export HAR avant partage (chat, rapport, etc.).

Supprime/masque : cookies, en-tetes Authorization et assimilés, et les motifs
évidents de secrets (cles sk-..., jetons sess-..., JWT) dans tout le document.
Stdlib uniquement. Relire quand meme le fichier produit avant tout envoi :
cet outil est un filet de securite, pas une garantie.

Usage : python3 sanitize_har.py entree.har sortie.har
"""
import json
import re
import sys

SENSITIVE_HEADERS = {
    "authorization", "cookie", "set-cookie", "x-api-key", "api-key",
    "openai-api-key", "x-auth-token", "proxy-authorization",
}
SECRET_PATTERNS = [
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{16,}"),
    re.compile(r"sess-[A-Za-z0-9_-]{16,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}"),  # JWT
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._-]{10,}"),
]


def scrub(value):
    if isinstance(value, str):
        for pat in SECRET_PATTERNS:
            value = pat.sub(lambda m: (m.group(1) + "REDACTED") if m.groups() else "REDACTED", value)
        return value
    if isinstance(value, list):
        return [scrub(v) for v in value]
    if isinstance(value, dict):
        return {k: scrub(v) for k, v in value.items()}
    return value


def clean_headers(items):
    for h in items or []:
        if str(h.get("name", "")).lower() in SENSITIVE_HEADERS:
            h["value"] = "REDACTED"
    return items


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    with open(sys.argv[1], encoding="utf-8") as f:
        har = json.load(f)
    for entry in har.get("log", {}).get("entries", []):
        for side in ("request", "response"):
            part = entry.get(side, {})
            part["headers"] = clean_headers(part.get("headers"))
            part["cookies"] = []
            if side == "request":
                for q in part.get("queryString", []) or []:
                    if any(s in str(q.get("name", "")).lower() for s in ("token", "key", "auth", "sig")):
                        q["value"] = "REDACTED"
    har = scrub(har)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(har, f, ensure_ascii=False, indent=1)
    print(f"OK -> {sys.argv[2]} (relis-le avant envoi : recherche 'sk-', 'Bearer', ton email)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
