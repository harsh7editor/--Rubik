#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et

import numpy as np
import cv2
from helpers import ciede2000, bgr2lab
from config import config
from constants import CUBE_PALETTE, COLOR_PLACEHOLDER

class ColorDetection:

    def __init__(self):
        self.prominent_color_palette = {
            'red'   : (0, 0, 255),
            'orange': (0, 165, 255),
            'blue'  : (255, 0, 0),
            'green' : (0, 255, 0),
            'white' : (255, 255, 255),
            'yellow': (0, 255, 255)
        }

        # Load colors from config and convert the list -> tuple.
        self.cube_color_palette = config.get_setting(
            CUBE_PALETTE,
            self.prominent_color_palette
        )
        self.lab_color_palette = {}
        for side, bgr in self.cube_color_palette.items():
            self.cube_color_palette[side] = tuple(bgr)
            self.lab_color_palette[side] = bgr2lab(bgr)

    def get_prominent_color(self, bgr):
        """Get the prominent color equivalent of the given bgr color."""
        for color_name, color_bgr in self.cube_color_palette.items():
            if tuple([int(c) for c in bgr]) == color_bgr:
                return self.prominent_color_palette[color_name]
        return COLOR_PLACEHOLDER

    def get_dominant_color(self, roi):
        """
        Get dominant color from a certain region of interest.

        :param roi: The image list.
        :returns: tuple
        """
        return tuple(np.mean(roi, axis=(0, 1)))

    def get_closest_color(self, bgr):
        """
        Get the closest color of a BGR color using CIEDE2000 distance.

        :param bgr tuple: The BGR color to use.
        :returns: dict
        """
        lab = bgr2lab(bgr)
        distances = []
        for color_name, color_lab in self.lab_color_palette.items():
            distances.append({
                'color_name': color_name,
                'color_bgr': self.cube_color_palette[color_name],
                'distance': ciede2000(lab, color_lab)
            })
        closest = min(distances, key=lambda item: item['distance'])
        return closest

    def convert_bgr_to_notation(self, bgr):
        """
        Convert BGR tuple to rubik's cube notation.
        The BGR color must be normalized first by the get_closest_color method.

        :param bgr tuple: The BGR values to convert.
        :returns: str
        """
        notations = {
            'green' : 'F',
            'white' : 'U',
            'blue'  : 'B',
            'red'   : 'R',
            'orange': 'L',
            'yellow': 'D'
        }
        color_name = self.get_closest_color(bgr)['color_name']
        return notations[color_name]

    def set_cube_color_pallete(self, palette):
        """
        Set a new cube color palette. The palette is being used when the user is
        scanning his cube in solve mode by matching the scanned colors against
        this palette.
        """
        for side, bgr in palette.items():
            self.cube_color_palette[side] = tuple([int(c) for c in bgr])
            self.lab_color_palette[side] = bgr2lab(self.cube_color_palette[side])

color_detector = ColorDetection()
