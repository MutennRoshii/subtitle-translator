# Subtitle Translator

## Description

This is a simple script that translates subtitle files from one language to another
using the website https://translatesubtitles.co/.

The website is free to use,
but has no API. If you appreciate the service,
please consider donating to them.

This script automates the process of translating subtitles using
Playwright. Using the googletrans library it is possible to translate
the subtitles, but I have found this to be very slow.

## Usage

The script takes three arguments:

| Arg         | Description                                            | Type                            | Default |
|-------------|--------------------------------------------------------|---------------------------------|---------|
| file-path   | The path to the subtitle file to be translated         | Required, positional            |         |
| output-dir  | The directory to write the translated subtitle file to | Optional, `-o`, `--output-dir`  | pwd     |
| target-lang | The language to translate the subtitles to             | Optional, `-l`, `--target-lang` | nl      |

```bash
python tl-subs.py ./movie-en.srt --output-dir ~/downloads  # write to downloads folder
python tl-subs.py ./movie-en.srt --target-lang fr          # translate to french
python tl-subs.py ./movie-en.srt -o ./subs -l es           # write to downloads and translate to spanish
```

## Installation

Clone the repository and install the dependencies:

```bash
git clone <this repo>
cd <this repo>

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```


