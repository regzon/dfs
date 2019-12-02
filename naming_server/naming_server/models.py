from django.db import models

from .utils import send_request


class Directory(models.Model):
    name = models.CharField(max_length=255)
    parent_dir = models.ForeignKey(
        'Directory',
        on_delete=models.CASCADE,
        related_name='subdirs',
        null=True,
    )


class Storage(models.Model):
    ip_address = models.GenericIPAddressField()
    files = models.ManyToManyField(
        'File',
        related_name='storages',
        through='StoredFile',
    )
    available_size = models.IntegerField()
    last_heartbeat = models.DateTimeField()

    def initialize(self):
        response = send_request(
            self.ip_address,
            uri='/initialize_root',
            method='post',
        )
        return response['size']

    def create_file(self, path):
        send_request(
            self.ip_address,
            uri='/create_file',
            method='post',
            data={'path': path},
        )

    def delete_file(self, path):
        send_request(
            self.ip_address,
            uri='/delete_file',
            method='post',
            data={'path': path},
        )

    def delete_dir(self, path):
        send_request(
            self.ip_address,
            uri='/delete_dir',
            method='post',
            data={'path': path},
        )

    def transfer(self, path, download_url):
        send_request(
            self.ip_address,
            uri='/transfer',
            method='post',
            data={'path': path, 'download_url': download_url},
        )

    def copy_file(self, path):
        send_request(
            self.ip_address,
            uri='/copy_file',
            method='post',
            data={'path': path},
        )


class File(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField(default=0)
    parent_dir = models.ForeignKey(
        'Directory',
        on_delete=models.CASCADE,
        related_name='files',
    )


class StoredFile(models.Model):
    WAITING = 'WTN'
    UPLOADING = 'UPL'
    READY = 'RDY'
    DELETING = 'DEL'
    MOVING = 'MOV'

    STATUSES = [
        (WAITING, 'Waiting'),
        (UPLOADING, 'Uploading'),
        (READY, 'Ready'),
        (DELETING, 'Deleting'),
        (MOVING, 'Moving'),
    ]

    status = models.CharField(
        max_length=3,
        choices=STATUSES,
        null=True,
    )

    file = models.ForeignKey(
        'File',
        on_delete=models.CASCADE,
        related_name='stored_files',
    )
    storage = models.ForeignKey(
        'Storage',
        on_delete=models.CASCADE,
        related_name='stored_files',
    )
