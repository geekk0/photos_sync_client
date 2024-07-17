import asyncio
import glob
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from file_service import FileTransferService
from PyQt5.QtCore import QObject, QMetaObject, Qt, Q_ARG


class FileSystemEventService(FileSystemEventHandler, QObject):

    def __init__(self):
        FileSystemEventHandler.__init__(self)
        QObject.__init__(self)
        self.file_service = FileTransferService()
        self.note_field = None

    def assign_log_widget(self, note_widget):
        self.note_field = note_widget

    def on_created(self, event):
        print(f'New file {event.src_path} has been created!')
        try:
            if event.src_path.lower().endswith('.jpg'):
                self.file_service.move_file(event.src_path)
                current_value = self.note_field.toPlainText()
                file_name = event.src_path.split('\\')[-1]
                print(self.file_service.destination_path)
                folder = (f"{self.file_service.destination_path.split('/')[-2]}/"
                          f"{self.file_service.destination_path.split('/')[-1]}")
                message = f'{file_name} был перемещен в папку "{folder}"\n'
                new_message = message + current_value

                # Update the text field in the main thread
                QMetaObject.invokeMethod(self.note_field, "setPlainText", Qt.QueuedConnection,
                                         Q_ARG(str, new_message))
        except Exception as e:
            print(f'Error occurred while moving file {event.src_path} to {self.file_service.destination_path}: {e}')


class HandlerService:
    def __init__(self):
        self.observer = None
        self.stopped = False
        self.event_handler = FileSystemEventService()

    async def monitor_folder(self, path, note_widget):
        self.event_handler.assign_log_widget(note_widget)
        self.observer = Observer()

        existing_files = glob.glob(os.path.join(path, '*'))
        for file in existing_files:
            event = FileCreatedEvent(file)
            await asyncio.sleep(0.3)
            self.event_handler.on_created(event)

        self.observer.schedule(self.event_handler, path, recursive=True)
        self.observer.start()

        try:
            while True:
                if self.stopped:
                    break
                await asyncio.sleep(0.7)
        except KeyboardInterrupt:
            pass
        finally:
            self.observer.stop()
            self.observer.join()

