from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import re
import os
import tempfile
from urllib.parse import urlparse, parse_qs
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_terabox_url(url):
    """
    Validate if the provided URL is a valid TeraBox URL.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url:
        return False
    
    # TeraBox URL patterns
    terabox_patterns = [
        r'https?://(?:www\.)?terabox\.com/',
        r'https?://(?:www\.)?teraboxapp\.com/',
        r'https?://(?:www\.)?1024terabox\.com/',
        r'https?://(?:www\.)?4funbox\.com/',
    ]
    
    for pattern in terabox_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    
    return False


def extract_file_info(url):
    """
    Extract file information from TeraBox URL.
    
    Args:
        url (str): TeraBox URL
        
    Returns:
        dict: File information including surl and other parameters
    """
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        # Extract surl parameter (short URL identifier)
        surl = query_params.get('surl', [None])[0]
        
        if not surl:
            # Try to extract from path
            path_match = re.search(r'/s/([a-zA-Z0-9_-]+)', parsed_url.path)
            if path_match:
                surl = path_match.group(1)
        
        return {
            'surl': surl,
            'url': url
        }
    except Exception as e:
        logger.error(f"Error extracting file info: {str(e)}")
        return None


def get_download_link(url):
    """
    Get the direct download link for a TeraBox file.
    
    Args:
        url (str): TeraBox URL
        
    Returns:
        dict: Download information including direct link and metadata
    """
    try:
        # Extract file information
        file_info = extract_file_info(url)
        
        if not file_info or not file_info.get('surl'):
            return {
                'success': False,
                'error': 'Could not extract file information from URL'
            }
        
        # For now, return the URL and file info
        # In a production environment, you would implement the actual TeraBox API integration
        # This would involve authenticating with TeraBox and getting the direct download link
        
        return {
            'success': True,
            'surl': file_info['surl'],
            'original_url': url,
            'message': 'File information extracted successfully'
        }
        
    except Exception as e:
        logger.error(f"Error getting download link: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information."""
    return jsonify({
        'name': 'TeraBox API',
        'version': '1.0.0',
        'description': 'RESTful API for downloading files from TeraBox',
        'endpoints': {
            '/': 'API information (GET)',
            '/api/download': 'Get download information (POST)',
            '/api/validate': 'Validate TeraBox URL (POST)',
            '/health': 'Health check (GET)'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    }), 200


@app.route('/api/validate', methods=['POST'])
def validate_url():
    """
    Validate a TeraBox URL.
    
    Expected JSON body:
    {
        "url": "https://terabox.com/..."
    }
    
    Returns:
        JSON response with validation result
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        url = data.get('url')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL parameter is required'
            }), 400
        
        is_valid = validate_terabox_url(url)
        
        if is_valid:
            return jsonify({
                'success': True,
                'valid': True,
                'message': 'Valid TeraBox URL'
            }), 200
        else:
            return jsonify({
                'success': True,
                'valid': False,
                'message': 'Invalid TeraBox URL'
            }), 200
            
    except Exception as e:
        logger.error(f"Error in validate_url: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/api/download', methods=['POST'])
def download_file():
    """
    Get download information for a TeraBox file.
    
    Expected JSON body:
    {
        "url": "https://terabox.com/..."
    }
    
    Returns:
        JSON response with download information
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        url = data.get('url')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL parameter is required'
            }), 400
        
        # Validate URL
        if not validate_terabox_url(url):
            return jsonify({
                'success': False,
                'error': 'Invalid TeraBox URL provided'
            }), 400
        
        # Get download link
        result = get_download_link(url)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in download_file: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
