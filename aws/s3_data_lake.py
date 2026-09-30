from pathlib import Path

import boto3


class S3DataLake:
    def __init__(self, bucket_name: str, region: str):
        self.bucket_name = bucket_name
        self.client = boto3.client("s3", region_name=region)

    def upload_file(
        self,
        local_path: str | Path,
        layer: str,
        object_name: str | None = None,
    ) -> str:
        path = Path(local_path)
        key = f"{layer.strip('/')}/{object_name or path.name}"

        self.client.upload_file(
            str(path),
            self.bucket_name,
            key,
        )

        return f"s3://{self.bucket_name}/{key}"

    def upload_directory(
        self,
        local_directory: str | Path,
        layer: str,
    ) -> list[str]:
        directory = Path(local_directory)
        uploaded = []

        for path in directory.rglob("*"):
            if path.is_file():
                relative = path.relative_to(directory).as_posix()
                uploaded.append(
                    self.upload_file(
                        path,
                        layer,
                        relative,
                    )
                )

        return uploaded
