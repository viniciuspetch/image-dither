# Image Dither
My own implementation of a image dithering script, made in [Python](https://www.python.org/), with the [numpy](https://numpy.org/) and [pillow](https://pillow.readthedocs.io/en/stable/index.html) packages. Currently it only uses [Floyd-Steinberg's algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering) and has only a couple of configurable options.

## Notes
There's still some kinks to be solved. From some testing, flat colors are still being specked with dots unnecessarily, and there's still generation of leftover files.

Also due to the focus on implementation and disregard for performance, it may be quite slow for bigger pictures.

## Requirements
- Python 3.x
- pip

## Usage
- Set up virtual environment: `python3 -m venv venv`, `source venv/bin/activate`;
- Install packages: `python3 -m pip install -r requirements.txt`
- Run the script: `python3 main.py <options>`

### Options
- `-h`: Show the script's manual.
- `-i <file>`: File being dithered.
- `-m <mode>`: Palette mode to be used when converting the original image's colors. `<mode>`=`bw` Generates a black-and-white image. `<mode>`=`original`: Reuse the original image's colors.  `<mode>`=`custom`: Uses the palette defined on custom_palette.txt. Defaults to `<mode>`=`bw`.
- `-c <amount>`: If "original" palette mode is used, define the amount of colors used. Defaults to `<amount>`=`2`.
- `-s <newSize>`: Resizes the original image. `<newSize>` defines the size of the biggest dimension (so height if it's a portrait, width if landscape).