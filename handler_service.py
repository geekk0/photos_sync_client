import asyncio
import glob
import os
import threading
import time
import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from file_service import FileTransferService
from PyQt5.QtCore import QObject, QMetaObject, Qt, Q_ARG


class FileSystemEventService(FileSystemEventHandler, QObject):

    def __init__(self):
        FileSystemEventHandler.__init__(self)
        QObject.__init__(self)
        self.file_service = FileTransferService()
        self.note_field = None
        self.pending_move_tasks = {}

    def assign_log_widget(self, note_widget):
        self.note_field = note_widget

    def on_moved(self, event: FileSystemEvent) -> None:
        if event.dest_path.lower().endswith('jpg'):
            print(f"see file {event.dest_path} at {datetime.datetime.now()}")

            if self.file_service.previous_file:
                if self.file_service.previous_file in self.pending_move_tasks:
                    self.pending_move_tasks[self.file_service.previous_file].cancel()
                    del self.pending_move_tasks[self.file_service.previous_file]
                self.move_file(self.file_service.previous_file)

            self.file_service.previous_file = event.dest_path
            timer = threading.Timer(60*2, self.move_file, [event.dest_path])
            self.pending_move_tasks[event.dest_path] = timer
            print(f'timer for {event.dest_path} started at: {datetime.datetime.now()}')
            timer.start()

    def rewrite_log_field(self, event_src_path, status: str):
        current_value = self.note_field.toPlainText()

        file_name = event_src_path.split('\\')[-1]
        folder = (f"{self.file_service.destination_path.split('/')[-2]}/"
                  f"{self.file_service.destination_path.split('/')[-1]}")
        if status == 'success':
            message = f'{file_name} был перемещен в папку "{folder}"\n'
            print(f'{file_name} was moved at {datetime.datetime.now()}')
        else:
            message = f'Ошибка переноса файла "{file_name}"!\n'

        new_message = message + current_value

        QMetaObject.invokeMethod(self.note_field, "setPlainText", Qt.QueuedConnection,
                                 Q_ARG(str, new_message))

    def move_file(self, file_path):
        if os.path.exists(file_path):
            try:
                move_result = self.file_service.move_file(file_path)
                self.rewrite_log_field(file_path, move_result)
                print(f'{file_path} was copied at: {datetime.datetime.now()}')
            except FileExistsError as e:
                print(f'File already exists: {e}')
            except Exception as e:
                print(f'Error occurred while moving file {file_path}: {e}')


class HandlerService:
    def __init__(self):
        self.observer = None
        self.stopped = False
        self.event_handler = FileSystemEventService()

    async def monitor_folder(self, path, note_widget):
        self.event_handler.assign_log_widget(note_widget)
        self.observer = Observer()

        await self.transfer_existing_files(path)

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

    async def transfer_existing_files(self, path):
        while not self.is_directory_empty(path):

            existing_files = [f for f in glob.glob(os.path.join(path, '*')) if os.path.isfile(f)]
            sorted_files = sorted(existing_files, key=os.path.getmtime)

            for file in sorted_files:
                move_result = self.event_handler.file_service.move_file(file)
                await asyncio.sleep(0.7)
                self.event_handler.rewrite_log_field(file, move_result)

    @staticmethod
    def is_directory_empty(path):
        with os.scandir(path) as it:
            for entry in it:
                if entry.name.lower().endswith('.jpg') and entry.is_file():
                    return False
        return True
