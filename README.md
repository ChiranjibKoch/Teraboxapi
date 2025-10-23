# TeraBox API

A RESTful API for downloading files from TeraBox URLs. This API provides endpoints to validate TeraBox URLs and retrieve download information.

## Features

- ✅ URL validation for TeraBox links
- ✅ RESTful API endpoints
- ✅ Comprehensive error handling
- ✅ CORS support for web applications
- ✅ Ready for Heroku deployment
- ✅ Health check endpoint

## API Endpoints

### 1. Home / API Information
```
GET /
```
Returns API information and available endpoints.

**Response:**
```json
{
  "name": "TeraBox API",
  "version": "1.0.0",
  "description": "RESTful API for downloading files from TeraBox",
  "endpoints": {
    "/": "API information (GET)",
    "/api/download": "Get download information (POST)",
    "/api/validate": "Validate TeraBox URL (POST)",
    "/health": "Health check (GET)"
  }
}
```

### 2. Health Check
```
GET /health
```
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### 3. Validate URL
```
POST /api/validate
```
Validate if a URL is a valid TeraBox URL.

**Request Body:**
```json
{
  "url": "https://terabox.com/s/1xxxxxxx"
}
```

**Response (Valid):**
```json
{
  "success": true,
  "valid": true,
  "message": "Valid TeraBox URL"
}
```

**Response (Invalid):**
```json
{
  "success": true,
  "valid": false,
  "message": "Invalid TeraBox URL"
}
```

### 4. Get Download Information
```
POST /api/download
```
Get download information for a TeraBox file.

**Request Body:**
```json
{
  "url": "https://terabox.com/s/1xxxxxxx"
}
```

**Response (Success):**
```json
{
  "success": true,
  "surl": "1xxxxxxx",
  "original_url": "https://terabox.com/s/1xxxxxxx",
  "files": [
    {
      "filename": "example_video.mp4",
      "size": 123456789,
      "fs_id": "123456",
      "path": "/example_video.mp4",
      "isdir": 0,
      "category": 1,
      "download_link": "https://...",
      "thumbnail": "https://..."
    }
  ],
  "share_info": {
    "shareid": "12345",
    "uk": "67890"
  },
  "message": "Successfully extracted 1 file(s)"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Invalid TeraBox URL provided"
}
```

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/ChiranjibKoch/Teraboxapi.git
cd Teraboxapi
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Heroku Deployment

1. Install the Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Deploy to Heroku:
```bash
git push heroku main
```

4. Open your app:
```bash
heroku open
```

## Usage Examples

### cURL

**Validate URL:**
```bash
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://terabox.com/s/1xxxxxxx"}'
```

**Get Download Information:**
```bash
curl -X POST http://localhost:5000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://terabox.com/s/1xxxxxxx"}'
```

### Python

```python
import requests

# Validate URL
response = requests.post(
    'http://localhost:5000/api/validate',
    json={'url': 'https://terabox.com/s/1xxxxxxx'}
)
print(response.json())

# Get download information
response = requests.post(
    'http://localhost:5000/api/download',
    json={'url': 'https://terabox.com/s/1xxxxxxx'}
)
print(response.json())
```

### JavaScript (Fetch API)

```javascript
// Validate URL
fetch('http://localhost:5000/api/validate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://terabox.com/s/1xxxxxxx'
  })
})
.then(response => response.json())
.then(data => console.log(data));

// Get download information
fetch('http://localhost:5000/api/download', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://terabox.com/s/1xxxxxxx'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Supported TeraBox URL Formats

The API supports the following TeraBox URL formats:
- `https://terabox.com/...`
- `https://www.terabox.com/...`
- `https://teraboxapp.com/...`
- `https://www.teraboxapp.com/...`
- `https://1024terabox.com/...`
- `https://4funbox.com/...`
- `https://terasharefile.com/...`
- `https://www.terasharefile.com/...`

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input or missing parameters
- **404 Not Found**: Endpoint doesn't exist
- **405 Method Not Allowed**: Wrong HTTP method used
- **500 Internal Server Error**: Server-side error

All errors return a JSON response with the following format:
```json
{
  "success": false,
  "error": "Error message description"
}
```

## Environment Variables

- `PORT`: Port number for the server (default: 5000)

## Technologies Used

- **Flask**: Web framework
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Gunicorn**: WSGI HTTP Server for production
- **Requests**: HTTP library for making requests

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please create an issue in the GitHub repository.