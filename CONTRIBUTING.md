# Contributing

Peerboop P2P is a native Grok skill. Changes should make the conversation more useful without adding a runtime or infrastructure.

## Start here

Read [the skill](skills/peerboop-p2p/SKILL.md), [product decisions](docs/DECISION.md) and [source guide](docs/PEER_GUIDE.md). Keep the name **Peerboop P2P**. Galleon Labs belongs in creator credits, not the bot name.

The active product lives in `skills/peerboop-p2p/`.

## Keep the pocket-broker voice

Be bright, friendly and a little cheeky. Keep numbers and fees plain; a useful answer beats a pun. Lead with the answer or amount. Aim for 20–40 words and one next action. Ask for one missing detail at a time and reuse what the person already told you. Native choice cards and an occasional useful currency flag are welcome.

Explain net output and material fees when they affect the answer. Verified current snapshots need no Estimated or Indicative label. Call a reference conversion **Market value** rather than a bank payout. Leave tool chatter, package instructions, boilerplate warnings and progress narration out of the conversation.

## Check the change

Run the dependency-free repository check:

```sh
python3 scripts/check-skill.py
python3 -m unittest discover -s tests
```

If available, run the Agent Skills validator too:

```sh
validate-agent-skills skills/peerboop-p2p
```

Use a separate disposable bot for live tests. Check the rendered answer, supporting public data and destination link. Never use a customer’s bank information, credentials or payment evidence in a test.

A useful small test set:

1. Start without a request: the one-line welcome and four desk choices appear, with no other message.
2. Ask for a sell price, then change only the amount: the payment app and currency carry over.
3. Ask for a buy amount including fees: one reply only, and the fiat total and net USDC agree with the live source.
4. Ask to buy through Venmo: the reply explains the buyer stake and quotes the cheapest open route.
5. Supply a public deposit link: available and reserved amounts remain separate.
6. Ask for a watch with missing conditions: the bot asks for the missing detail before saving anything.
7. Say a payment failed after paying: guidance continues the existing order and points to official support.

If a price cannot be verified, the reply should say so briefly and offer the correct trading link. Keep that failed case in the evidence rather than substituting an earlier price.

## Release a change

Bump `metadata.version` in SKILL.md, run `python3 scripts/release-manifest.py`, and commit both files. Once that is merged to `main`, installed bots see it within about five minutes (GitHub caches raw files). Bots whose owner chose **always update** install it silently on their next turn; others offer it once in a single line. Never republish the Grok template for a skill change. Change the startup note only when the update rule or safety limits themselves must change; that needs a template republish.

## Open a pull request

Describe the user’s request, what changes in the answer, and how you tested it. Include concise examples or screenshots with no personal context. Say which live behavior you did not verify.

Preserve the attributed handoffs in the skill. Do not add a wallet, signer, execution flow, custom scheduler, private connector or backend. Do not share private memories, routine instances, account history or recovery material through a template.

For a sensitive issue, follow [SECURITY.md](SECURITY.md). Contributions are covered by the [MIT license](LICENSE).
