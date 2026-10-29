# Building Peerboop inside Grok

Design notes for **Peerboop P2P**, reviewed **29 October 2026**. These are choices for the current skill-only product, with first-party host references for future maintenance.

## Give it a useful first turn

Offer the four desk jobs with native choices, or answer the stated request immediately. A new person should get a price or a useful next question before any setup report. [Grok Bot use cases](https://docs.x.ai/grok-bot/use-cases) is the host reference.

## Put repeatable behavior in the skill

Keep the public-data procedures, fee arithmetic, voice and handoffs in one complete Markdown skill. Save it as the dedicated bot’s active skill. A file merely existing in a repository is not evidence that Grok is using it. Inspect the native configuration and test the rendered answer. See [Bots](https://docs.x.ai/grok-bot/bots) and [Skills, routines and automations](https://docs.x.ai/grok-bot/skills-routines-and-automations).

## Let native chat do the work

Use readable Markdown, supported native question cards and concise action links. Keep the pocket-broker voice friendly and brief. Lead with amounts and net output, ask one missing detail at a time, and leave internal tool progress out of the reply. Make fees clear before adding any cheek. No custom card renderer or intermediary website is needed. [Chat and collaboration](https://docs.x.ai/grok-bot/chat-and-collaboration) describes the host’s conversation surfaces.

## Prove a read before scheduling it

A watch starts with an exact condition and a baseline public read. Save a native Routine only after the person defines the schedule and stop condition. Inspect the actual host’s notification options; do not infer silent conditional delivery from a prompt alone. [Skills, routines and automations](https://docs.x.ai/grok-bot/skills-routines-and-automations) is the scheduling reference.

## Share the role, keep the person private

Inspect the actual shared template’s context, skill list and integrations. Include only the generic description and skill; exclude personal memories, routine instances and account/order history. A fresh copy should check prices without credentials. See [Grok Bot FAQ](https://docs.x.ai/grok-bot/faq) and [Approvals, security and privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy).

## Test the bot people actually install

Start from the public template, then try normal questions, missing details, a follow-up, an unavailable route and an existing-order problem. Compare quoted amounts with live public data and inspect actual link destinations. Keep failures in the record and replay them after fixes. Screenshots of an authored response are not evidence of an installed skill.

[Verification notes](BUILD.md) record native observations and unresolved acceptance. [The source guide](PEER_GUIDE.md) documents the selected Peer and USDCtoFiat references.

## Design references

Public marketplace examples reviewed during the project included [Haggle Bot](https://x.ai/bot/marketplace/bots/haggle-bot), [Tradbot](https://x.ai/bot/marketplace/bots/tradbot-2) and [tinkabot](https://x.ai/bot/marketplace/bots/tinkabot). The useful patterns were a clear job, one question at a time and testing behavior inside the actual host. Their integrations and execution permissions are not dependencies or authority for this desk.
