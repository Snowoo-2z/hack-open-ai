# [Target] Short, impact-first title (e.g. "User B can read user A's private X via Y")

## Summary
One paragraph: who (less-privileged attacker), which enforced restriction is bypassed,
which protected resource/action is reached, concrete unauthorized outcome.

## Affected product
- Product / target: (ChatGPT web / api.openai.com / Codex Desktop …)
- URL / endpoint: (no session tokens)
- Version, OS, browser: …
- Test accounts: A = owner/victim (…@bugcrowdninja.com), B = attacker (both mine)
- Conversation ID (if ChatGPT): https://chatgpt.com/c/…

## Steps to reproduce
1. As A, …
2. As B (separate browser profile, no shared session), …
3. Observe …

## Expected vs actual
- Expected (restriction enforced): …
- Actual (bypass observed): …

## Impact
What an attacker gains at scale / against real users, stated conservatively and factually.
Data classes exposed, actions possible, preconditions, user interaction required.

## Evidence
- Screenshots (redacted): …
- Sanitized request/response excerpts (method, path, status, JSON fields): …
- Timestamps (UTC): …

## Scope & safety note
Testing performed only on my own two accounts and my own test objects, in scope per the
program brief. Testing stopped as soon as the issue was demonstrated. No third-party data
was accessed (if any exposure occurred: state the strict minimum observed and that copies
were deleted).

## Suggested remediation (optional, brief)
Server-side authorization check on … / re-validate … on state transition …
