"""
Google Cloud Storage Reader
"""
import io
import os
from ...data.readers.internals.base_inner_reader import BaseInnerReader
from ...utils import common, paths
from ...logging import get_logger
try:
    from google.auth.credentials import AnonymousCredentials  # type:ignore
    from google.cloud import storage  # type:ignore
except ImportError:   # pragma: no cover
    pass


class GoogleCloudStorageReader(BaseInnerReader):

    def __init__(self, project: str, **kwargs):
        super().__init__(**kwargs)
        self.project = project

    def get_blob_stream(self, object_name):
        bucket, object_path, name, extension = paths.get_parts(object_name)
        blob = get_blob(project=self.project, bucket=bucket, blob_name=object_path + name + extension)
        stream = blob.download_as_bytes()
        io_stream = io.BytesIO(stream)
        return io_stream

    def get_blobs_at_path(self, path):
        bucket, object_path, name, extension = paths.get_parts(path)

        # this means we're testing
        if os.environ.get("STORAGE_EMULATOR_HOST") is not None:
            client = storage.Client(
                credentials=AnonymousCredentials(),
                project=self.project,
            )
        else:
            client = storage.Client(project=self.project)

        gcs_bucket = client.get_bucket(bucket)
        blobs = list(client.list_blobs(bucket_or_name=gcs_bucket, prefix=object_path))

        yield from [bucket + '/' + blob.name
                for blob in blobs
                if not blob.name.endswith('/')]


def get_blob(
        project: str,
        bucket: str,
        blob_name: str):

    # this means we're testing
    if os.environ.get("STORAGE_EMULATOR_HOST") is not None:
        client = storage.Client(
            credentials=AnonymousCredentials(),
            project=project,
        )
    else:
        client = storage.Client(project=project)

    gcs_bucket = client.get_bucket(bucket)
    blob = gcs_bucket.get_blob(blob_name)
    return blob
