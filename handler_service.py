from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file_service import FileTransferService
import time


class FileSystemEventService(FileSystemEventHandler):

    def __init__(self):
        self.file_service = FileTransferService()
        super().__init__()

    def on_created(self, event):
        print(f'New file {event.src_path} has been created!')
        try:
            self.file_service.move_file(event.src_path)
        except Exception as e:
            print(f'Error occurred while moving file {event.src_path} to {self.file_service.destination_path}: {e}')


class HandlerService:
    def __init__(self):
        self.system_service = FileSystemEventService

    @staticmethod
    def monitor_folder(path):
        event_handler = FileSystemEventService()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

# Use the function
# monitor_folder('path_to_your_folder')
