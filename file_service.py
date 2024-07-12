import os
import shutil
import configparser
import time


class FileTransferService:

    def __init__(self, ):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.destination_path = config['PATH_SETTINGS']['DESTINATION_PATH']

    def move_file(self, file):
        if self.check_file_complete(file):
            try:
                shutil.move(file, self.destination_path)
                # print(self.destination_path)
            except Exception as e:
                print(f'move file error {e}')

    @staticmethod
    def check_file_complete(file):
        start_file_size = os.path.getsize(file)
        time.sleep(0.7)
        end_file_size = os.path.getsize(file)
        if end_file_size == start_file_size:
            print(f'start size: {start_file_size}')
            print(f'stop size: {end_file_size}')
            print('file size match')
            return True
