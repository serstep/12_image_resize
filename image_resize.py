import argparse
from PIL import Image
from pathlib import PurePosixPath

def get_args_namespace():
    argument_parser = argparse.ArgumentParser(description="Image Resize Script", usage='%(prog)s [arguments]')
    argument_parser.add_argument("--scale", "-s", type=float)
    argument_parser.add_argument("--width", "-w", type=int)
    argument_parser.add_argument("--height", "-i", type=int)
    argument_parser.add_argument("--output", "-o")
    argument_parser.add_argument("filepath")

    args_namespace = vars(argument_parser.parse_args())

    scale = args_namespace["scale"]
    width = args_namespace["width"]
    height = args_namespace["height"]

    if scale is None and width is None and height is None:
        print("--scale/-s or (--width/-w or --height/-h) required")
        exit(1)

    if not(scale is None or (width is None and height is None)):
        print("--scale/-s is not allowed with --width/-w or --height/-h")
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


def proportion_notice(initial_size, resized_size):
    """
    Compare proportion of initial image an resized image.
    Diiference in proportions compares with little constant, 
    because result of division is float and in most of cases is less than 1.
    """
    resized_width , resized_height = resized_size
    initial_width, initial_height = initial_size

    return resized_height / resized_width - initial_height / initial_width > 0.1
        


def resize_image(image, args_namespace):

    scale = args_namespace['scale']
    required_width = args_namespace['width']
    required_height = args_namespace['height']
    filepath = args_namespace["filepath"]
    output_path = args_namespace["output"]

    width, height = image.size

    if scale is not None:
        required_width = int(width*scale)
        required_height = int(height*scale)
        resized_image = image.resize((required_width, required_height))

    elif required_width is not None and required_height is not None:
        resized_image = image.resize((required_width, required_height))

    elif required_width is not None and required_height is None:
        required_height = height * (required_width // width)
        resized_image = image.resize((required_width, required_height))

    elif required_width is None and required_height is not None:
        required_width = width * (required_height // height)
        resized_image = image.resize((required_width, required_height))

    
    return resized_image
    

if __name__ == '__main__':
    args_namespace = get_args_namespace()
    filepath = args_namespace["filepath"]
    output_path = args_namespace["output"]

    image = Image.open(filepath)
    resized_image = resize_image(image, args_namespace)

    if proportion_notice(image.size, resized_image.size):
        print("Notice: the proportion of image wiil be upset.")

    result_image_path = get_result_path(filepath, output_path, resized_image)

    try :
        resized_image.save(result_image_path)
    except OSError:
        print("Image saving error.")
