import unittest
import json
from app import app, validate_terabox_url, extract_file_info


class TestTeraBoxAPI(unittest.TestCase):
    """Test suite for TeraBox API"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_endpoint(self):
        """Test home endpoint returns API information"""
        response = self.app.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'TeraBox API')
        self.assertEqual(data['version'], '1.0.0')
        self.assertIn('endpoints', data)

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')

    def test_validate_url_valid(self):
        """Test URL validation with valid TeraBox URL"""
        response = self.app.post(
            '/api/validate',
            data=json.dumps({'url': 'https://terabox.com/s/test123'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['valid'])

    def test_validate_url_invalid(self):
        """Test URL validation with invalid URL"""
        response = self.app.post(
            '/api/validate',
            data=json.dumps({'url': 'https://google.com'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(data['valid'])

    def test_validate_url_missing_parameter(self):
        """Test URL validation without URL parameter"""
        response = self.app.post(
            '/api/validate',
            data=json.dumps({}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    def test_download_valid_url(self):
        """Test download endpoint with valid TeraBox URL"""
        response = self.app.post(
            '/api/download',
            data=json.dumps({'url': 'https://terabox.com/s/test123'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        # Since network access may be blocked in test environment,
        # we accept either success (200) or network error (400)
        self.assertIn(response.status_code, [200, 400])
        
        # If successful, check for expected fields
        if response.status_code == 200:
            self.assertTrue(data['success'])
            self.assertIn('surl', data)
        # If network error, verify it's a proper error response
        else:
            self.assertFalse(data['success'])
            self.assertIn('error', data)

    def test_download_invalid_url(self):
        """Test download endpoint with invalid URL"""
        response = self.app.post(
            '/api/download',
            data=json.dumps({'url': 'https://google.com'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_download_missing_parameter(self):
        """Test download endpoint without URL parameter"""
        response = self.app.post(
            '/api/download',
            data=json.dumps({}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_method_not_allowed(self):
        """Test wrong HTTP method"""
        response = self.app.get('/api/download')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])

    def test_endpoint_not_found(self):
        """Test non-existent endpoint"""
        response = self.app.get('/nonexistent')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_validate_terabox_url_function(self):
        """Test validate_terabox_url function directly"""
        # Valid URLs
        self.assertTrue(validate_terabox_url('https://terabox.com/s/test'))
        self.assertTrue(validate_terabox_url('https://www.terabox.com/s/test'))
        self.assertTrue(validate_terabox_url('https://teraboxapp.com/s/test'))
        self.assertTrue(validate_terabox_url('https://1024terabox.com/s/test'))
        self.assertTrue(validate_terabox_url('https://4funbox.com/s/test'))
        self.assertTrue(validate_terabox_url('https://terasharefile.com/s/test'))
        self.assertTrue(validate_terabox_url('https://www.terasharefile.com/s/test'))
        
        # Invalid URLs
        self.assertFalse(validate_terabox_url('https://google.com'))
        self.assertFalse(validate_terabox_url('https://example.com'))
        self.assertFalse(validate_terabox_url(''))
        self.assertFalse(validate_terabox_url(None))

    def test_extract_file_info_function(self):
        """Test extract_file_info function directly"""
        # Test with path-based URL
        info = extract_file_info('https://terabox.com/s/test123')
        self.assertIsNotNone(info)
        self.assertEqual(info['surl'], 'test123')
        
        # Test with query parameter URL
        info = extract_file_info('https://terabox.com/sharing/link?surl=test456')
        self.assertIsNotNone(info)
        self.assertEqual(info['surl'], 'test456')


if __name__ == '__main__':
    unittest.main()
