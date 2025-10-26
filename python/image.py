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

def fetch_image(file_name: str, width: int=600) -> Image:
    """
    Read an image file and return for embedded display.

    Images are assumed to lie in to which "../images"
    (TODO: generalize).

    Args:
        file_name: of image
        width: in pixels of returned image

    Returns:
        resized image as IPython display image

    """
    return Image(join(pardir, "images", file_name), width=width,)
