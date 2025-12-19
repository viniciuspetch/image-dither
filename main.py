from PIL import Image
import sys
import numpy as np
import math
import os

PALETTE = (
    (255, 255, 255),
    (0, 0, 0),
)
CMYK_PALETTE = (
    (255, 255, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (0, 0, 0),
)
RGB_PALETTE = (
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 0, 0),
)


def getMainColors(image, paletteSize):
    convertedImage = image.convert(
        mode="P", palette=Image.Palette.ADAPTIVE, colors=paletteSize
    )
    convertedImage.save("converted_output.png")
    palette = convertedImage.getpalette()
    parsedPalette = []
    for i in range(math.floor(len(palette) / 3)):
        parsedPalette.append([palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2]])
    return parsedPalette


def getPaletteDistances(a, b):
    return (
        math.pow((a[0] - b[0]), 2)
        + math.pow((a[1] - b[1]), 2)
        + math.pow((a[2] - b[2]), 2)
    )


def getClosestPalettePixel(pixel):
    distances = [(entry, getPaletteDistances(pixel, entry)) for entry in PALETTE]
    distances = sorted(distances, key=lambda x: x[1])
    return distances[0][0]


def resizeImage(image: Image, size):
    (width, height) = (image.width, image.height)
    newWidth = None
    newHeight = None
    bigger = max(width, height)
    newWidth = math.floor((width / bigger) * size)
    newHeight = math.floor((height / bigger) * size)
    return image.resize((newWidth, newHeight))


def parseArguments():
    options = {"mode": "bw", "originalCount": 1}
    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == "-h":
            print("-i: Input file.")
            print(
                '-m: Palette mode. "bw" = black-and-white, "original" = reuse most used colors on the original image. "custom" = uses a palette conversion defined on "custom_palette.txt". Defaults to "bw".'
            )
            print(
                '-c: If palette mode is "original", sets the amount of colors used, apart from black and white. Defaults to "2".'
            )
            print("-s: Resizes the original image to the given size. Keeps proportion.")
            sys.exit()
        elif sys.argv[i] == "-i":
            i += 1
            options["inputFile"] = sys.argv[i]
        elif sys.argv[i] == "-m":
            i += 1
            options["mode"] = sys.argv[i]
        elif sys.argv[i] == "-c":
            i += 1
            options["originalCount"] = int(sys.argv[i])
        elif sys.argv[i] == "-s":
            i += 1
            options["resize"] = int(sys.argv[i])
        i += 1
    print(options)
    if "inputFile" not in options:
        raise Exception("Input filepath is required")
    return options


options = parseArguments()
with Image.open(options["inputFile"]) as (image):
    # Get palette
    if options["mode"] == "bw":
        pass
    elif options["mode"] == "original":
        PALETTE = getMainColors(image, options["originalCount"])
        PALETTE.append((0, 0, 0))
        PALETTE.append((255, 255, 255))
    elif options["mode"] == "custom":
        with open("custom_palette.txt", encoding="utf-8") as file:
            colors = list(
                map(
                    lambda x: list(map(lambda y: int(y), x.split(","))),
                    file.read().split("\n"),
                )
            )
            print(colors)
            PALETTE = colors
    """ elif PALETTE_SOURCE == "cmyk":
        PALETTE = CMYK_PALETTE
    elif PALETTE_SOURCE == "rgb":
        PALETTE = RGB_PALETTE """

    # Do the thing
    print("Original image size: " + str(image.width) + " x " + str(image.height))
    if "resize" in options:
        image = resizeImage(image, options["resize"])
        print("Resized image size: " + str(image.width) + " x " + str(image.height))
    imgArray = np.array(image, np.int16)
    for y, array in enumerate(imgArray):
        print(f"Row: {y}")
        for x, pixel in enumerate(array):
            oldPixel = pixel
            newPixel = getClosestPalettePixel(pixel.astype(int))
            error = oldPixel - newPixel
            imgArray[y][x] = newPixel
            if x != imgArray.shape[1] - 1:
                imgArray[y][x + 1] = imgArray[y][x + 1] + error * 7 / 16
            if y != imgArray.shape[0] - 1:
                if x != 0:
                    imgArray[y + 1][x - 1] = imgArray[y + 1][x - 1] + error * 3 / 16
                imgArray[y + 1][x] = imgArray[y + 1][x] + error * 5 / 16
                if x != imgArray.shape[1] - 1:
                    imgArray[y + 1][x + 1] = imgArray[y + 1][x + 1] + error * 1 / 16
    newImg = Image.fromarray(np.uint8(imgArray))
    newImg.save("output.png")

    # Check sizes
    print(
        "Original size: "
        + "{:.2f}".format(int(os.path.getsize(options["inputFile"])) / 1024)
        + "KB"
    )
    print(
        "Final size: "
        + "{:.2f}".format(int(os.path.getsize("output.png")) / 1024)
        + " KB"
    )
