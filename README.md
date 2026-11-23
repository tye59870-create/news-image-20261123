# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)

One image summing up the world news of Monday 23 November 2026: COP31
collapses in Antalya, the AI stock sell-off sinks markets, Trump dares Iran
over the Hormuz blockade, a Russian strike kills 15 near Kyiv, and
"El Chapo Isidro" is captured in Mexico — plus the day's other headlines.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

The image is rendered by `build_image.py` (Pillow, no network) and bundled as
`entry.png.b64` (base64 of the PNG, so the repository stays plain text);
`main.py` decodes it to `/output/entry.png`, deterministically.

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261123)</sub>
