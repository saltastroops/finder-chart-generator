import io
from pathlib import Path
from typing import Generator

import numpy as np
import pytest
from PIL import Image
from starlette.testclient import TestClient

from fcg.main import app


@pytest.fixture(scope="session", autouse=True)
def seed_random_number_generator():
    # We need to seed the random number generator as AstroPy uses random numbers, which
    # (without seeding) results in slightly different finder charts every time the tests
    # are run
    np.random.seed(0)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app=app)


@pytest.fixture()
def check_image(file_regression):
    """
    Return a function for checking an image against a previously stored version.

    Images may differ slightly because of comments added by Matplotlib. We therefore
    compare their data with the help of Pillow.

    Parameters
    ----------
    file_regression
    """

    def _compare_images(actual: Path, expected: Path) -> None:
        # Adapted from https://www.redshiftzero.com/pytest-image/
        img1 = Image.open(actual)
        img2 = Image.open(expected)

        sum_sq_diff = np.sum(
            (np.asarray(img1).astype("float") - np.asarray(img2).astype("float")) ** 2
        )

        if sum_sq_diff > 0:
            raise AssertionError("The image has changed.")

    def _check_image(image_contents: bytes):
        # Matplotlib adds a string with version information to the PNG. As this
        # leads to test failure if the previously stored finder chart was generated
        # with another Matplotlib version, we store the image with Pillow to get
        # rid of the string.
        file_regression.check(
            image_contents,
            binary=True,
            extension=".png",
            check_fn=_compare_images,
        )

    return _check_image
