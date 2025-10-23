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
        r'https?://(?:www\.)?terasharefile\.com/',
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
        
        surl = file_info['surl']
        
        # Fetch file metadata from TeraBox API
        # TeraBox uses a public API endpoint for shared files
        api_url = "https://www.terabox.com/share/list"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': url,
        }
        
        params = {
            'shorturl': surl,
            'root': '1',
            'page': '1',
            'num': '20',
            'web': '1',
            'channel': 'dubox',
            'app_id': '250528',
            'jsToken': '',
        }
        
        logger.info(f"Fetching file metadata for surl: {surl}")
        response = requests.get(api_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if the response is successful
        if data.get('errno') != 0:
            error_msg = data.get('errmsg', 'Unknown error from TeraBox API')
            logger.error(f"TeraBox API error: {error_msg}")
            return {
                'success': False,
                'error': f'TeraBox API error: {error_msg}',
                'errno': data.get('errno')
            }
        
        # Extract file list
        file_list = data.get('list', [])
        
        if not file_list:
            return {
                'success': False,
                'error': 'No files found in the shared link'
            }
        
        # Process files and extract download information
        files = []
        for file_item in file_list:
            file_data = {
                'filename': file_item.get('server_filename', 'Unknown'),
                'size': file_item.get('size', 0),
                'fs_id': file_item.get('fs_id'),
                'path': file_item.get('path', ''),
                'isdir': file_item.get('isdir', 0),
                'category': file_item.get('category', 0),
            }
            
            # Add download link if available
            if file_item.get('dlink'):
                file_data['download_link'] = file_item['dlink']
            
            # Add thumbnail for images/videos
            if file_item.get('thumbs'):
                file_data['thumbnail'] = file_item['thumbs'].get('url3', '')
            
            files.append(file_data)
        
        return {
            'success': True,
            'surl': surl,
            'original_url': url,
            'files': files,
            'share_info': {
                'shareid': data.get('shareid'),
                'uk': data.get('uk'),
            },
            'message': f'Successfully extracted {len(files)} file(s)'
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error getting download link: {str(e)}")
        return {
            'success': False,
            'error': f'Network error: {str(e)}'
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
