# -*- coding: utf-8 -*-
import httpx
from tqdm import tqdm
from zipfile import ZipFile
import shutil, os, pathlib, stat, logging


def download_camunda(version: str):
    url: str = f"https://downloads.camunda.cloud/release/camunda-bpm/run/{version}/camunda-bpm-run-{version}.0.zip"
    local_filename = url.split("/")[-1]
    # NOTE the stream=True parameter below
    with httpx.stream("GET", url, follow_redirects=True) as r:
        total_size = int(r.headers["Content-Length"])
        downloaded = 0  # keep track of size downloaded so far
        chunkSize = 1024
        bars = int(total_size / chunkSize)
        logging.info(dict(num_bars=bars))
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in tqdm(
                r.iter_bytes(chunkSize),
                total=bars,
                unit="KB",
                desc=local_filename,
                leave=True,
            ):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
                downloaded += chunkSize  # increment the downloaded
                prog = downloaded * 100 / total_size
                # progress["value"] = (prog)  # *100 #Default max value of tkinter progress is 100

    return local_filename


def unzip_camunda(version: str):

    file_name: str = f"camunda-bpm-run-{version}.0.zip"
    with ZipFile(file_name, "r") as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall("bpm_run")
    os.remove(file_name)
    set_execute_permission()


def set_execute_permission():
    st = os.stat("bpm_run/start.sh")
    os.chmod("bpm_run/start.sh", st.st_mode | stat.S_IEXEC)


def process_existing_files():
    return True


def copy_files():

    file_list:list = ["bpm_run/configuration/default.yml","bpm_run/configuration/production.yml","bpm_run/configuration/resources/*"]#,""]
    
    for f in tqdm(file_list):
        my_file = pathlib.Path(f'/workspaces/camunda-bpm-run/engine/{f}')

        to_file = pathlib.Path(f'/workspaces/camunda-bpm-run/engine/back_up')
        shutil.copy(my_file, to_file)


def clean_directories():
    print("clean directories")
    rename_files()


def rename_files():
    print("renaming files")


def main(version: str):
    logging.info("Starting Download")
    copy_files()
    # download_camunda(version=version)
    # clean_directories()
    # move_camunda(version=version)
    # unzip_camunda(version=version)


if __name__ == "__main__":
    main(version="7.17")
