import datetime
import os
import time


def create_dummy_files(directory, qty):
    for n in range(1, qty+1):
        print(n)
        initial_filename = f"initial_file_{n}.JPG"
        final_filename = f"final_file_{n}.JPG"
        file_size = 15 * 1024 * 1024

        initial_path = os.path.join(directory, initial_filename)
        final_path = os.path.join(directory, final_filename)

        with open(initial_path, 'wb') as f:
            f.write(os.urandom(file_size))
        time.sleep(5)

        try:
            os.rename(initial_path, final_path)
            print(datetime.datetime.now())
        except FileExistsError:
            print(f'file {initial_path} was moved')


directory = input("Enter the directory path: ")
num_files = int(input("Enter number of files: "))

try:
    create_dummy_files(directory, num_files)
except Exception as e:
    print(e)
