# scripts/download_data.py
import boto3
import os
from pathlib import Path

def download_from_s3(prefix: str, local_dir: str):
    """Télécharge les données depuis S3 vers le dossier local."""
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ.get('AWS_REGION', 'eu-west-3'),
    )
    bucket = 'afrinutri-data-lake'
    Path(local_dir).mkdir(parents=True, exist_ok=True)

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in response.get('Contents', []):
        key      = obj['Key']
        filename = key.replace(prefix, '', 1).lstrip('/')
        dest     = Path(local_dir) / filename
        dest.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(bucket, key, str(dest))
        print(f"  ↓ {key}")

if __name__ == '__main__':
    print("Téléchargement des images raw...")
    download_from_s3('datasets/raw/', 'data/raw/images/')

    print("Téléchargement des embeddings...")
    download_from_s3('embeddings/', 'data/processed/embeddings/')