import os
import sys
import logging
from azure.storage.blob import BlobServiceClient


# TODO: needs some test cases!
class AzureBlobController:
    def __init__(self, connection_string, container_name):
        # Create a logger for the 'azure.storage.blob' SDK
        self.logger = logging.getLogger('azure.storage.blob')
        self.logger.setLevel(logging.DEBUG)

        # Configure a console output
        self.handler = logging.StreamHandler(stream=sys.stdout)
        self.logger.addHandler(self.handler)

        self.container_name = container_name
        self.service_client = BlobServiceClient.from_connection_string(connection_string, logging_enable=True)
        self.container_client = self.service_client.get_container_client(container_name)

    def upload(self, source, dest):
        """
        Upload a file or directory to a path inside the container
        """
        if os.path.isdir(source):
            self.upload_dir(source, dest)
        else:
            self.upload_file(source, dest)

    def upload_file(self, source, dest):
        """
        Upload a single file to a path inside the container
        """
        print(f'Uploading {source} to {dest}')
        with open(source, 'rb') as data:
            self.container_client.upload_blob(name=dest, data=data)

    def upload_dir(self, source, dest):
        """
        Upload a directory to a path inside the container
        """
        prefix = '' if dest == '' else dest + '/'
        prefix += os.path.basename(source) + '/'
        for root, dirs, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = '' if dir_part == '.' else dir_part + '/'
                file_path = os.path.join(root, name)
                blob_path = prefix + dir_part + name
                self.upload_file(file_path, blob_path)

    def download(self, source, dest):
        """
        Download a file or directory to a path on the local filesystem
        """
        if not dest:
            raise Exception('A destination must be provided')

        blobs = self.ls_files(source, recursive=True)
        if blobs:
            # if source is a directory, dest must also be a directory
            if not source == '' and not source.endswith('/'):
                source += '/'
            if not dest.endswith('/'):
                dest += '/'
            # append the directory name from source to the destination
            dest += os.path.basename(os.path.normpath(source)) + '/'

            blobs = [source + blob for blob in blobs]
            for blob in blobs:
                blob_dest = dest + os.path.relpath(blob, source)
                self.download_file(blob, blob_dest)
        else:
            self.download_file(source, dest)

    def download_file(self, source, dest):
        """
        Download a single file to a path on the local filesystem
        """
        # dest is a directory if ending with '/' or '.', otherwise it's a file
        if dest.endswith('.'):
            dest += '/'
        blob_dest = dest + os.path.basename(source) if dest.endswith('/') else dest

        print(f'Downloading {source} to {blob_dest}')
        os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
        bc = self.service_client.get_blob_client(container=self.container_name, blob=source)
        with open(blob_dest, 'wb') as file:
            data = bc.download_blob()
            file.write(data.readall())

    def ls_files(self, path, recursive=False):
        """
        List files under a path, optionally recursively
        """
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.container_client.list_blobs(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
            if recursive or '/' not in relative_path:
                files.append(relative_path)
        return files

    def ls_dirs(self, path, recursive=False):
        """
        List directories under a path, optionally recursively
        """
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.container_client.list_blobs(name_starts_with=path)
        dirs = []
        for blob in blob_iter:
            relative_dir = os.path.dirname(os.path.relpath(blob.name, path))
            if relative_dir and (recursive or '/' not in relative_dir) and relative_dir not in dirs:
                dirs.append(relative_dir)

        return dirs

    def rm(self, path, recursive=False):
        """
        Remove a single file, or remove a path recursively
        """
        if recursive:
            self.rmdir(path)
        else:
            print(f'Deleting {path}')
            self.container_client.delete_blob(path)

    def rmdir(self, path):
        """
        Remove a directory and its contents recursively
        """
        blobs = self.ls_files(path, recursive=True)
        if not blobs:
            return

        if not path == '' and not path.endswith('/'):
            path += '/'
        blobs = [path + blob for blob in blobs]
        print(f'Deleting {", ".join(blobs)}')
        self.container_client.delete_blobs(*blobs)
