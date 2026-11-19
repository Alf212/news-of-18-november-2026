[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Alf212/news-of-18-november-2026/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Alf212/news-of-18-november-2026/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World in One Day — Wednesday 18 November 2026

An entry for make.fun's **news-image-20261118** contest: sum up one day's
world news in a single image. The image is a newspaper front page drawn
entirely in code — every headline is real type set by the drawing program,
so nothing in it can come out garbled.

## What the front page reports

All stories happened, or were first reported, on Wednesday 18 November
2026 (in some time zone), as covered that day by wire services and the
day's news roundups (AFP, AP, Reuters, Al Jazeera and national outlets):

- **Lead — Strait of Hormuz.** US jets struck an IRGC missile site on
  Qeshm Island; the US said it destroyed five Iranian tankers. Iran
  answered with drones against US bases in Bahrain and Kuwait; oil
  traded near $93.
- **APEC, Shenzhen.** Xi Jinping and Vladimir Putin met as the APEC
  summit opened, ahead of Thursday's three-way talks with Donald Trump;
  Quad leaders gathered in Manila.
- **Nvidia.** A record quarter: revenue of $115.8bn for the quarter to
  25 October, more than double a year earlier, on AI-chip demand. The
  board ruled out founder Jensen Huang's return as CEO.
- **Cyclone Akvan.** A severe Bay of Bengal storm closing on India's
  Andhra coast for a Friday landfall; Odisha evacuated towns and shut
  schools.
- **Ukraine.** A second night of strikes shut the Kerch (Crimea)
  Bridge; Kyiv counted 141 Russian drones in one night.
- **Also today.** The UN warned Gaza's displaced face deadly winter
  cold; Mary Peltola flipped Alaska's US Senate seat, putting Democrats
  on course for a 56–44 edge; COP31 climate talks in Antalya entered
  their final, still-divided days.

## How it is built

- `compose.py` — the drawing program (Python + Pillow, run locally
  only). It lays out the masthead, the date band, the lead scene and the
  four icon panels, and writes `entry.png` (1024×1024, ~133 KB).
- `entry.png` — the finished front page, committed to the repository.
- `main.py` — the contest program (Python 3.13, standard library only).
  The harness runs it twice with no network; it copies `entry.png` to
  `/output/entry.png`, byte for byte, both times.

Run the entry the way the harness does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
