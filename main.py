import asyncio
import os
import configparser

from handler_service import HandlerService

config = configparser.ConfigParser()
config.read('config.ini')


class SyncManager:
    def __init__(self, current_config: configparser.ConfigParser, note_field):
        self.config = current_config
        self.source_path = None
        self.destination_path = None
        self.error = None
        self.note_field = note_field
        self.handler_service = HandlerService(note_field)

    def init_paths(self):
        paths = dict(config.items('PATH_SETTINGS'))
        for key, path in paths.items():
            if not os.path.isdir(path):
                print(f'No such path: {path}')
                self.error = True
            else:
                setattr(self, key, path)

    async def track_created_files(self):
        await self.handler_service.monitor_folder(self.source_path, self.note_field)
        # await asyncio.sleep(10)






