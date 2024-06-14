"""
ArgumentParser subclass needed for image resizer.
"""

import argparse
import sys

help_flags = ('help', '--help', '-h', '/?', '?')

class ResizerParser(argparse.ArgumentParser):
    def __init__(self) -> None:
        super().__init__(
            prog='resizeimage',
            description='Utility to resize an image to a target file size',
            add_help=True
        )
        self._add_args()

    def error(self, message) -> None:
        print(f'ResizeParserError: {message}\n', file=sys.stderr)
        self.print_help()
        sys.exit(2)

    def parse_args(self, args=None, namespace=None) -> argparse.Namespace:
        if args is None:
            args = sys.argv[1:]
        
        if len(args) < 1 or (args[0].lower() in help_flags):
            self.print_help(sys.stderr)
            sys.exit()

        return super().parse_args(args, namespace)

    def _add_args(self) -> None:

        # file path input required
        self.add_argument(
            '-i', '--input',
        help=(
            'Path to source image. Examples: "F:\\Desktop\\img.png", '
            '"/home/maria/img.jpg"'
        ),
        required=True,
        type=str
        )

        # file path output is NOT required;
        # if not specified, resized image will be saved in same folder as input
        self.add_argument(
            '-o', '--output',
            help=(
                'Where to save new resized file. If not given, defaults to '
                'same folder as input'
            ),
            required=False,
            type=str
        )

        # tolerance (X%) within which an image resize can be considered
        # "successful." (defaults to 5)
        self.add_argument(
            '-n', '--tolerance',
            help=(
                'Resize image within X %% of your desired file '
                'size (default=5)'
            ),
            required=False,
            type=str
        )

        self.add_argument(
            '-v', '--verbose',
            help=(
                'Print more details about operation to console'
            ),
            action='store_true',
            required=False,
        )
        
        # argument group -- user must give either '-s' OR '-p', but NOT both
        g = self.add_mutually_exclusive_group(required=True)
        # resizeimage -i <INPUT_FILEPATH> -o <OUTPUT_FILEPATH> 
        #   --targetsize 40kb/40mb
        g.add_argument(
            '-s', '--targetsize',
            help=(
                'Desired file size in bytes. Examples: -s 40kb, '
                '--targetsize 0.3mb, -s 1.2MB, -s 941KB'
            ),
            type=str
        )
        # resizeimage -i <INPUT_FILEPATH> -o <OUTPUT_FILEPATH> 
        #   --percent 80% (or -20%)
        g.add_argument(
            '-p', '--percent',
            help=(
                'Desired file size by percent (%%). Examples: '
                '-p -40%% or -p 60%%, --percent 80%%, -p 15, -p -32.5'
            ),
            type=str
        )




