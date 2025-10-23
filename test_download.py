#!/usr/bin/env python3
"""
Test script to demonstrate TeraBox file download link extraction
This script tests the new functionality with the provided URL.

Usage:
    python test_download.py
"""

import requests
import json
import sys

def test_terabox_download():
    """Test the TeraBox API with the provided URL"""
    
    # URL from the problem statement
    test_url = "https://terasharefile.com/s/1Bu86w3Ap-s5O6nsa2PRWQQ"
    
    # API endpoint (use environment-specific URL)
    api_url = "http://localhost:5000/api/download"
    
    print("=" * 70)
    print("TeraBox File Download Link Extraction Test")
    print("=" * 70)
    print(f"\nTest URL: {test_url}")
    print(f"API Endpoint: {api_url}")
    print("\n" + "-" * 70)
    
    # First, validate the URL
    print("\n1. Validating URL...")
    try:
        response = requests.post(
            "http://localhost:5000/api/validate",
            json={"url": test_url},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        result = response.json()
        print(json.dumps(result, indent=2))
        
        if not result.get('valid'):
            print("\n❌ URL validation failed!")
            return
        print("\n✅ URL is valid!")
    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        return
    
    # Now get the download information
    print("\n" + "-" * 70)
    print("\n2. Fetching download information...")
    try:
        response = requests.post(
            api_url,
            json={"url": test_url},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        result = response.json()
        
        print(json.dumps(result, indent=2))
        
        if result.get('success'):
            print("\n✅ Successfully extracted file information!")
            
            # Display file details
            files = result.get('files', [])
            if files:
                print(f"\n📁 Found {len(files)} file(s):")
                for i, file_item in enumerate(files, 1):
                    print(f"\n  File {i}:")
                    print(f"    - Name: {file_item.get('filename', 'N/A')}")
                    print(f"    - Size: {file_item.get('size', 0):,} bytes")
                    print(f"    - Path: {file_item.get('path', 'N/A')}")
                    if file_item.get('download_link'):
                        print(f"    - Download Link: {file_item['download_link'][:60]}...")
                    if file_item.get('thumbnail'):
                        print(f"    - Thumbnail: {file_item['thumbnail'][:60]}...")
            
            # Display share info
            share_info = result.get('share_info', {})
            if share_info:
                print(f"\n📋 Share Information:")
                print(f"    - Share ID: {share_info.get('shareid', 'N/A')}")
                print(f"    - UK: {share_info.get('uk', 'N/A')}")
        else:
            print(f"\n❌ Failed to extract file information:")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️  Cannot connect to API server.")
        print("   Make sure the Flask server is running:")
        print("   python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_terabox_download()
