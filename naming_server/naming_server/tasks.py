import logging

from uwsgidecorators import timer, spool

from .models import Storage, File, StoredFile

logger = logging.getLogger(__name__)


@spool(pass_arguments=True)
def transfer_task(file_id, sender_storage_id, receiver_storage_id):
    logger.info("Started a transfering task")
    file = File.objects.get(id=file_id)
    sender_storage = Storage.objects.get(id=sender_storage_id)
    receiver_storage = Storage.objects.get(id=receiver_storage_id)
    download_url = sender_storage.url + '/download_file'
    receiver_storage.transfer(file.path, download_url)
    logger.info("Finished a transfering task")


@timer(secs=10, target='spooler')
def check_stored_files(signum):
    logger.info("Started checking stored files")
    for storage in Storage.objects.all():
        for file in File.objects.exclude(storages=storage):
            logger.info(
                f"File {file.path} is not in storage {storage.ip_address}"
            )
            stored_file_queryset = StoredFile.objects.filter(
                status=StoredFile.READY,
                file=file,
            )
            if stored_file_queryset.count() == 0:
                logger.error(f"No storages available for file {file.path}")
                continue
            stored_file = stored_file_queryset[0]
            sender_storage = stored_file.storage
            StoredFile.objects.create(
                file=file,
                storage=storage,
                status=StoredFile.UPLOADING,
            )
            transfer_task.spool(file.id, sender_storage.id, storage.id)
    logger.info("Finished checking stored files")


@timer(secs=10, target='spooler')
def check_storages(signum):
    logger.info("Started checking storages")
    for storage in Storage.objects.all():
        try:
            storage.check_availability()
        except Exception:
            logger.warning("Storage {storage.ip_address} is unavailable")
            storage.delete()
    logger.info("Finished checking storages")
