# MonsterAPI Image Generator with CLI

A command-line tool that generates AI images using MonsterAPI's `txt2img` model. Allows default or fully customized generation settings, downloads the output, and optionally opens the image(s) using your default browser.


## Features

- Generate AI images via MonsterAPI from your terminal
- Choose between **default** and **advanced** settings (steps, samples, seed, etc.)
- Auto-download and save images to disk
- Optionally open image(s) in your browser after generation
- Validates inputs using Pydantic
- Graceful handling of timeouts and API overloads


## Commands

This script is interactive, but includes:

- Prompt for input image description
- Prompt to select between:
  - `default` – Quick generation with pre-set values
  - `advance` – Full control over samples, steps, aspect ratio, etc.
- Option to open generated image(s) automatically
- Timeout protection with message to retry after a few hours


## Requirements

- **Python 3.13.5**
- Install dependencies using:

```bash
pip install -r requirements.txt
```


## Setup
1) Clone this repository or download the files:
```bash
git clone https://github.com/Feniel-Dhanak/monsterapi-with-python.git
```
2) Open `monsterapi_w_python.py` and replace the API key placeholder with your **MonsterAPI key**.
3) Don't forget to save.
4) Run the script in your terminal:
```bash
python monsterapi_w_python.py
```

**After generation:**
- The image(s) will be downloaded to your project folder
- If selected, images will open automatically using `open_image.py`
  
