# PixlSorting
A Python console app, made to perform pixel sorting style image manipulation.

More info and examples at the [PixelSorting subreddit](https://www.reddit.com/r/pixelsorting/).

## Tools used
* [Python Imaging Library (PIL)](https://python-pillow.org).

## Installation
```console
# clone the repo
$ git clone https://github.com/BlackPixl/PixlSorting.git

# change the working directory to PixlSorting
$ cd PixlSorting

# install the requirements
$ python3 -m pip install -r requirements.txt
```

## Usage
```console
python3 pixlsorting [-h]
                    [--output OUTPUT]
                    [--threshold THRESHOLD]
                    [--function {green,blue,brightness,red,hue}]
                    [--interval INTERVAL]
                    [--vertical]
                    input

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Sets the name of the processed image.
  --threshold THRESHOLD, -t THRESHOLD
                        Sets the threshold value of pixels to sort.
  --function {green,blue,brightness,red,hue}, -f {green,blue,brightness,red,hue}
                        Sets the function for the sorting script, accepted values: brightness,red, blue, green and hue.
  --interval INTERVAL, -i INTERVAL
                        Sets the maximum lenght of the sorting intervals, by default is the whole width or height of the image (Under
                        Construction).
  --vertical, -v        Sets the pixel sorting vertical (Default is Horizontal).
```
## Note:
While sorting by red, blue, green and brightness, the ideal values for the threshold are from 0 to 255.

While  sorting by hue, the ideal values to use for the threshold are from 0 to 1.

The threshold is set to 100 by default.

## Examples:
```console
python3 pixlsorting input1.png -o output1.png -t 215 -f brightness -v
```

```console
python3 pixlsorting input2.png -o output2.png -t 57 -f brightness -v
```
Play with all possible options to see what results can you get!
