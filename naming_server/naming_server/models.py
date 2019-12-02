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


class File(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField(default=0)
    parent_dir = models.ForeignKey(
        'Directory',
        on_delete=models.CASCADE,
        related_name='files',
    )


class StoredFile(models.Model):
    UPLOADING = 'UPL'
    READY = 'RDY'
    DELETING = 'DEL'
    MOVING = 'MOV'

    STATUSES = [
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

    file = models.ForeignKey('File', on_delete=models.CASCADE)
    storage = models.ForeignKey('Storage', on_delete=models.CASCADE)
