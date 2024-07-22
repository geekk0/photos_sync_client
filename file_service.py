import os
import shutil
import configparser
import time

from loguru import logger


class FileTransferService:

    def __init__(self, ):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.destination_path = config['PATH_SETTINGS']['DESTINATION_PATH']
        self.delay_value = int(config['STUDIO_SETTINGS']['delay_value'])
        self.logger = None
        self.init_logger()

    def move_file(self, file):
        try:
            shutil.move(file, self.destination_path)
            return 'success'
        except Exception as e:
            logger.error(f'move file error {e}')
            return 'error'

    def check_file_complete(self, file, counter=0):

        start_file_size = os.path.getsize(file)
        time.sleep(0.7)
        end_file_size = os.path.getsize(file)
        if end_file_size == start_file_size:
            logger.info(f'file {file} is full')
            return True
        elif counter < 3:
            counter += 1
            logger.debug(f'file {file} is uncompleted')
            self.check_file_complete(file, counter)

        else:
            return False

    async def transfer_files(self, files_list: list):
        for file in files_list:
            try:
                shutil.move(file, self.destination_path)
                logger.info(f'file {file} moved')
            except Exception as e:
                logger.error(f'move file error {e}')

    def check_file_name(self, file):
        if '~' in file:
            time.sleep(self.delay_value)

    def init_logger(self):
        log_file_name = 'sync_client.log'

        self.logger = logger

        logger.add(log_file_name,
                   format="{time} {level} {message}",
                   rotation="10 MB",
                   compression='zip',
                   level="DEBUG")


