import argparse
from PIL import Image
from pathlib import PurePosixPath

def get_args_coolision(args_namespace):
    scale = args_namespace.scale
    width = args_namespace.width
    height = args_namespace.height

    if scale is None and width is None and height is None:
        return "--scale/-s or (--width/-w or --height/-h) required"
        
    if not(scale is None or (width is None and height is None)):
        return "--scale/-s is not allowed with --width/-w or --height/-h"

    return None
        

def get_args_namespace():
    argument_parser = argparse.ArgumentParser(description="Image Resize Script", usage='%(prog)s [arguments]')
    argument_parser.add_argument("--scale", "-s", type=float)
    argument_parser.add_argument("--width", "-w", type=int)
    argument_parser.add_argument("--height", "-i", type=int)
    argument_parser.add_argument("--output", "-o")
    argument_parser.add_argument("filepath")

    args_namespace = argument_parser.parse_args()

    args_coolision = get_args_coolision(args_namespace)

    if args_coolision is not None:
        print(args_coolision)
        exit(1)
    
    return args_namespace


def get_result_path(filepath, output_path, image):
    if output_path is not None:
        return output_path

    width, height = image.size
    image_path = PurePosixPath(filepath)
    image_name = image_path.stem
    image_parent = image_path.parent
    image_extension = image_path.suffix
    return "{}/{}__{}x{}{}".format(image_parent, image_name, width, height, image_extension)


def compare_proportion(initial_size, resized_size):
    resized_width , resized_height = resized_size
    initial_width, initial_height = initial_size

    return abs(resized_height / resized_width - initial_height / initial_width) > 0.1


def get_required_size(image, args_namespace):

    scale = args_namespace.scale
    required_width = args_namespace.width
    required_height = args_namespace.height
    filepath = args_namespace.filepath
    output_path = args_namespace.output

    width, height = image.size

    if scale is not None:
        required_width = int(width*scale)
        required_height = int(height*scale)

    elif required_width is not None and required_height is None:
        required_height = height * required_width // width

    elif required_width is None and required_height is not None:
        required_width = width * required_height // height
    
    return(required_width, required_height)
    
    
if __name__ == '__main__':
    args_namespace = get_args_namespace()
    filepath = args_namespace.filepath
    output_path = args_namespace.output

    image = Image.open(filepath)
    required_size = get_required_size(image, args_namespace)
    resized_image = image.resize(required_size)

    if compare_proportion(image.size, resized_image.size):
        print("Notice: the proportion of image wiil be upset.")

    result_image_path = get_result_path(filepath, output_path, resized_image)

    try :
        resized_image.save(result_image_path)
    except OSError:
        print("Image saving error.")
