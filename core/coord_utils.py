"""
Coordinate conversion utilities for percentage-based screen coordinates.
Base resolution: 1080x2460 (100% = 1080 width, 100% = 2460 height)
"""

# Base resolution used for percentage calculations
BASE_WIDTH = 1080
BASE_HEIGHT = 2460


def pixel_to_percent(x: float, y: float) -> tuple[float, float]:
    """Convert pixel coordinates to percentage coordinates."""
    x_percent = (x / BASE_WIDTH) * 100
    y_percent = (y / BASE_HEIGHT) * 100
    return x_percent, y_percent


def percent_to_pixel(x_percent: float, y_percent: float, 
                     screen_width: int = BASE_WIDTH, 
                     screen_height: int = BASE_HEIGHT) -> tuple[int, int]:
    """Convert percentage coordinates to pixel coordinates."""
    x_pixel = int((x_percent / 100) * screen_width)
    y_pixel = int((y_percent / 100) * screen_height)
    return x_pixel, y_pixel


def box_pixel_to_percent(box: list[int]) -> list[float]:
    """Convert box [x1, y1, x2, y2] from pixels to percentages."""
    x1, y1, x2, y2 = box
    x1_p, y1_p = pixel_to_percent(x1, y1)
    x2_p, y2_p = pixel_to_percent(x2, y2)
    return [x1_p, y1_p, x2_p, y2_p]


def box_percent_to_pixel(box: list[float], 
                         screen_width: int = BASE_WIDTH,
                         screen_height: int = BASE_HEIGHT) -> list[int]:
    """Convert box [x1%, y1%, x2%, y2%] from percentages to pixels."""
    x1_p, y1_p, x2_p, y2_p = box
    x1, y1 = percent_to_pixel(x1_p, y1_p, screen_width, screen_height)
    x2, y2 = percent_to_pixel(x2_p, y2_p, screen_width, screen_height)
    return [x1, y1, x2, y2]


def round_percentages(box: list[float], decimals: int = 2) -> list[float]:
    """Round percentage values to specified decimal places."""
    return [round(v, decimals) for v in box]
