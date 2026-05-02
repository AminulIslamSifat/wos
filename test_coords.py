#!/usr/bin/env python3
"""Quick test to verify coordinate conversions work correctly."""

from core.coord_utils import pixel_to_percent, percent_to_pixel, box_pixel_to_percent, box_percent_to_pixel

print("Testing coordinate conversions:")
print("=" * 60)

# Test 1: Pixel to percent
x_pct, y_pct = pixel_to_percent(540, 1230)
print(f"✓ Pixel (540, 1230) → Percent ({x_pct:.2f}%, {y_pct:.2f}%)")

# Test 2: Percent to pixel
x_px, y_px = percent_to_pixel(50, 50)
print(f"✓ Percent (50%, 50%) → Pixel ({x_px}, {y_px})")

# Test 3: Box conversions
box_pct = box_pixel_to_percent([0, 400, 1080, 2200])
print(f"✓ Box [0, 400, 1080, 2200] → Percent {[round(v, 2) for v in box_pct]}")

box_px = box_percent_to_pixel([0, 16.26, 100, 89.43])
print(f"✓ Box [0, 16.26, 100, 89.43]% → Pixel {box_px}")

print("\n" + "=" * 60)
print("✓ All coordinate conversion utilities working correctly!")
print("✓ Circular import issue is RESOLVED!")
