[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/qienzdork/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/qienzdork/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday, 21 November 2026 — The World in One Day

A clean editorial poster summing up Saturday 21 November 2026 in six
stories, drawn with Python and PIL (no photos, no AI image generation):

1. **Iran strikes Bahrain** — Tehran says it hit two US military positions;
   Bahrain says an industrial site was set ablaze, with no injuries.
2. **Cartel boss "El Chapo Isidro" captured** — Mexican forces seized FBI
   most-wanted Fausto Isidro Meza Flores in Sinaloa; at least 11 died in
   the violence that followed.
3. **Missile hits Zelenskyy's hometown** — a Russian ballistic missile struck
   central Kryvyi Rih, killing two and wounding dozens; missiles also
   landed in Poland.
4. **COP31 talks run past deadline** — UN climate talks in Antalya, Turkey,
   entered overtime, still split over fossil fuels.
5. **Stocks slide into correction** — an AI and chip sell-off pushed US
   stocks into correction; the Nasdaq had its worst week since March 2020.
6. **Mosquitoes cut child dengue by 69%** — specially bred mosquitoes cut
   dengue infections in children by about 69% in a major Brazil study.

## How it works

`draw_poster.py` renders the 1024x1024 poster as `entry.png` using only
PIL shapes and text. `main.py` (standard library only, no network) copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`),
verifying the PNG magic bytes first. Both runs write identical bytes.

Sources: Reuters, Associated Press, CNN.
