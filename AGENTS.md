# Peerboop P2P

Peerboop P2P is an independent, informational Grok bot from Galleon Labs. The product is one Markdown skill, `skills/peerboop-p2p/SKILL.md`, plus the generic startup note quoted in its Native activation section. The bot name has no publisher suffix and must not imply official Peer support.

- Releases: bump `metadata.version`, run `python3 scripts/release-manifest.py`, merge to `main`. Installed bots update themselves from `manifest.json`; never republish the Grok template for a skill change.
- Keep it skill-only: no backend, package, wallet, signer, order creation, custom connector or scheduler. Watches use Grok's native Routines only when a person asks.
- Market data comes from Peer's public orderbook feed and the indexer-backed Peerlytics explorer API. Never hard-code a live price, fee or payment-app list.
- Keep `referralCode=TOFIAT` on every Peer link and use Peer only on `/referrals` and the mobile onboarding link. The USDCtoFiat sell link may be prefilled with `platform`, `currency` and `amount`.
- Voice: one finished reply per turn, answer first, usually 20–40 words, then the links.
- Before a change run `python3 scripts/check-skill.py`, `python3 -m unittest discover -s tests` and `python3 scripts/release-manifest.py --check`; test the rendered answer in a disposable Grok bot and reconcile figures against the live source.
- Public templates carry only the description, the startup note and the skill. Never publish personal memories, watch instances, order history or credentials.
