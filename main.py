import os
import configparser

from handler_service import HandlerService

config = configparser.ConfigParser()
with open('config.ini', 'r', encoding='utf-8') as f:
    config.read_file(f)


class SyncManager:
    def __init__(self, current_config: configparser.ConfigParser):
        self.config = current_config
        self.source_path = None
        self.destination_path = None
        self.error = None
        self.note_field = None
        self.studio_name = None
        self.handler_service = HandlerService()

    def init_settings(self):
        try:
            paths = dict(config.items('PATH_SETTINGS'))
            for key, path in paths.items():
                if not os.path.isdir(path):
                    print(f'No such path: {path}')
                    self.error = True
                else:
                    setattr(self, key, path)
            studio_settings = dict(config.items('STUDIO_SETTINGS'))
            for key, value in studio_settings.items():
                setattr(self, key, value)
        except Exception as e:
            print(e)

    @staticmethod
    def save_settings(**settings: str):

        for k, v in settings.items():
            if 'path' in k:
                config.set('PATH_SETTINGS', k, v)
            else:
                config.set('STUDIO_SETTINGS', k, v)
            with open('config.ini', 'w', encoding='utf-8') as configfile:
                config.write(configfile)

    async def track_created_files(self, note_field):
        await self.handler_service.monitor_folder(self.source_path, note_field)
