#!/usr/bin/env python3
import boto3
import json
import time
import os

def setup_s3_bucket():
    """Set up S3 bucket and upload ld_cache.json"""
    
    # Configure boto3 to use LocalStack
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:4566',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )
    
    bucket_name = 'ld-cache-bucket'
    
    # Create bucket
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Created bucket: {bucket_name}")
    except Exception as e:
        print(f"Bucket creation error (might already exist): {e}")

    # Upload ld_cache.json to S3
    try:
        s3_client.upload_file('ld_cache.json', bucket_name, 'all')
        print(f"Uploaded ld_cache.json to s3://{bucket_name}/all")
    except Exception as e:
        print(f"Upload error: {e}")

if __name__ == "__main__":
    print("Waiting for LocalStack to be ready...")
    time.sleep(5)  # Give LocalStack time to start
    setup_s3_bucket()
