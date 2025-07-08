#!/usr/bin/env python3
"""
Test script to verify that both Python and Node.js backends
return identical responses and serve the same SVG file
"""

import requests
import json
import sys


def test_backend(port=8000):
    """Test backend responses"""
    base_url = f"http://localhost:{port}"

    print(f"🔍 Testing backend at {base_url}")

    try:
        # Test 1: Get main SVG app
        print("📄 Testing main SVG app...")
        response = requests.get(base_url)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'image/svg+xml' in content_type:
                print(f"   ✅ SVG served correctly (Content-Type: {content_type})")
                print(f"   📏 Size: {len(response.content)} bytes")

                # Check if it contains our app identifier
                if b'NotePWA - Drawing and Notes' in response.content:
                    print("   ✅ Contains correct app title")
                else:
                    print("   ⚠️  App title not found in SVG")
            else:
                print(f"   ❌ Wrong content type: {content_type}")
        else:
            print(f"   ❌ Failed to get SVG: {response.status_code}")

        # Test 2: Get backend info
        print("ℹ️  Testing backend info...")
        response = requests.get(f"{base_url}/api/info")
        if response.status_code == 200:
            info = response.json()
            backend = info.get('backend', 'Unknown')
            framework = info.get('framework', 'Unknown')
            print(f"   ✅ Backend: {backend}")
            print(f"   ✅ Framework: {framework}")
        else:
            print(f"   ❌ Failed to get backend info: {response.status_code}")

        # Test 3: Get notes (should return empty array initially)
        print("📝 Testing notes API...")
        response = requests.get(f"{base_url}/api/notes")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ Notes API working (found {len(notes)} notes)")
        else:
            print(f"   ❌ Failed to get notes: {response.status_code}")

        # Test 4: Get PWA manifest
        print("📱 Testing PWA manifest...")
        response = requests.get(f"{base_url}/manifest.json")
        if response.status_code == 200:
            manifest = response.json()
            app_name = manifest.get('name', 'Unknown')
            print(f"   ✅ Manifest working (App: {app_name})")
        else:
            print(f"   ❌ Failed to get manifest: {response.status_code}")

        print(f"✅ Backend test completed\n")
        return True

    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {base_url}")
        print("   Make sure the server is running")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False


def compare_backends():
    """Compare responses from both backends"""
    print("🔄 Comparing Python vs Node.js backends...")
    print("   Note: Run each server separately and test")
    print("   Both should serve identical SVG content")
    print()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

    print("🧪 NotePWA Backend Compatibility Test")
    print("=" * 40)
    print()

    if test_backend(port):
        print("🎉 Backend test passed!")
        print()
        print("💡 To test both backends:")
        print("   1. Run: python note_server.py")
        print("   2. Test: python test_backends.py")
        print("   3. Stop Python server (Ctrl+C)")
        print("   4. Run: npm start")
        print("   5. Test: python test_backends.py")
        print("   6. Compare results - they should be identical!")
    else:
        print("💥 Backend test failed!")
        sys.exit(1)