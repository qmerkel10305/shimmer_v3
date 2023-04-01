from dataclasses import dataclass

import numpy as np


@dataclass
class Camera:
    """
    Dataclass representing a camera object, used to store information about certain images.

    Attributes:
        make (str):
            The make of the camera
        model (str):
            The model of the camera
        lens (str):
            The lens the camera is using
        hfov (float):
            The horizontal fov of the camera with the specified lens
        vfov (float):
            The vertical fov of the camera with the specified lens
        camera_matrix (np.ndarray):
            A matrix representing the camera
        distortion_coefficients (np.ndarray):
            Input vector of distortion coefficients

        See UndistoredPoints (https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga55c716492470bfe86b0ee9bf3a1f0f7e)
        for more information about camera_matrix and distortion_coefficients
    """

    make: str
    model: str
    lens: str
    hfov: float
    vfov: float
    camera_matrix: np.ndarray = None
    distortion_coefficients: np.ndarray = None


LUCID_PHOENIX_8MM = Camera(
    make="Lucid", model="PHX200S", lens="Computar 1.1' 8 mm F2.8", hfov=83, vfov=66
)

LUCID_PHOENIX_12MM = Camera(
    make="Lucid", model="PHX200S", lens="Computar 1.1' 12 mm F2.8", hfov=60.5, vfov=46.2
)

LUCID_PHOENIX_16MM = Camera(
    make="Lucid", model="PHX200S", lens="Computar 1.1' 16 mm F2.8", hfov=48.2, vfov=36.2
)
