# Peerboop image pack

Four still images for X and the README; there are no videos. Every image is real Grok Bot chat from the published **Peerboop P2P 1.6.2** template ([x.ai/bot/OVV5tPy7c0yg5WyMfv6pj](https://x.ai/bot/OVV5tPy7c0yg5WyMfv6pj)), added through Grok’s native Add Bot dialog at 16:17 UTC on 29 October 2026, with no setup messages before the first question.

| Image | Prompt | Reply (UTC) | Independent check |
| --- | --- | --- | --- |
| [01-buy](../assets/marketing/01-buy.png) | What's the cheapest way to buy 100 USDC with USD? | 16:18:06 | Orderbook generated 16:17:55, 119 rows: Chime, Revolut, Wise (and Venmo, stake) $102.98, Zelle $105.00, fee 0.959111 USDC |
| [02-sell](../assets/marketing/02-sell.png) | Sell 250 USDC to Revolut EUR? | 16:18:30 | Orderbook generated 16:18:26: market €224.04, lowest Revolut EUR seller €0.9544 (+6.5%), 5 sellers, 5,331.298 USDC |
| [03-venmo](../assets/marketing/03-venmo.png) | Can I buy 100 USDC with Venmo? | 16:18:48 | Venmo orderbook generated 16:18:44: cheapest fillable stake-backed offer $102.98 |
| [04-track](../assets/marketing/04-track.png) | Check deposit 1300 | 16:19:07 and 16:19:23 | Peerlytics deposit API: three deposits numbered 1300; the selected one has 3,192.71 available, 0 reserved, 302,695.46 sold |

## How they are made

1. Grok Bot was zoomed to 200% (Cmd+=) so the chat renders at native resolution on a 1× display, then `screencapture -l` captured the window. Zoom was reset afterwards.
2. [crop_bubbles.py](../assets/marketing/crop_bubbles.py) cuts each user bubble, bot message and native card at its exact edge without changing a pixel. The crops are in [captures/](../assets/marketing/captures/).
3. [build.py](../assets/marketing/build.py) writes an editable HTML layout per image and renders the PNG with headless Chrome. The crops keep their conversation order, and every crop in an image is scaled by one factor (1.2–1.8×) so it reads at phone width. Only the gap between a question and its replies is tightened. Nothing is reordered, retyped or left out. Image 04 shows the wallet card after option A was chosen, as Grok displays it, followed by the balances that came back.

Each bot reply opens with Grok’s short holding line (“Pulling the live USD offers now.”). It is left in because it is what the bot sent. Outside the chat there is only the Peerboop mark. Capture dates live here rather than on the images. Sidebar, account and setup content are cropped away. The masked wallets in 04 belong to a public example deposit.

## Limits

Prices are a dated snapshot, not current offers, and no trade was placed. The [launch post](LAUNCH.md) is unpublished.
