# Public sources and Peer guide

Reviewed 29 October 2026 against the first-party pages below. This is a source register for the informational bot, not a price cache. Peerboop P2P answers questions, checks current prices and links to the trading sites.

## Destinations and product boundary

| Person's intent        | Links                                                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Buy USDC               | [Buy on Peer](https://app.peer.xyz/referrals?referralCode=TOFIAT) · [Peer mobile](https://mobile.peer.xyz/onboard?referralCode=TOFIAT) |
| Sell USDC              | [Sell on USDCtoFiat](https://usdctofiat.xyz) (deep link `/sell?platform=&currency=&amount=`) · [Sell on Peer](https://app.peer.xyz/referrals?referralCode=TOFIAT) |
| Existing-order problem | [Peer Support](https://support.peer.xyz)                                                                                  |

## Market data

| Data | Public source |
| --- | --- |
| Offers: price, fee, limits, eligibility, premium over the onchain oracle | `https://api.zkp2p.xyz/v3/orderbook/table`, Peer's orderbook feed built on the indexer |
| Deposits, wallets and intents | `https://peerlytics.xyz/api/explorer/deposit/{id}` and `/address/{address}`, indexer-backed |
| Aggregate liquidity by route | `https://peerlytics.xyz/explorer/liquidity.json` |
| Raw protocol state | `https://indexer.zkp2p.xyz/v1/graphql` (anonymous; used for verification, not by the bot) |

Takeability follows the rule Peerlytics publishes in `liquidity.json` (`method.takeability`): an offer is public when it needs a buyer stake or has no whitelist. Peer records the TOFIAT referral only on `/referrals` and the mobile onboarding link, so Peer `/buy/…` and `/sell/…` deep links are not used. USDCtoFiat's `/sell` page reads `platform`, `currency` and `amount` and falls back to USD for a currency the app does not offer.

Use the exact URLs. Use the verified TOFIAT web/mobile routes documented below. Do not invent other referral parameters or promise that every wallet connection earns commission. The bot does not create an order, reserve liquidity, hold funds, verify a payment, inspect private order status or process a refund. It never needs a wallet key or payout details.

## Curated answers

Each sample is intentionally short. The trade link is the primary action; a source citation supports the explanation rather than offering another task.

### Overview

**What is Peer?** A marketplace connecting people who buy and sell crypto using payment apps. Crypto is held in protocol escrow while the payment is verified. This bot helps you understand the options and check current prices; trades happen on the linked site.

Source: [Peer overview](https://peer.xyz). Avoid extending a general non-custodial claim into a guarantee that contracts, counterparties or payment platforms have no risk.

### Buying

**Buy crypto with your payment app.** Choose the amount and route on Peer, review the current quote, pay the seller exactly as instructed, then follow verification and completion prompts. Wait for confirmed delivery; finishing verification alone does not prove crypto arrived. [Buy on Peer](https://app.peer.xyz/referrals?referralCode=TOFIAT).

Source: [Buying Crypto with Peer](https://docs.peer.xyz/guides/for-buyers/complete-guide-to-onboarding). The current guide distinguishes external-wallet and social-sign-in paths and shows route-specific destinations. Do not promise that any particular person, payment account or destination qualifies without checking the live app.

### Selling

**Sell USDC into your payment account.** USDCtoFiat lets you choose a payout route and review the expected proceeds before you act. A buyer pays your account; payment verification precedes USDC release. Quotes and waiting times vary. [Sell on USDCtoFiat](https://usdctofiat.xyz).

Sources: [USDCtoFiat](https://usdctofiat.xyz), [Peer seller guide](https://docs.peer.xyz/guides/for-sellers/provide-liquidity-sell-usdc). The seller guide describes USDC escrow on Base. Do not claim that a source-chain funding address automatically creates a sell deposit or that this bot can prepare one.

### Fees

**No bot fee.** Trading costs depend on the route. Check the destination's current rate, expected output and fee rows before you proceed; network, service or routing costs may apply. A stored percentage is not the final price.

Source: [What are the fees on Peer?](https://support.peer.xyz/general/what-are-the-fees-on-peer). This article explicitly prioritizes the quote over fixed fee percentages. It also distinguishes interface fees from other possible route components. Do not copy a promotional fee maximum into a universal promise.

### Verification

**Payment verification depends on your route.** Follow Peer's prompts on the trading site or app. Some flows use PeerAuth to capture encrypted payment evidence; registration and verification requirements vary by payment method. This bot never asks for bank logins, codes or proofs.

Sources: [Why PeerAuth may be needed](https://support.peer.xyz/general/why-do-i-need-to-install-an-extension), [Peer buyer guide](https://docs.peer.xyz/guides/for-buyers/complete-guide-to-onboarding), [Peer seller guide](https://docs.peer.xyz/guides/for-sellers/provide-liquidity-sell-usdc). The seller guide currently describes extension-based identity verification for Wise and PayPal. Do not say every flow needs an extension, or that every flow avoids one. Refresh a platform-specific answer before giving instructions.

### Safety

**Use the official trading site and its order details.** Keep seed phrases, private keys, bank passwords and verification codes out of chat. For a manual release, confirm the actual fiat payment in your own account matches the order; a message or screenshot alone is insufficient.

Source: [Manual release guidance](https://support.peer.xyz/managing-a-deposit/ive-been-contacted-to-manually-release-payment-what-should-i-do). This bot explains the rule; it does not release funds or approve a release. Route a concerning case to official support.

### Troubleshooting

**Paid, but verification failed?** Continue verification on that same order; don't send another payment or cancel it while resolving the issue. If retrying fails, use [Peer Support](https://support.peer.xyz) with the order link and error message. Keep payment evidence on the official support channel.

Source: [Payment verification timed out or failed](https://support.peer.xyz/completing-an-order/proof-generation-timed-out-or-failed). Begin with the least disruptive documented step. Do not operate the user's browser, reinstall extensions, change settings or collect credentials from this informational chat.

## More specific support questions

| Situation                           | Supported guidance                                                                                                                                                                      | Source                                                                                              |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| An order is pending                 | Use the order's displayed countdown. Duration varies; no generic fixed expiry. If already paid, contact support rather than waiting for expiry.                                         | [Stuck or pending order](https://support.peer.xyz/completing-an-order/my-order-is-stuck-or-pending) |
| Seller wants to withdraw            | Available liquidity can be withdrawn through the site's deposit management. Amounts committed to active orders remain reserved until completion/cancellation or expiry and pruning.     | [Managing a deposit](https://support.peer.xyz/managing-a-deposit)                                   |
| Buyer wants a refund                | Contact official support first. Support can help contact the seller but does not directly control the user's funds or guarantee a refund.                                               | [Refund help](https://support.peer.xyz/completing-an-order/how-do-i-get-a-refund)                   |
| Wrong amount, currency or recipient | Keep the existing order. Use the relevant official error article or support; do not prescribe a second payment as a generic fix.                                                        | [Completing orders](https://support.peer.xyz/completing-an-order)                                   |
| Crypto not on expected chain        | An order completing and cross-chain delivery are distinct. Check the selected route and official instructions; this bot cannot inspect a private balance or promise bridging succeeded. | [Buyer guide](https://docs.peer.xyz/guides/for-buyers/complete-guide-to-onboarding)                 |

## Prices, methods and currencies

- Fetch every requested price from the read-only public source. Keep freshness, eligibility and reservation checks internal; verified snapshots need no Estimated or Indicative label. Use decimal human units and distinguish a fiat budget from target USDC. A market reference must be labelled market value rather than a bank payout.
- A bounded public orderbook scan does not establish the absolute best price, every eligible offer or guaranteed liquidity. A quote failure must stay a failure; do not substitute an old number.
- Use the quote source's live capabilities for supported combinations. Explain that the list describes that surface; destination eligibility and liquidity are checked there.
- Peer's marketing site, support pages, SDK and USDCtoFiat do not expose identical lists. In this review, the Peer homepage advertised more Revolut/Wise currencies than USDCtoFiat and the pinned Cash SDK. The general provider support page also omitted rails present on other first-party surfaces. Do not flatten those into one static global currency count.
- Payment-platform presence is not evidence of universal country availability, account eligibility, identity requirements, fees or extension requirements. Avoid unsupported claims such as "works everywhere", "no KYC anywhere" or "no extensions needed".

Reference discovery: [Peer docs](https://docs.peer.xyz), [Peer general help](https://support.peer.xyz/general), [USDCtoFiat payment methods](https://usdctofiat.xyz).

## Refresh and review policy

Live prices and liquidity must be fetched for the request and carry their observation time where available. Never use this document as a price source.

Review these guide links and summaries before each release, and again when a user reports changed behavior or asks about a time-sensitive requirement. Re-open the specific official page before asserting current fees, payment methods, country/account eligibility, extension requirements or procedural details. If live verification is unavailable, say the requirement needs checking on the destination rather than presenting this review date as current proof.

When sources conflict, prefer the chosen product's live options and review screen for that product. Use the detailed relevant support article for a specific failure; do not repeat conflicting marketing shorthand. Record unresolved discrepancies without inventing a reconciliation.

Keep guidance under approximately 60 words by default. Link the exact supporting source near a material claim. Do not fill a normal answer with package, SDK, privacy architecture or implementation commentary. Offer one useful next action.

## Verified TOFIAT handoffs

Verified on 29 October 2026 from current public first-party assets and the public referral lookup API. TOFIAT is active and belongs to the expected integration wallet.

- Web: https://app.peer.xyz/referrals?referralCode=TOFIAT. Current public app code reads the code, waits for authentication/wallet readiness and attempts eligible redemption; external-wallet redemption uses the destination's signature flow. Existing referrals are not replaced. [Web referral bundle](https://app.peer.xyz/assets/Referrals-TyGPcXgj.js).
- Mobile: https://mobile.peer.xyz/onboard?referralCode=TOFIAT. The onboarding page preserves the code into the installed app. After a fresh store installation, return to the same link and tap Continue in Peer App; the store link itself is not verified deferred attribution. [Mobile onboarding bundle](https://mobile.peer.xyz/_next/static/chunks/app/onboard/page-11d95a4645be8ddd.js).
- Do not use peer.xyz?referralCode=TOFIAT for attribution: current marketing app links do not retain the code.
- The documented wallet-referral earnings event is qualifying referred-seller liquidity being filled, not a wallet connection or buy alone. [Official referral program](https://docs.peer.xyz/guides/for-sellers/referrals).
- USDCtoFiat independently embeds peer-ref-TOFIAT on standard sell deposits and referralCode TOFIAT through its Cash path. No extra query parameter is needed on its sell link. This is deposit integration credit rather than wallet referral enrollment. Verified in the owning personal source; actual new referral redemption was not performed.

Keep these distinctions internal unless asked. Ordinary replies should be clean and confident, normally 20–40 words: one bold amount/answer, a useful flag or native choice card when appropriate, one attributed action link, no boilerplate. Verified snapshots use separate pay/receive rows and no Estimated/Indicative label. Retain freshness and actual payout versus market-value distinctions in the working logic.

## Human deposit lookup

Verified 29 October 2026 against the existing public Peerlytics routes. A plain deposit ID is accepted by `/api/explorer/deposit/{id}`. The response includes the selected `data.deposit` and raw `linked.alternates`; a number can match several escrows on the same chain. Ask for the wallet address or offer brief state/balance/date choices rather than making the person supply a composite reference. Pin the selected returned full ID internally because the default candidate ranking can change with liquidity.

The address endpoint `/api/explorer/address/{address}?limit=100&offset=0` exposes seller-owned rows under `linked.activity.makerDeposits`; verify the depositor. Its raw USDC amounts use six decimals. The broader `data.deposits` also includes escrow and delegated roles. Customer labels use **Deposit #1300** and a human receipt link. Source IDs remain an internal lookup detail.

## Live routes instead of a bot catalog

The desk is platform-agnostic: “what can I use” means the payment apps with at least one public offer in that currency in the current orderbook read. New apps and currencies appear without a skill change. A route with no current offer is described as having no live offers, not as unsupported. Product-specific selectors (USDCtoFiat, Peer web) are not read; the sell deep link falls back gracefully if a product does not offer a pair.

For fiat rounding, prefer explicit route units. Otherwise resolve digits through the runtime’s `Intl.NumberFormat`. The generic skill stores the lookup procedure and safety rules, never a live fee, rate or platform list.
