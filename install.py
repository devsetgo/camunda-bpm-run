from zipfile import ZipFile
import requests
from pathlib import Path
import tqdm
import os
import stat
import sys

save_directory = "camunda"
unzip_dir = "bpm_run"


def unzip_to_directory(version:int):
    
    file_name: str = f"camunda-bpm-run-7.{version}.0.zip"
    
    # open from
    open_path = Path.cwd().joinpath(save_directory)
    saved_file = f"{open_path}/{file_name}"

    # unzip to
    unzip_path = Path.cwd().joinpath(unzip_dir)
    unzip_file = f"{unzip_path}/{file_name}"
    # unzip file
    with ZipFile(saved_file, 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        zipObj.extractall(unzip_path)

def chmod_start_sh():
        # unzip to
    unzip_path = Path.cwd().joinpath(unzip_dir)
    chmod_file = f"{unzip_path}/start.sh"
    st = os.stat(chmod_file)
    os.chmod(chmod_file, st.st_mode | stat.S_IEXEC)





def download_file(version: int):

    # https://downloads.camunda.cloud/release/camunda-bpm/run/7.13/camunda-bpm-run-7.13.0.zip
    url: str = f"https://downloads.camunda.cloud/release/camunda-bpm/run/7.{version}/camunda-bpm-run-7.{version}.0.zip"

    r = requests.get(url, stream=True)
    file_size = int(r.headers['Content-Length'])
    chunk_size = 1024  # 1 MB
    num_bars = int(file_size / chunk_size)


    file_name = url.split('/')[-1] # this will take only -1 splitted part of the url

    directory_path = Path.cwd().joinpath(save_directory)
    save_file = f"{directory_path}/{file_name}"
    # download and save file
    with open(save_file,'wb') as output_file:
        # stream data save by each chunk
        for chunk in tqdm.tqdm(r.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc="Download Camunda BPM Run", leave=True, file=sys.stdout):
        
            output_file.write(chunk)


def start():
    
    # start download
    download_file(version=13)
    # unzip file
    unzip_to_directory(version=13)
    # set permission
    chmod_start_sh()
    # add resource files?

    # configure?

    # start?

if __name__ == "__main__":
    start()