```
usage: resizeimage [-h] -i INPUT [-o OUTPUT] [-n TOLERANCE] [-v] (-s TARGETSIZE | -p PERCENT)

Utility to resize an image to a target file size

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to source image. Examples: "F:\Desktop\img.png", "/home/maria/img.jpg"
  -o OUTPUT, --output OUTPUT
                        Where to save new resized file. If not given, defaults to same folder as input
  -n TOLERANCE, --tolerance TOLERANCE
                        Resize image within X % of your desired file size (default=5)
  -v, --verbose         Print more details about operation to console
  -s TARGETSIZE, --targetsize TARGETSIZE
                        Desired file size in bytes. Examples: -s 40kb, --targetsize 0.3mb, -s 1.2MB, -s 941KB
  -p PERCENT, --percent PERCENT
                        Desired file size by percent (%). Examples: -p -40% or -p 60%, --percent 80%, -p 15, -p -32.5
```
