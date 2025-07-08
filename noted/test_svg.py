#!/usr/bin/env python3
"""
Quick SVG validator to check if notepwa.svg is well-formed XML
"""

import xml.etree.ElementTree as ET
import sys


def validate_svg(filename='notepwa.svg'):
    """Validate SVG file for XML well-formedness"""
    try:
        print(f"🔍 Validating {filename}...")

        # Try to parse the XML
        tree = ET.parse(filename)
        root = tree.getroot()

        print("✅ SVG file is well-formed XML!")
        print(f"📋 Root element: {root.tag}")
        print(f"📐 Viewbox: {root.get('viewBox', 'Not specified')}")

        # Count elements
        elements = list(root.iter())
        print(f"📊 Total elements: {len(elements)}")

        # Check for script tag
        scripts = root.findall('.//{http://www.w3.org/2000/svg}script')
        if scripts:
            print(f"📜 Found {len(scripts)} script element(s)")

        return True

    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        print(f"   Line {e.lineno}, Column {e.offset}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'notepwa.svg'

    if validate_svg(filename):
        print("\n🎉 SVG validation passed!")
        print("   The file should work correctly with Python server.")
    else:
        print("\n💥 SVG validation failed!")
        print("   Please fix the XML syntax errors.")
        sys.exit(1)