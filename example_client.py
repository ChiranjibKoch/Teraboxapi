#!/usr/bin/env python3
"""
Example client for TeraBox API
This script demonstrates how to use the TeraBox API endpoints.

Usage:
    python example_client.py                          # Uses http://localhost:5000
    python example_client.py --url https://api.url    # Uses specified URL
    export TERABOX_API_URL=https://api.url && python example_client.py
"""

import requests
import json
import sys
import argparse
import os


class TeraBoxAPIClient:
    """Client for interacting with TeraBox API"""
    
    def __init__(self, base_url="http://localhost:5000"):
        """
        Initialize the client.
        
        Args:
            base_url (str): Base URL of the API (default: http://localhost:5000)
        """
        self.base_url = base_url.rstrip('/')
        
    def get_api_info(self):
        """Get API information"""
        try:
            response = requests.get(f"{self.base_url}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def check_health(self):
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def validate_url(self, url):
        """
        Validate a TeraBox URL.
        
        Args:
            url (str): TeraBox URL to validate
            
        Returns:
            dict: Validation result
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/validate",
                json={"url": url},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_download_info(self, url):
        """
        Get download information for a TeraBox URL.
        
        Args:
            url (str): TeraBox URL
            
        Returns:
            dict: Download information
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/download",
                json={"url": url},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


def main():
    """Main function to demonstrate API usage"""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Example client for TeraBox API'
    )
    parser.add_argument(
        '--url',
        default=os.environ.get('TERABOX_API_URL', 'http://localhost:5000'),
        help='Base URL of the TeraBox API (default: http://localhost:5000 or TERABOX_API_URL env var)'
    )
    args = parser.parse_args()
    
    # Initialize client
    client = TeraBoxAPIClient(args.url)
    
    print("=" * 60)
    print("TeraBox API Client Example")
    print(f"API URL: {args.url}")
    print("=" * 60)
    
    # Get API info
    print("\n1. Getting API information...")
    api_info = client.get_api_info()
    print(json.dumps(api_info, indent=2))
    
    # Check health
    print("\n2. Checking API health...")
    health = client.check_health()
    print(json.dumps(health, indent=2))
    
    # Example TeraBox URL
    test_url = "https://terabox.com/s/1abc123"
    
    # Validate URL
    print(f"\n3. Validating URL: {test_url}")
    validation = client.validate_url(test_url)
    print(json.dumps(validation, indent=2))
    
    # Get download info
    print(f"\n4. Getting download information for: {test_url}")
    download_info = client.get_download_info(test_url)
    print(json.dumps(download_info, indent=2))
    
    # Test with invalid URL
    invalid_url = "https://google.com"
    print(f"\n5. Testing with invalid URL: {invalid_url}")
    validation = client.validate_url(invalid_url)
    print(json.dumps(validation, indent=2))
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
