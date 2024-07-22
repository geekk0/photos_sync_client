import os
import time
from datetime import datetime


def create_dummy_files(directory, num_files, file_size):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(num_files):
        now = datetime.now()
        filename = f'{now.hour}_{now.minute}_{i}.jpg'
        with open(os.path.join(directory, filename), 'wb') as f:
            f.write(os.urandom(file_size))
        time.sleep(0.5)

# Size of each file in bytes (15 MB)
file_size = 15 * 1024 * 1024

directory = input("Enter the directory path: ")
num_files = int(input("Enter number of files: "))


while True:
    start_time = time.time()
    create_dummy_files(directory, num_files, file_size)
    end_time = time.time()
    elapsed_time = end_time - start_time
    now = datetime.now()
    print(f'Files created at {now.strftime("%H:%M:%S")}, {num_files} files created.')
    time.sleep(max(0, int(3600 - elapsed_time)))


