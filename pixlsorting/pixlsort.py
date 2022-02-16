from PIL import Image
from random import randint
from argparse import ArgumentParser
from colorsys import rgb_to_hsv

# Defining arguments to be passed:
def arguments():
    parser = ArgumentParser(description="PixlSort: A simple pixel sorter for .jpg and .png images")

    parser.add_argument("input",
                        type=str)

    parser.add_argument("--output",
                        "-o",
                        dest="output",
                        type=str,
                        default="output.png",
                        help="Sets the name of the processed image.")

    parser.add_argument("--threshold",
                        "-t",
                        dest="threshold",
                        type=float,
                        default=100,
                        help="Sets the threshold value of pixels to sort.")

    parser.add_argument("--function",
                        "-f",
                        dest="function",
                        type=str,
                        default="brightness",
                        choices = {"brightness", "red", "green", "blue", "hue"},
                        help="Sets the function for the sorting script, \
                         accepted values: brightness,red, blue, green and hue.")

    parser.add_argument("--interval",
                        "-i",
                        dest="interval",
                        type=int,
                        help="Sets the maximum lenght of the sorting intervals, by default is the whole width or height of the image (Under Construction).")

    parser.add_argument("--vertical",
                        "-v",
                        dest="vertical",
                        action='store_true',
                        help='Sets the pixel sorting vertical (Default is Horizontal).')

    arguments = parser.parse_args()

    return {
        "input": arguments.input,
        "output": arguments.output,
        "threshold": arguments.threshold,
        "function": arguments.function,
        "interval_length": arguments.interval,
        "orientation": arguments.vertical
    }

#defining functions from which to make the processing
def brightness(r_g_b):
    r = r_g_b[0]
    g = r_g_b[1]
    b = r_g_b[2]
    bright = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return bright


def hue(r_g_b):
    r, g, b= r_g_b[:3]
    hue_value = rgb_to_hsv(r/255, g/255, b/255)
    return hue_value[0]


def red(r_g_b):
    return r_g_b[0]


def green(r_g_b):
    return r_g_b[1]


def blue(r_g_b):
    return r_g_b[2]

# we'll use the quick sort algorithm.
def quicksort(array, function):
    if len(array) < 2:
        return array

    low, same, high = [], [], []

    pivot = array[randint(0, len(array) - 1)]

    for item in array:
        if function(item) < function(pivot):
            low.append(item)
        elif function(item) == function(pivot):
            same.append(item)
        elif function(item) > function(pivot):
            high.append(item)

    return quicksort(low, function) + same + quicksort(high, function)



def main():
    args = arguments()
    input_image = args.pop("input")
    output_image = args.pop("output")
    threshold = args.pop("threshold")
    function = args.pop("function")
    interval = args.pop("interval_length")
    orientation = args.pop("orientation")

    print('Welcome to PixlSort.\ninput: %s\noutput: %s\nthreshold: %f\nsorting by: %s\n'% (input_image, output_image, threshold, function))

    if function == 'hue':
        sorting_function = hue
    elif function == 'red':
        sorting_function = red
    elif function == 'green':
        sorting_function = green
    elif function == 'blue':
        sorting_function = blue
    elif function == 'brightness':
        sorting_function = brightness


    with Image.open(input_image) as im:
        if orientation:
            im = im.rotate(90, expand=True)

        px = im.load()
        width = im.width
        height = im.height
        if not interval:
            interval = im.width

    print("width %s" % width)
    print("height %s" % height)
    print("sorting...")

    temSort = []
    rows = 1
    x = 0
    for y in range(height):
        while x < width:
            pixel = px[x, y]
            a = x + 1
            pxls = 0
            while sorting_function(pixel) < threshold:
                temSort.append(pixel)
                if a >= width:
                    break
                else:
                    pixel = px[a, y]
                    a += 1
                pxls += 1
            pxls = 0
            if temSort:
                a = x
                temSort = quicksort(temSort, sorting_function)
                for i in range(len(temSort)):
                    px[a, y] = temSort[i]
                    a += 1
                x = a - 1
            x += 1
            temSort = []
        x = 0

    final = []
    for y in range(height):
        for x in range(width):
            final.append(px[x, y])

    newimage = Image.new(mode="RGB", size=(width, height))
    newimage.putdata(final)
    if orientation:
        newimage = newimage.rotate(-90, expand=True)
    newimage.save(output_image, "PNG")
    im.close()
    newimage.close()
    print('Image succesfully processed.')


if __name__=="__main__":
    main()