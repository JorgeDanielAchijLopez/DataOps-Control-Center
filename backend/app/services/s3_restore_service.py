import os
import boto3


def download_backup_from_s3(file_name):

    bucket = os.getenv(
        "AWS_BUCKET"
    )

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv(
            "AWS_ACCESS_KEY_ID"
        ),
        aws_secret_access_key=os.getenv(
            "AWS_SECRET_ACCESS_KEY"
        ),
        region_name=os.getenv(
            "AWS_REGION"
        )
    )

    os.makedirs(
        "restored_backups",
        exist_ok=True
    )

    local_path = (
        f"restored_backups/{file_name}"
    )

    s3.download_file(
        bucket,
        f"backups/{file_name}",
        local_path
    )

    return local_path