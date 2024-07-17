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
        self.logger = None
        self.init_logger()

    def move_file(self, file):
        try:
            if self.check_file_complete(file):
                try:
                    shutil.move(file, self.destination_path)
                except Exception as e:
                    logger.error(f'move file error {e}')
            else:
                logger.warning(f'file {file} is not complete')
        except Exception as e:
            logger.error(e)

    # @staticmethod
    # async def check_file_complete(file):
    #     print(f'executing check_file_complete for {file}')
    #     try:
    #         old_file_size = 0
    #         while True:
    #             current_file_size = os.path.getsize(file)
    #             if current_file_size == old_file_size:  # If the file size hasn't changed, the file is complete
    #                 print(f'file {file} is full')
    #                 return True
    #             else:  # If the file size has changed, wait and check again
    #                 old_file_size = current_file_size
    #                 await asyncio.sleep(0.7)
    #     except Exception as e:
    #         print(e)

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

    def init_logger(self):
        log_file_name = 'sync_client.log'

        self.logger = logger

        logger.add(log_file_name,
                   format="{time} {level} {message}",
                   rotation="10 MB",
                   compression='zip',
                   level="DEBUG")


