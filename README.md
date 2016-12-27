# 12_image_resize

Script image_resize.py provides to resize images.

##Using

    $python3 image_resize.py (--scale|--width --height) filepath --output/-o 

scale - float property
width, height - integer properties

You can use only width-height resizing or scale resizing, not both of them.
If you set only width or only height parameters, res parameter will be set in propotion to initial image.

If you don't set output filepath, it wiil be set authomatically in format: filepath__widthXheight.extension
