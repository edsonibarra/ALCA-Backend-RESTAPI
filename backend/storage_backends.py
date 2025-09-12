import boto3
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class PrivateMediaStorage(S3Boto3Storage):
    """
    Custom S3 storage backend for private media files.
    Files uploaded with this storage will be private and require signed URLs to access.
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False  # Don't use custom domain for private files
    querystring_auth = True  # Enable query string authentication
    querystring_expire = 3600  # URLs expire in 1 hour
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure files are private by default
        self.default_acl = 'private'


class S3ImageService:
    """
    Service class to handle S3 operations for property images
    """
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    def generate_presigned_url(self, object_key, expiration=3600):
        """
        Generate a presigned URL for a private S3 object
        
        Args:
            object_key (str): The S3 object key (file path)
            expiration (int): Time in seconds for the URL to remain valid (default: 1 hour)
        
        Returns:
            str: Presigned URL or None if error
        """
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logger.error(f"Error generating presigned URL for {object_key}: {e}")
            return None
    
    def upload_file(self, file_obj, object_key, content_type=None):
        """
        Upload a file to S3 with private ACL
        
        Args:
            file_obj: File object to upload
            object_key (str): The S3 object key (file path)
            content_type (str): MIME type of the file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            extra_args = {'ACL': 'private'}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_key,
                ExtraArgs=extra_args
            )
            return True
        except ClientError as e:
            logger.error(f"Error uploading file {object_key}: {e}")
            return False
    
    def delete_file(self, object_key):
        """
        Delete a file from S3
        
        Args:
            object_key (str): The S3 object key (file path)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except ClientError as e:
            logger.error(f"Error deleting file {object_key}: {e}")
            return False
    
    def file_exists(self, object_key):
        """
        Check if a file exists in S3
        
        Args:
            object_key (str): The S3 object key (file path)
        
        Returns:
            bool: True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except ClientError:
            return False