# Example API Response for TeraBox File Download

This document shows example API responses for the TeraBox API, specifically for extracting raw file/download links from TeraBox share URLs.

## Test URL
```
https://terasharefile.com/s/1Bu86w3Ap-s5O6nsa2PRWQQ
```

## 1. URL Validation

**Request:**
```bash
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://terasharefile.com/s/1Bu86w3Ap-s5O6nsa2PRWQQ"}'
```

**Response:**
```json
{
  "success": true,
  "valid": true,
  "message": "Valid TeraBox URL"
}
```

## 2. Get Download Information

**Request:**
```bash
curl -X POST http://localhost:5000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://terasharefile.com/s/1Bu86w3Ap-s5O6nsa2PRWQQ"}'
```

**Successful Response Example:**
```json
{
  "success": true,
  "surl": "1Bu86w3Ap-s5O6nsa2PRWQQ",
  "original_url": "https://terasharefile.com/s/1Bu86w3Ap-s5O6nsa2PRWQQ",
  "files": [
    {
      "filename": "example_video.mp4",
      "size": 52428800,
      "fs_id": "123456789",
      "path": "/example_video.mp4",
      "isdir": 0,
      "category": 1,
      "download_link": "https://d2.terabox.com/file/abc123xyz...?fid=123&rt=sh&sign=FDTAER...",
      "thumbnail": "https://data.terabox.com/thumbnail/abc123..."
    }
  ],
  "share_info": {
    "shareid": "987654321",
    "uk": "123456789"
  },
  "message": "Successfully extracted 1 file(s)"
}
```

## Field Descriptions

### Root Level Fields
- `success` (boolean): Indicates if the request was successful
- `surl` (string): Short URL identifier extracted from the share link
- `original_url` (string): The original URL that was submitted
- `files` (array): Array of file objects contained in the share
- `share_info` (object): Information about the share
- `message` (string): Human-readable message describing the result

### File Object Fields
- `filename` (string): Name of the file
- `size` (integer): File size in bytes
- `fs_id` (string): File system identifier
- `path` (string): Path of the file in the share
- `isdir` (integer): 0 for file, 1 for directory
- `category` (integer): File category (1 for video, 2 for audio, 3 for image, etc.)
- `download_link` (string): Direct download URL for the file (if available)
- `thumbnail` (string): Thumbnail URL for media files (if available)

### Share Info Fields
- `shareid` (string): Unique identifier for the share
- `uk` (string): User key associated with the share

## Error Response Examples

### Invalid URL
```json
{
  "success": false,
  "error": "Invalid TeraBox URL provided"
}
```

### Network Error (in sandboxed environments)
```json
{
  "success": false,
  "error": "Network error: HTTPSConnectionPool(host='www.terabox.com', port=443): Max retries exceeded..."
}
```

### TeraBox API Error
```json
{
  "success": false,
  "error": "TeraBox API error: Share not found",
  "errno": -9
}
```

### No Files Found
```json
{
  "success": false,
  "error": "No files found in the shared link"
}
```

## Notes

1. **Network Requirements**: The API requires external network access to communicate with TeraBox servers. In restricted/sandboxed environments, network errors are expected.

2. **Rate Limiting**: TeraBox may implement rate limiting on their API endpoints. Consider implementing caching or rate limiting on your side.

3. **Authentication**: The current implementation uses the public TeraBox API which doesn't require authentication for shared links.

4. **File Categories**:
   - 0: Other
   - 1: Video
   - 2: Audio
   - 3: Image
   - 4: Document
   - 5: Application
   - 6: Other

5. **Download Links**: The `download_link` field contains a direct, temporary URL that can be used to download the file. These links typically have an expiration time.

6. **Multiple Files**: If a share contains multiple files or folders, all will be listed in the `files` array.
