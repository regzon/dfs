from django.db import models


class Directory(models.Model):
    name = models.CharField(max_length=255)
    parent_dir = models.ForeignKey(
        'Directory',
        on_delete=models.CASCADE,
        related_name='subdirs',
    )


class Storage(models.Model):
    storage_id = models.UUIDField()
    files = models.ManyToManyField(
        'Storage',
        related_name='storages',
        through='StoredFile',
    )
    available_size = models.IntegerField()
    last_heartbeat = models.DateTimeField()


class File(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()
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
