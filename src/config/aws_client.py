"""AWS service clients configuration"""

import boto3
from botocore.exceptions import ClientError
from src.config.settings import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AWSClientManager:
    """Manages AWS service clients"""
    
    def __init__(self):
        self._s3_client = None
        self._textract_client = None
    
    @property
    def s3(self):
        """Get or create S3 client"""
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )
        return self._s3_client
    
    @property
    def textract(self):
        """Get or create Textract client"""
        if self._textract_client is None:
            self._textract_client = boto3.client(
                'textract',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )
        return self._textract_client
    
    def upload_to_s3(self, file_content: bytes, key: str, 
                     content_type: Optional[str] = None) -> bool:
        """
        Upload file to S3 bucket
        
        Args:
            file_content: File content as bytes
            key: S3 object key (path)
            content_type: MIME type of the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3.put_object(
                Bucket=settings.s3_bucket_name,
                Key=key,
                Body=file_content,
                **extra_args
            )
            logger.info(f"Successfully uploaded {key} to S3")
            return True
        except ClientError as e:
            logger.error(f"Failed to upload {key} to S3: {e}")
            return False
    
    def download_from_s3(self, key: str) -> Optional[bytes]:
        """
        Download file from S3 bucket
        
        Args:
            key: S3 object key (path)
            
        Returns:
            File content as bytes, or None if failed
        """
        try:
            response = self.s3.get_object(
                Bucket=settings.s3_bucket_name,
                Key=key
            )
            return response['Body'].read()
        except ClientError as e:
            logger.error(f"Failed to download {key} from S3: {e}")
            return None
    
    def delete_from_s3(self, key: str) -> bool:
        """
        Delete file from S3 bucket
        
        Args:
            key: S3 object key (path)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3.delete_object(
                Bucket=settings.s3_bucket_name,
                Key=key
            )
            logger.info(f"Successfully deleted {key} from S3")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete {key} from S3: {e}")
            return False


# Global AWS client manager instance
aws_client = AWSClientManager()
