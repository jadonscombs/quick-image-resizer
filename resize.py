"""
Driver file for image resizer program; intended to be used to downsize
images and not upscale. Unexpected behavior should be expected if program
is used instead to upscale an image.

This project is an improvement to StackOverflow user Jeronimo's answer 
(https://stackoverflow.com/a/52944228)(2018) and is for personal use only.

Other credit goes to:
https://stackoverflow.com/questions/4042452/
"""

import argparse
import io
import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from PIL import Image
from custom_parser import ResizerParser

# argparse verbose flag; if true, display more information during operations
verbose = False

def _get_file_data(
    src_image_file: str,
    format: str = None,
    curr_image: Image = None
) -> bytes:
    """
    Return image file data in bytes.
    """

    # if function call came from while loop...
    if not curr_image:
        # open image, and get file extension
        curr_image = Image.open(src_image_file)

    # change ".png"/".jpg"/etc. to "png", "jpg", ...
    if format is None:
        format = Path(src_image_file).suffix.strip('.')
    else:
        format = format.split('.')[-1]

    if verbose:
        print(f'[get_file_data] format: {format}')

    # open memory buffer, then temporarily save image to memory (not disk!),
    # then fetch/return image bytes
    with io.BytesIO() as buffer:
        curr_image.save(buffer, format=format)
        curr_image_data = buffer.getvalue()
        return curr_image_data


def _convert_percent_to_bytes(
    target_percent: float,
    source_image_file: str
) -> float:
    """
    Convert a percentage (e.g., 85.0) of bytes to actual target
    number of bytes; return the value 
    """
    image_data = _get_file_data(source_image_file)
    source_bytes = len(image_data)
    return (target_percent / 100) * source_bytes


def resize_image(
    src_image_file: str,
    dst_image_file: str,
    target_file_size_bytes: float,
    target_file_size_percent: float,
    resize_tolerance: float,
) -> None:

    curr_image = original_image = Image.open(src_image_file)
    aspect_ratio = curr_image.size[0] / curr_image.size[1]
    image_format = Path(dst_image_file)

    if verbose:
        print(f'dst_image_file: {dst_image_file}')
        print(f'image_format: {image_format}')

    while True:

        # get currently reduced file size (N number of bytes)
        data = _get_file_data(
            src_image_file,
            format=str(image_format),
            curr_image=curr_image
        )
        curr_file_size = len(data)
        
        # if user specified a percent (assuming more than 0%),
        # convert the % to bytes
        if target_file_size_percent > 0:
            target_file_size_bytes = _convert_percent_to_bytes(
                target_file_size_percent, src_image_file
            )

        # update current-to-target file size ratio;
        # ratio closer to 1:1 or 1:(1+tolerance) is better
        size_deviation = curr_file_size / target_file_size_bytes
        if verbose:
            print(
                f"size: {curr_file_size}; "
                f"factor: {round(size_deviation, 3)}"
            )

        # if current file size is within tolerance bounds of target size,
        # write the final image to file and exit script
        if size_deviation <= (100 + resize_tolerance) / 100:
            with open(dst_image_file, "wb") as f:
                f.write(data)
            print(
                f'Success. Resized file saved to '
                f'{Path(dst_image_file).resolve()}'
            )
            break
        else:
            # filesize not good enough => modify width and height
            # use sqrt of deviation since applied both in width and height
            new_width = curr_image.size[0] / size_deviation**0.5    
            new_height = new_width / aspect_ratio
            # resize from original image to preserve quality
            curr_image = original_image.resize(
                (int(new_width), int(new_height))
            )


def _parse_args(args, parser: ArgumentParser) -> dict:
    """
    Helper method. Process user arguments further, then return
    the args as a dict.
    """
    target_filesize_bytes = -1
    target_filesize_percent = -1
    tolerance = 5
    input_file, output_file = '', ''

    # check if <targetsize> was specified
    if args.targetsize:
        target_matches = re.match(
            r'([0-9]*[.]*[0-9]*)(kb|mb)',
            args.targetsize or '',
            flags=re.IGNORECASE
        )
        if target_matches:
            target_filesize_bytes, unit = target_matches.groups()
            target_filesize_bytes = float(target_filesize_bytes)
            if unit.lower() == 'kb':
                target_filesize_bytes *= 1024
            elif unit.lower() == 'mb':
                target_filesize_bytes *= 1024 * 1024
            else:
                sys.exit(
                    "Invalid targetsize units. Use 'kb' or 'mb' (no quotes)."
                )

    # otherwise check if <percent> was specified
    elif args.percent:
        percent_matches = re.match(
            r'(?:%*)(-?[.\d]+)\s*(?:%*)',
            args.percent
        )
        if percent_matches:
            target_filesize_percent = float(percent_matches.groups()[0])
            if abs(target_filesize_percent) > 100:
                raise parser.error(
                    "Invalid percent value (must not exceed +/-100.00)"
                )
            if target_filesize_percent < 0:
                target_filesize_percent = 100 - -target_filesize_percent
    else:
        raise parser.error("Invalid percent value. Exiting.")

    # now parse <tolerance>
    if args.tolerance:
        tolerance_matches = re.match(
            r'(?:%*)([.\d]+)\s*(?:%*)',
            args.tolerance
        )
        if tolerance_matches:
            tolerance = float( tolerance_matches.groups()[0] )
        
    # now parse <output>
    if not args.output:
        input_file = Path(args.input)
        output_base_name = input_file.name.removesuffix(
            "".join(input_file.suffixes)
        )
        #args.output = f"{output_base_name}_resized{input_file.suffix}"
        output_file = f"{output_base_name}_resized{input_file.suffix}"
    else:
        output_file = args.output

    return {
        'input': args.input,
        'output': output_file,
        'targetsize': target_filesize_bytes,
        'percent': target_filesize_percent,
        'tolerance': tolerance
    }


def main() -> None:

    # initialize custom argparser
    parser = ResizerParser()
    args = parser.parse_args()
    args = _parse_args(args, parser)

    # perform image resize
    resize_image(
        args['input'],
        args['output'],
        args['targetsize'],
        args['percent'],
        args['tolerance']
    )


if __name__ == '__main__':
    main()


