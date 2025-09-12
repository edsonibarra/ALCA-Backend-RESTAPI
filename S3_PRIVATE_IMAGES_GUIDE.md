# S3 Private Images Implementation Guide

## Overview

This guide explains the implementation of private S3 bucket integration for property images in the ALCA Real Estate API. All property images are now stored in a private S3 bucket called "alca-inmo" and are only accessible through the application with proper authentication.

## Key Features

- **Private Storage**: All images are stored with private ACL in S3
- **Secure Access**: Images are only accessible through presigned URLs
- **Authentication Required**: All image operations require user authentication
- **Automatic URL Generation**: Secure URLs are automatically generated with configurable expiration
- **Generic Image Model**: Supports images for both HouseForSale and HouseForRent models

## Architecture Components

### 1. Custom Storage Backend (`backend/storage_backends.py`)

#### PrivateMediaStorage
- Extends `S3Boto3Storage` with private ACL settings
- Ensures all uploaded files are private by default
- Disables custom domain for private files

#### S3ImageService
- Handles S3 operations (upload, delete, presigned URLs)
- Provides methods for secure file management
- Includes error handling and logging

### 2. Updated Models (`property/models.py`)

#### PropertyImage Model
- Uses `PrivateMediaStorage` for the image field
- Includes `get_secure_url()` method for generating presigned URLs
- Enhanced upload path with unique identifiers and timestamps

#### Property Models (HouseForSale & HouseForRent)
- Both models now have `images` property for accessing related images
- Generic relationship allows flexible image association

### 3. Enhanced Serializers (`property/serializers.py`)

#### PropertyImageSerializer
- Provides both `image_url` (deprecated) and `secure_url` fields
- Automatically generates presigned URLs with configurable expiration
- Backward compatibility maintained

### 4. New ViewSet (`property/views.py`)

#### PropertyImageViewSet
- Complete CRUD operations for property images
- Secure URL generation endpoints
- Bulk upload functionality
- Image management features (set as main, etc.)

## API Endpoints

### Property Images

#### Base URL: `/api/property-images/`

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | List all images (filterable) | Required |
| POST | `/` | Create new image | Required |
| GET | `/{id}/` | Get specific image details | Required |
| PUT/PATCH | `/{id}/` | Update image | Required |
| DELETE | `/{id}/` | Delete image | Required |
| GET | `/{id}/secure_url/` | Get presigned URL | Required |
| GET | `/{id}/redirect_to_image/` | Redirect to image | Required |
| POST | `/bulk_upload/` | Upload multiple images | Required |
| PATCH | `/{id}/set_as_main/` | Set as main image | Required |

### House Image Upload

#### For Sale Properties
- **Endpoint**: `POST /api/houses-for-sale/{id}/upload_images/`
- **Content-Type**: `multipart/form-data`
- **Fields**: `images` (multiple files), `caption`, `is_main`, `order`

#### For Rent Properties
- **Endpoint**: `POST /api/houses-for-rent/{id}/upload_images/`
- **Content-Type**: `multipart/form-data`
- **Fields**: `images` (multiple files), `caption`, `is_main`, `order`

## Usage Examples

### 1. Upload Images to a Property

```bash
curl -X POST \
  http://localhost:8000/api/houses-for-sale/1/upload_images/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" \
  -F "caption=Beautiful living room" \
  -F "is_main=true"
```

### 2. Get Secure URL for an Image

```bash
curl -X GET \
  "http://localhost:8000/api/property-images/1/secure_url/?expiration=7200" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response:
```json
{
  "secure_url": "https://alca-inmo.s3.us-east-1.amazonaws.com/properties/...",
  "expires_in": 7200,
  "image_id": 1
}
```

### 3. Filter Images by Property

```bash
curl -X GET \
  "http://localhost:8000/api/property-images/?content_type=house_for_sale&object_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 4. Bulk Upload Images

```bash
curl -X POST \
  http://localhost:8000/api/property-images/bulk_upload/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" \
  -F "content_type=house_for_sale" \
  -F "object_id=1"
```

## Configuration

### Environment Variables (`.env`)

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=alca-inmo
AWS_S3_REGION_NAME=us-east-1
```

### Django Settings

Key settings in `backend/settings.py`:

```python
# S3 Configuration for private files
AWS_DEFAULT_ACL = 'private'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 3600  # 1 hour

# Use custom private storage backend
DEFAULT_FILE_STORAGE = "backend.storage_backends.PrivateMediaStorage"
```

## Security Features

### 1. Private ACL
- All images are uploaded with `private` ACL
- Direct S3 URLs are not accessible without authentication

### 2. Presigned URLs
- Temporary URLs with configurable expiration (default: 1 hour)
- URLs automatically expire for security

### 3. Authentication Required
- All image operations require JWT authentication
- Only authenticated users can access images

### 4. Unique File Names
- Files are renamed with timestamps and UUIDs to prevent conflicts
- Original filenames are preserved in the path structure

## File Organization

Images are organized in S3 with the following structure:

```
alca-inmo/
├── properties/
│   ├── houseforsale/
│   │   ├── {property_id}/
│   │   │   ├── 20250112_143022_a1b2c3d4.jpg
│   │   │   └── 20250112_143055_e5f6g7h8.png
│   └── houseforrent/
│       ├── {property_id}/
│       │   ├── 20250112_144022_i9j0k1l2.jpg
│       │   └── 20250112_144055_m3n4o5p6.png
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "No images provided"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 404 Not Found
```json
{
  "detail": "Not found."
}
```

#### 500 Internal Server Error
```json
{
  "error": "Could not generate secure URL"
}
```

## Migration Notes

### Database Changes
- Migration `0003_alter_propertyimage_image.py` updates the storage backend
- No data loss occurs during migration
- Existing images will use the new storage backend for new uploads

### Backward Compatibility
- `image_url` field is maintained for backward compatibility
- Both `image_url` and `secure_url` return presigned URLs
- Existing API clients will continue to work

## Best Practices

### 1. URL Expiration
- Use appropriate expiration times based on use case
- Default 1 hour is suitable for most applications
- Longer expiration for cached content, shorter for sensitive data

### 2. Error Handling
- Always check for null/empty secure URLs
- Implement retry logic for failed S3 operations
- Log errors for debugging

### 3. Performance
- Cache presigned URLs when possible (within expiration time)
- Use bulk operations for multiple images
- Consider CDN for frequently accessed images

### 4. Security
- Never expose AWS credentials in client-side code
- Regularly rotate AWS access keys
- Monitor S3 access logs for suspicious activity

## Troubleshooting

### Common Issues

#### 1. "Could not generate secure URL"
- Check AWS credentials in `.env` file
- Verify S3 bucket exists and is accessible
- Check AWS IAM permissions

#### 2. "Authentication credentials were not provided"
- Ensure JWT token is included in Authorization header
- Check token expiration and refresh if needed

#### 3. Images not uploading
- Verify file size limits (10MB default)
- Check file format (JPEG, PNG supported)
- Ensure proper multipart/form-data encoding

#### 4. S3 Access Denied
- Verify AWS credentials have proper S3 permissions
- Check bucket policy and IAM roles
- Ensure bucket name matches configuration

## Dependencies

### Required Python Packages
- `boto3==1.35.0` - AWS SDK for Python
- `django-storages==1.14.4` - Django storage backends
- `pillow==10.4.0` - Image processing

### AWS Permissions Required
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::alca-inmo/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::alca-inmo"
    }
  ]
}
```

## Support

For issues or questions regarding the S3 private images implementation, please refer to:
- Django documentation: https://docs.djangoproject.com/
- Django-storages documentation: https://django-storages.readthedocs.io/
- AWS S3 documentation: https://docs.aws.amazon.com/s3/