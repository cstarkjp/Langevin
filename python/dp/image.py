"""
Fetch a PNG/JPEG etc image and return as an IPython display image.
"""
import warnings
from os.path import join, pardir
from IPython.display import Image 

warnings.filterwarnings("ignore")

__all__ = [
    "fetch_image"
]

def fetch_image(filename: str, width: int=600) -> Image:
    """
    Read an image file and return for embedded display.

    Args:
        filename: to which "../Images" are prepended when trying to load
        width: in pixels of returned image

    Returns:
        resized image as IPython display image

    """
    return Image(join(pardir, "Images", filename), width=width,)
