# 12_image_resize

Script image_resize.py provides to resize images.

##Using

    $python3 image_resize.py (--scale/-s|--width/-w --height/-i) filepath --output/-o output_filepath

scale - float property
width, height - integer properties

You can use only width-height resizing or scale resizing, not both of them.
If you set only width or only height parameters, res parameter will be set in propotion to initial image.
