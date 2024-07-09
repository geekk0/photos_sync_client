import os
import time
import configparser

from handler_service import HandlerService

config = configparser.ConfigParser()
config.read('config.ini')


class SyncManager:
    def __init__(self, current_config: configparser.ConfigParser):
        self.config = current_config
        self.source_path = None
        self.destination_path = None
        self.error = None
        self.handler_service = HandlerService()

    def init_paths(self):
        paths = dict(config.items('PATH_SETTINGS'))
        for key, path in paths.items():
            if not os.path.isdir(path):
                print(f'No such path: {path}')
                self.error = True
            else:
                setattr(self, key, path)

    def track_created_files(self):
        self.handler_service.monitor_folder(self.source_path)


def run_sync_manager():
    sync_manager = SyncManager(config)
    sync_manager.init_paths()
    if not sync_manager.error:
        sync_manager.track_created_files()


if __name__ == '__main__':
    sync_manager = SyncManager(config)
    sync_manager.init_paths()
    if not sync_manager.error:
        sync_manager.track_created_files()





