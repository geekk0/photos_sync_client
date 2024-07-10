import asyncio

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file_service import FileTransferService
from PyQt5.QtCore import QObject, QMetaObject, Qt, Q_ARG


class FileSystemEventService(FileSystemEventHandler, QObject):


    def __init__(self, note_widget):
        FileSystemEventHandler.__init__(self)
        QObject.__init__(self)
        self.file_service = FileTransferService()
        self.note_field = note_widget

    def on_created(self, event):
        print(f'New file {event.src_path} has been created!')
        try:
            self.file_service.move_file(event.src_path)

            # Get the current value
            current_value = self.note_field.toPlainText()

            file_name = event.src_path.split('\\')[-1]
            print(file_name)

            message = f'{file_name} has been moved\n'
            new_message = message + current_value

            # Update the text field in the main thread
            QMetaObject.invokeMethod(self.note_field, "setText", Qt.QueuedConnection,
                                     Q_ARG(str, new_message))
        except Exception as e:
            print(f'Error occurred while moving file {event.src_path} to {self.file_service.destination_path}: {e}')


class HandlerService:
    def __init__(self, note_widget):
        self.system_service = FileSystemEventService(note_widget)
        self.note_widget = note_widget

    @staticmethod
    async def monitor_folder(path, note_widget):
        event_handler = FileSystemEventService(note_widget)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        try:
            while True:
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
