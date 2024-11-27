import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region='us-east-1'):
    """Create an S3 bucket with the given name and region (default: us-east-1)."""
    try:
        # Initialize the S3 client with the specified region
        s3_client = boto3.client('s3', region_name=region)
        
        # Create the bucket with a location constraint (for regions other than us-east-1)
        if region == 'us-east-1':  # No location constraint needed for us-east-1
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        print(f"Bucket '{bucket_name}' created successfully in region '{region}'.")
        return True
    except ClientError as e:
        print(f"Error occurred: {e}")
        return False

if __name__ == "__main__":
    bucket_name = "music-app1999"  # Bucket name must be globally unique
    region = 'us-east-1'  # You can change this to any AWS region (e.g., 'us-west-2', 'eu-west-1')
    create_bucket(bucket_name, region)
