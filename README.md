# 24 November 2026 — World News in One Image

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/AllisonMuse/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/AllisonMuse/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

An entry for [make.fun's "Sum up 24 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261124) ($100, 50 places paid). The program (`main.ts`, Node 22, standard
library only) copies `entry.png` to the output directory; the image is a
1024×1024 PNG drawn at build time by `draw_news.py` (Python + Pillow),
so both grader runs write identical bytes. No network is used at run time.

## The six stories in the image

All six were first reported on Tuesday 24 November 2026. Claims are
attributed in the image where the reporting itself says they are
unconfirmed. Nothing was invented.

1. **Strait of Hormuz — Iran reports four tankers hit mines.**
   Iran's IRGC said three oil tankers hit naval mines and caught fire,
   then said a fourth tanker hit a mine. The IRGC also said its navy
   attacked a container ship in the strait. The Joint Maritime
   Information Centre said the mine claims were unconfirmed.
2. **Riyadh, Saudi Arabia — Houthi drone hits PIF tower; 11 injured.**
   Saudi Civil Defence said a Houthi drone attack on a tower in Riyadh's
   King Abdullah Financial District wounded 11 people: two Saudis, two
   Indians, three Nepalis and four Egyptians.
3. **New York, USA — Huawei guilty on 10 of 12 counts.**
   A US federal jury in Brooklyn convicted Huawei of conspiracy to steal
   trade secrets and bank fraud, and acquitted it of racketeering
   conspiracy.
4. **Ukraine war — Ukraine drones hit Russian ships.**
   Kyiv said drones struck the Russian cargo ship Sparta II in the Gulf
   of Finland (crew evacuated, ship towed to port) and struck ships off
   Libya.
5. **Markets — AI rally cools after Huang's return.**
   Tech stocks slipped on Tuesday, a day after Nvidia reinstated Jensen
   Huang as chief executive and sparked a market rally.
6. **South Korea — Russian jets enter air-defence zone.**
   South Korea's military said several Russian aircraft entered its air
   defence identification zone near Ulleungdo; fighter jets were
   scrambled and no territorial airspace was violated. (Earlier reports
   misidentified the aircraft as possibly North Korean; the military
   corrected this.)

## Sources (all dated 24 November 2026)

- Reuters — "China's Huawei convicted in US in sprawling criminal trial
  over Iran business", 24 Nov 2026.
  https://www.reuters.com/legal/litigation/chinas-huawei-convicted-us-criminal-trial-stemming-iran-business-2026-11-24/
- Al Jazeera — "Saudi civil defence says 11 injured in Houthi drone
  attack on Riyadh tower", 24 Nov 2026.
  https://www.aljazeera.com/amp/news/2026/11/24/saudi-led-coalition-condemns-terrorist-attack-on-tower-in-riyadh
- Arab News — "11 injured in Houthi attack on tower in Riyadh's
  financial district", 24 Nov 2026.
  https://www.arabnews.com/saudi-arabia/11-injured-in-houthi-attack-on-tower-in-riyadhs-financial-district-3013857
- Dow Jones Newswires via Morningstar — "Top Markets Headlines",
  24 Nov 2026 (tech stocks backslide after the Nvidia rally; oil
  prices weighed shipping risks).
  https://www.morningstar.com/news/dow-jones/202611245205/dow-jones-top-markets-headlines-at-11-am-et-tech-stocks-backslide-after-epic-rally-us
- Daily Summary Of — "World News: 24 November 2026" (30 stories,
  64 sources), published 24 Nov 2026.
  https://dailysummaryof.com/world/2026-11-24
- Gulf News — live coverage, 24–25 Nov 2026 (Hormuz shipping,
  Riyadh attack).
  https://gulfnews.com/world/mena/middle-east-conflict-us-investigates-iran-over-cyberattacks-on-50-ships-as-fresh-sanctions-target-irans-shadow-banking-network-1.500758688

## Verify

```sh
python3 draw_news.py        # regenerates entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# run main.ts twice and compare the two outputs: they are byte-identical
```
