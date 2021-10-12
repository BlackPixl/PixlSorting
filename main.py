from PIL import Image
from random import randint
from argparse import ArgumentParser
from colorsys import rgb_to_hsv


# Defining parameters:
def arguments():
    parser = ArgumentParser(description="A simple pixel sorter for .jpg and .png images",
                            usage="*Under construction*")

    parser.add_argument("input",
                        type=str)

    parser.add_argument("-o",
                        type=str,
                        default="output.png")

    parser.add_argument("-t",
                        type=float,
                        default=150,
                        help="Sets the point where the script starts sorting the pixels.")

    parser.add_argument("-f",
                        type=str,
                        default="hue",
                        choices = {"brightness, red, green, blue, hue"},
                        help="Sets the function for the sorting script, \
                         accepted values: brightness,reds, blues, greens")

    parser.add_argument("-i",
                        type=int,
                        help="Sets maximum interval lenght to the image, by default is the whole width or height")

    parser.add_argument('-v',
                        action='store_true',
                        help='Sets the pixel sorting vertical (Default is Horizontal)')

    arguments = parser.parse_args()

    return {
        "input": arguments.input,
        "output": arguments.o,
        "threshold": arguments.t,
        "function": arguments.f,
        "interval_length": arguments.i,
        "orientation": arguments.v
    }

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


args = arguments()
input_image = args.pop("input")
output_image = args.pop("output")
threshold = args.pop("threshold")
function = args.pop("function")
interval = args.pop("interval_length")
orientation = args.pop("orientation")

# TODO: User logger instead of print
print('Welcome to PixlSort.\ninput: %s\noutput: %s\nthreshold: %f\n' % (input_image, output_image, threshold))

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

# TODO: Change print to logger
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
