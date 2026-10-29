# Peerboop P2P verification

## Current product

**Peerboop P2P** is one Markdown skill, [SKILL.md](../skills/peerboop-p2p/SKILL.md), currently **1.7.4**, plus one generic startup note. Grok supplies the chat, public reads and optional Routines. There is no backend, wallet, signer or trading runtime.

The public template is [x.ai/bot/OVV5tPy7c0yg5WyMfv6pj](https://x.ai/bot/OVV5tPy7c0yg5WyMfv6pj). Before publication, its Context showed the listing description, one startup note under Memories and the single `peerboop-p2p` skill. There were no other memories, routines or integrations. The page serves the name **Peerboop P2P** and the new description. It was shared from the Peerboop P2P bot in Andrew’s Grok account, the only bot that can publish a later revision to the same link.

Earlier links still serve older revisions: [TTGN1ZyR36y7IHPyVoxqw](https://x.ai/bot/TTGN1ZyR36y7IHPyVoxqw) (1.4.7) and [L_8sIrjGWakeIuv1ScdJF](https://x.ai/bot/L_8sIrjGWakeIuv1ScdJF) (1.6.1). A Grok template can be revised only from the bot that shared it, and both sharing bots were removed from the account. The new link replaces them everywhere. The 1.2.1 [W9 template](https://x.ai/bot/W9UsMGleqdY8oeBhmCrMi) is older still.

## Self-updating (1.7)

The Grok template is published once. Every installed bot fetches [`manifest.json`](../skills/peerboop-p2p/manifest.json) (version, SHA-256, raw skill URL) at the start of each turn. A release is a merge to `main` with a bumped version and a regenerated manifest.

Grok does not let a bot silently rewrite its own skill because a note says so. It treats the startup note as untrusted memory and asks the person first. So updates are opt-in once: a bot on an older version adds one line offering the new version. After the person replies **always update**, the bot saves that in its private memory and later versions install silently. It checks the hash and diffs before swapping.

Verified on 29 October 2026:

- **Opt-in:** a bot installed from the template refused to self-update until told in chat; it then installed 1.7.1 (hash checked, diffed) at 16:44 UTC.
- **Silent update:** 1.7.2 was released by merge only. On the next ordinary question the opted-in bot installed it at 16:52 UTC, answered the question normally (€192.64 for 200 USDC, which reconciles), and said nothing about the update.
- **Propagation:** GitHub serves raw files from a cache of up to about five minutes, so a release reaches bots within minutes. One bot fetched 1.7.1 for a few minutes after 1.7.2 was pushed.
- **Shared library:** skills live in one library per Grok account, so every Peerboop copy in an account shares one skill file. The one-line offer could therefore not be observed in the author’s own account; it applies to other people’s installs.
- **Template versions 2–4** were published from the same author bot, so the link never changed. Version 4 keeps the startup note minimal: identity, the welcome rule, the update rule and the safety limits. Everything else ships in the skill.

The startup note holds the limits an update can never change: no trading, signing, funds, wallet connections, credentials or payout details, and `referralCode=TOFIAT` on Peer links. Anyone who can push to `main` controls the skill every opted-in bot runs, so only the owner should have write access.

Open: a brand-new install opens with Grok’s own one-line greeting before the skill loads (no name or account context since version 4), then the correct four-choice card.

## What changed in 1.6

- **Market data from the indexer.** Prices, fees, limits, eligibility, live payment apps and the market reference all come from Peer’s public orderbook feed, which is built on the Peer indexer. Market value is each offer’s price divided by its stated premium over Peer’s onchain oracle. Deposits come from the indexer through the Peerlytics explorer API. The USDCtoFiat calculator, route board and payment-methods page are no longer read, and the bot opens no website to answer.
- **Stake-backed offers count.** Peer’s takeability rule, as used by Peerlytics, treats offers that require a buyer stake as open to every buyer. Venmo and PayPal offers all require one, so the old filter hid the largest US route. They are now priced and labelled “Needs a buyer stake in Peer.” Rate-managed offers are included as ordinary offers. Whitelisted offers without a stake and seller-automated offers are excluded. At equal price, an offer without a stake ranks first.
- **Platform-agnostic voice.** Replies talk about the Peer market. Product names appear only in links: buy on Peer web or mobile; sell on USDCtoFiat or Peer.
- **Deep links.** The USDCtoFiat sell link is prefilled: `/sell?platform=…&currency=…&amount=…`. Peer links stay on `/referrals?referralCode=TOFIAT` and the mobile onboarding link, because Peer records the referral only there; a `/buy/…` deep link would drop TOFIAT.
- **Sell answers** show market value plus the live competition on the route (lowest seller price and its premium, seller count, USDC listed) instead of 30-day history.
- **One reply per turn.** The skill and the startup note forbid the holding messages Grok tends to send before slow lookups.
- **1.6.2** prices sell competition and market value with `takerConversionRate` (what buyers pay, including any rate-manager fee) and computes the premium when a row has no `spread`. An independent review found both.
- **New welcome:** “Hey, I’m Peerboop 👋 Live USDC prices, fees and payment apps, right here.” with **Buy USDC**, **Sell USDC**, **Cheapest route today** and **Track a deposit**. Watches remain available on request but are not advertised.

The HTML catalog parser and its tests were removed with the USDCtoFiat page read.

## Live acceptance

The [QA record](QA_2026-10-29.md) has every turn. Fresh installs of the published 1.6.1 and 1.6.2 templates passed the welcome, cheapest buy, sell, Venmo, plain deposit ID, payment apps and payment-help journeys. Every figure matched an independent calculation from the same public sources taken within seconds of the reply.

**Holding messages remain the open voice gap.** A short line such as “Pulling the live USD offers now.” preceded 3 of 9 customer turns in the 1.6.1 install and 4 of 4 lookups in the final 1.6.2 install. Moving the rule to the top of the startup note (tested as 1.6.3) did not change it. This is Grok’s own behaviour before tool use; the skill cannot reliably switch it off.

## Checks

```sh
python3 scripts/check-skill.py
python3 -m unittest discover -s tests
validate-agent-skills skills/peerboop-p2p
```

The 19 offline tests load the Python recipes straight from SKILL.md. They cover fee-boundary arithmetic (with 29,997 property cases), the takeability rule, stake tie-breaks, the market reference (taker rate, null spreads) and the sell snapshot. They do not prove that the model follows the skill; the live QA does that.

## Media

[Four still images](launch/MEDIA.md) replace the earlier videos. Each is real chat from the published bot, cropped without edits. The [launch post](launch/LAUNCH.md) is drafted and unpublished.
