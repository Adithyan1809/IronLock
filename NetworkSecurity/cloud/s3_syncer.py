
import os
import sys
import subprocess

from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging


class S3Sync:

    def sync_folder_to_s3(self, folder: str, aws_bucket_url: str):
        try:
            # Check whether local folder exists
            if not os.path.exists(folder):
                raise FileNotFoundError(
                    f"Local folder does not exist: {folder}"
                )

            if not os.path.isdir(folder):
                raise NotADirectoryError(
                    f"Expected a directory, got: {folder}"
                )

            command = [
                "aws",
                "s3",
                "sync",
                folder,
                aws_bucket_url,
                "--only-show-errors"
            ]

            logging.info(
                f"Starting S3 sync: {folder} -> {aws_bucket_url}"
            )

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )

            if result.stdout:
                logging.info(result.stdout)

            if result.stderr:
                logging.warning(result.stderr)

            logging.info(
                f"Successfully synced {folder} to {aws_bucket_url}"
            )

        except Exception as e:
            logging.error(f"S3 synchronization failed: {str(e)}")
            raise NetworkSecurityException(e, sys)
