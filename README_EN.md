# yt_downloader

A simple program for downloading videos and music from YouTube with format selection, destination folder management, and operation logging.

## Features

- Download video or audio only from YouTube
- Select format and quality
- Copy files to chosen directories (with the ability to add/remove paths)
- Check free disk space before downloading
- Log operations to `log.txt`
- Configure directories via `.env` file
- Unit tests included

## Requirements

- Python 3.8+
- yt-dlp
- python-dotenv

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Configure the `.env` file (optional) with default paths.
2. Run the program:

```bash
python ytdownloader.py
```

3. Follow the instructions in the terminal.

## Tests

To run unit tests:

```bash
python test_basic.py
```

## Notes

- This program is not intended for downloading copyrighted materials without the owner's permission.
- Use in accordance with YouTube's Terms of Service.

---

**Feel free to report bugs and suggestions!**
