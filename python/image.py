"""
Fetch a PNG/JPEG etc image and return as an IPython display image.
"""
import warnings
from os.path import join #, pardir, abspath
from IPython.display import Image 
import lvn

warnings.filterwarnings("ignore")

__all__ = [
    "fetch_image"
]

def fetch_image(dir: tuple, file_name: str, width: int=600,) -> Image:
    """
    Read an image file and return for embedded display.

    Images are assumed to lie in to which "<lvn>/images".

    Args:
        dir: path to images as tuple
        file_name: of image
        width: in pixels of returned image

    Returns:
        resized image as IPython display image

    """
    # images_dir: str = abspath(join(lvn.__file__, pardir, "images"))
    return Image(join(*dir, file_name), width=width,)
