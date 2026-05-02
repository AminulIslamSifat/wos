#!/usr/bin/env python3
"""
Script to convert all TextArea JSON files from pixel coordinates to percentage-based coordinates.
Base resolution: 1080x2460
"""

import json
import os
from pathlib import Path
from core.coord_utils import box_pixel_to_percent, round_percentages

TEXTAREA_DIR = Path(__file__).parent / "references" / "TextArea"
BASE_WIDTH = 1080
BASE_HEIGHT = 2460


def convert_textarea_file(file_path: Path) -> dict:
    """Convert a single TextArea JSON file from pixels to percentages."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    converted = {}
    for key, value in data.items():
        new_value = dict(value)
        
        # Convert box coordinates if they exist
        if "box" in value and value["box"] is not None:
            box = value["box"]
            # Convert from pixels to percentages
            box_percent = box_pixel_to_percent(box)
            # Round to 2 decimal places for readability
            new_value["box"] = round_percentages(box_percent, decimals=2)
        
        converted[key] = new_value
    
    return converted


def convert_all_textarea_files():
    """Convert all TextArea JSON files."""
    if not TEXTAREA_DIR.exists():
        print(f"TextArea directory not found: {TEXTAREA_DIR}")
        return
    
    json_files = sorted(TEXTAREA_DIR.glob("*.json"))
    
    print(f"Found {len(json_files)} TextArea files to convert")
    print("-" * 60)
    
    for file_path in json_files:
        try:
            print(f"\nProcessing: {file_path.name}")
            converted_data = convert_textarea_file(file_path)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(converted_data, f, indent=4, ensure_ascii=False)
            
            print(f"✓ Converted: {file_path.name}")
            
            # Show a sample of conversions
            sample_items = list(converted_data.items())[:2]
            for item_key, item_value in sample_items:
                if "box" in item_value and item_value["box"]:
                    print(f"  {item_key}: {item_value['box']}")
        
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")
    
    print("\n" + "=" * 60)
    print("✓ All TextArea files converted to percentage-based coordinates")


if __name__ == "__main__":
    convert_all_textarea_files()
