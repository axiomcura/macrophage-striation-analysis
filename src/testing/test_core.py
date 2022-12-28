"""
Test module: test_core.py

Testing module focuses on testing the core functions of the analysis pipeline.
"""

import unittest
from pathlib import Path
from typing import Iterator

from PIL import Image

from src.common.file_io import load_tiff_images
from src.structs.selections import ImageCropSelection
from src.utils.image_utils import image_crop_walk


class TestUtils(unittest.TestCase):
    """Tests utilities functions"""

    def test_load_tiff_img(self) -> None:
        """With a given path to a `.tiff` file, should return and Image.Image
        object"""

        # loading directory
        loaded_img = load_tiff_images("./test_data/tiff_images")

        # checking if iterator is returned
        self.assertIsInstance(loaded_img, Iterator)

        # checking if elements are loaded as Image.Image types
        images = list(loaded_img)
        img_sel = images[0]
        self.assertIsInstance(img_sel, Image.Image)

    def test_load_tiff_with_empty_dir(self) -> None:
        """Testing loader with an empty directory. Should expect a
        `FileNotFoundError` if no `.tiff` files are found"""
        # loading
        jpeg_path = "./test_data/empty_dir"
        jpeg_img = load_tiff_images(jpeg_path)

        # since it's a generator we need to use the `next` function to trigger
        # the error
        self.assertRaises(FileNotFoundError, next, jpeg_img)

    def test_load_tiff_with_no_tiffs(self) -> None:
        """Tests focuses on attempting to load images that are not `.tiff`
        images. This should raise a `FileNotFoundError` since no `.tiff` files
        are found.
        """

        # loading
        jpeg_path = "./test_data/jpeg_imgs"
        jpeg_img = load_tiff_images(jpeg_path)

        # since it's a generator we need to use the `next` function to trigger
        # the error
        self.assertRaises(FileNotFoundError, next, jpeg_img)

    def test_iter_images(self) -> None:
        """Tests if images can be iterator"""

        img_iterator = load_tiff_images("./test_data/tiff_images")
        for img_obj in img_iterator:
            self.assertIsInstance(img_obj, Image.Image)

    # testing image cropper functions
    def test_cropping(self) -> None:
        """Positive test that checks for a List[ImageCropSelection]."""

        # loading image
        loaded_imgs = load_tiff_images("./test_data/tiff_images/")

        # setting image crop size
        width, height = (256, 256)

        # cropping all images

        # checking if every image cropped respects the size and objects
        for loaded_img in loaded_imgs:

            # applying crop walk to image and check types
            cropped_cords = image_crop_walk(loaded_img, width, height)
            self.assertIsInstance(cropped_cords, list)

            # iterating all cropped objects and check type and size
            for selection in cropped_cords:
                self.assertIsInstance(selection, ImageCropSelection)
