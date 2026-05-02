#!/usr/bin/env python3
"""
Script to automatically convert hardcoded pixel coordinates in Python files to percentages.
Base resolution: 1080x2460
"""

BASE_WIDTH = 1080
BASE_HEIGHT = 2460

# Coordinate conversion table
COORDS_TO_CONVERT = {
    # core/change_player.py
    "100, 170": (100 / BASE_WIDTH * 100, 170 / BASE_HEIGHT * 100),
    "550, 1800": (550 / BASE_WIDTH * 100, 1800 / BASE_HEIGHT * 100),
    "550, 400": (550 / BASE_WIDTH * 100, 400 / BASE_HEIGHT * 100),
    
    # core/fsm.py
    "50, 150": (50 / BASE_WIDTH * 100, 150 / BASE_HEIGHT * 100),
    
    # usecases/arena.py
    "883, 815": (883 / BASE_WIDTH * 100, 815 / BASE_HEIGHT * 100),
    "986, 920": (986 / BASE_WIDTH * 100, 920 / BASE_HEIGHT * 100),
    "883, 1007": (883 / BASE_WIDTH * 100, 1007 / BASE_HEIGHT * 100),
    "986, 1112": (986 / BASE_WIDTH * 100, 1112 / BASE_HEIGHT * 100),
    "883, 1200": (883 / BASE_WIDTH * 100, 1200 / BASE_HEIGHT * 100),
    "986, 1305": (986 / BASE_WIDTH * 100, 1305 / BASE_HEIGHT * 100),
    "883, 1392": (883 / BASE_WIDTH * 100, 1392 / BASE_HEIGHT * 100),
    "986, 1497": (986 / BASE_WIDTH * 100, 1497 / BASE_HEIGHT * 100),
    "883, 1585": (883 / BASE_WIDTH * 100, 1585 / BASE_HEIGHT * 100),
    "986, 1690": (986 / BASE_WIDTH * 100, 1690 / BASE_HEIGHT * 100),
    "550, 1400": (550 / BASE_WIDTH * 100, 1400 / BASE_HEIGHT * 100),
    "550, 940": (550 / BASE_WIDTH * 100, 940 / BASE_HEIGHT * 100),
    
    # usecases/labyrinth.py
    "550, 2000": (550 / BASE_WIDTH * 100, 2000 / BASE_HEIGHT * 100),
    
    # usecases/training_troops.py
    "4, 1103": (4 / BASE_WIDTH * 100, 1103 / BASE_HEIGHT * 100),
    "540, 1200": (540 / BASE_WIDTH * 100, 1200 / BASE_HEIGHT * 100),
    "540, 1230": (540 / BASE_WIDTH * 100, 1230 / BASE_HEIGHT * 100),
    "550, 1100": (550 / BASE_WIDTH * 100, 1100 / BASE_HEIGHT * 100),
    
    # usecases/collect.py
    "680, 1104": (680 / BASE_WIDTH * 100, 1104 / BASE_HEIGHT * 100),
    "550, 1240": (550 / BASE_WIDTH * 100, 1240 / BASE_HEIGHT * 100),
    "350, 1600": (350 / BASE_WIDTH * 100, 1600 / BASE_HEIGHT * 100),
    "350, 800": (350 / BASE_WIDTH * 100, 800 / BASE_HEIGHT * 100),
    "110, 950": (110 / BASE_WIDTH * 100, 950 / BASE_HEIGHT * 100),
    "600, 1250": (600 / BASE_WIDTH * 100, 1250 / BASE_HEIGHT * 100),
    
    # usecases/gather.py
    "910, 2120": (910 / BASE_WIDTH * 100, 2120 / BASE_HEIGHT * 100),
    "1000, 1920": (1000 / BASE_WIDTH * 100, 1920 / BASE_HEIGHT * 100),
    "0, 1920": (0 / BASE_WIDTH * 100, 1920 / BASE_HEIGHT * 100),
    
    # usecases/pet.py
    "560, 1540": (560 / BASE_WIDTH * 100, 1540 / BASE_HEIGHT * 100),
    
    # usecases/intel.py
    "860, 1740": (860 / BASE_WIDTH * 100, 1740 / BASE_HEIGHT * 100),
    
    # usecases/alliance.py
    
    # Main/main.py
}

# Box conversion table (x1, y1, x2, y2)
BOXES_TO_CONVERT = {
    # usecases/arena.py
    "[0, 1960, 1080, 2100]": ([0 / BASE_WIDTH * 100, 1960 / BASE_HEIGHT * 100, 1080 / BASE_WIDTH * 100, 2100 / BASE_HEIGHT * 100]),
    "[0, 460, 1080, 1950]": ([0 / BASE_WIDTH * 100, 460 / BASE_HEIGHT * 100, 1080 / BASE_WIDTH * 100, 1950 / BASE_HEIGHT * 100]),
    "[220, 815, 986, 1690]": ([220 / BASE_WIDTH * 100, 815 / BASE_HEIGHT * 100, 986 / BASE_WIDTH * 100, 1690 / BASE_HEIGHT * 100]),
    "[300, 1725, 665, 1830]": ([300 / BASE_WIDTH * 100, 1725 / BASE_HEIGHT * 100, 665 / BASE_WIDTH * 100, 1830 / BASE_HEIGHT * 100]),
    
    # usecases/training_troops.py
    "[0, 690, 670, 1650]": ([0 / BASE_WIDTH * 100, 690 / BASE_HEIGHT * 100, 670 / BASE_WIDTH * 100, 1650 / BASE_HEIGHT * 100]),
    "[250, 1400, 930, 1800]": ([250 / BASE_WIDTH * 100, 1400 / BASE_HEIGHT * 100, 930 / BASE_WIDTH * 100, 1800 / BASE_HEIGHT * 100]),
    
    # usecases/collect.py
    "[60, 355, 1050, 400]": ([60 / BASE_WIDTH * 100, 355 / BASE_HEIGHT * 100, 1050 / BASE_WIDTH * 100, 400 / BASE_HEIGHT * 100]),
    "[0, 0, 1080, 1080]": ([0 / BASE_WIDTH * 100, 0 / BASE_HEIGHT * 100, 1080 / BASE_WIDTH * 100, 1080 / BASE_HEIGHT * 100]),
    
    # usecases/pet.py
    "[0, 400, 1080, 2200]": ([0 / BASE_WIDTH * 100, 400 / BASE_HEIGHT * 100, 1080 / BASE_WIDTH * 100, 2200 / BASE_HEIGHT * 100]),
    
    # usecases/gather.py
    "[0, 1940, 1080, 1980]": ([0 / BASE_WIDTH * 100, 1940 / BASE_HEIGHT * 100, 1080 / BASE_WIDTH * 100, 1980 / BASE_HEIGHT * 100]),
    "[300, 500, 400, 650]": ([300 / BASE_WIDTH * 100, 500 / BASE_HEIGHT * 100, 400 / BASE_WIDTH * 100, 650 / BASE_HEIGHT * 100]),
}

def format_coords(x, y):
    """Format coordinates with appropriate precision."""
    return f"{round(x, 2)}, {round(y, 2)}"

def format_box(box):
    """Format box coordinates."""
    return f"[{round(box[0], 2)}, {round(box[1], 2)}, {round(box[2], 2)}, {round(box[3], 2)}]"

print("Coordinate Conversion Reference Table")
print("=" * 80)
print("\nPixel → Percentage Conversions (x, y) format:")
print("-" * 80)
for pixel_coord, pct_coord in COORDS_TO_CONVERT.items():
    print(f"  {pixel_coord:20} → {format_coords(pct_coord[0], pct_coord[1])}")

print("\n\nBox Conversions [x1, y1, x2, y2] format:")
print("-" * 80)
for pixel_box, pct_box in BOXES_TO_CONVERT.items():
    print(f"  {pixel_box:30} → {format_box(pct_box)}")

# Generate replacement commands for reference
print("\n\n" + "=" * 80)
print("Use these conversions as reference for updating code files manually or via scripts")
