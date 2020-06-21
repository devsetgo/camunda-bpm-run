from zipfile import ZipFile
import requests
from pathlib import Path
import tqdm
import os
import stat
import sys
import shutil
from dotenv import load_dotenv
import yaml

save_directory = "camunda"
bpm_dir = "bpm_run"
resource_dir = "resources"

USE_ENV = os.getenv("USE_ENV")
if USE_ENV != 'docker':
    load_dotenv()

env_var = {
"TEST": "bob",
"RUN_APPS": os.getenv("RUN_APPS"),
"USER_NAME": os.getenv("USER_NAME"),
"PASSWORD": os.getenv("PASSWORD"),
# Options [postgres, mariadb, h2, oracle, mssql, db2]
"DRIVER_TYPE": os.getenv("DRIVER_TYPE"),
"DB_URI": os.getenv("DB_URI"),
"DB_NAME": os.getenv("DB_NAME"),
}

def unzip_to_directory(version: int):

    file_name: str = f"camunda-bpm-run-7.{version}.0.zip"

    # open from
    open_path = Path.cwd().joinpath(save_directory)
    saved_file = f"{open_path}/{file_name}"

    # unzip to
    unzip_path = Path.cwd().joinpath(bpm_dir)
    unzip_file = f"{unzip_path}/{file_name}"
    # unzip file
    with ZipFile(saved_file, "r") as zipObj:
        # Extract all the contents of zip file in different directory
        zipObj.extractall(unzip_path)


def chmod_start_sh():
    # unzip to
    unzip_path = Path.cwd().joinpath(bpm_dir)
    chmod_file = f"{unzip_path}/start.sh"
    st = os.stat(chmod_file)
    os.chmod(chmod_file, st.st_mode | stat.S_IEXEC)


def copy_resources():

    resource_path = Path.cwd().joinpath(resource_dir)
    resource_build = Path.cwd().joinpath(bpm_dir)
    bpm_resource_location = f"{resource_build}/configuration/resources"
    shutil.copytree(resource_path, bpm_resource_location)


def download_file(version: int):

    # https://downloads.camunda.cloud/release/camunda-bpm/run/7.13/camunda-bpm-run-7.13.0.zip
    url: str = f"https://downloads.camunda.cloud/release/camunda-bpm/run/7.{version}/camunda-bpm-run-7.{version}.0.zip"

    r = requests.get(url, stream=True)
    file_size = int(r.headers["Content-Length"])
    chunk_size = 1024  # 1 MB
    num_bars = int(file_size / chunk_size)

    file_name = url.split("/")[-1]  # this will take only -1 splitted part of the url

    directory_path = Path.cwd().joinpath(save_directory)
    save_file = f"{directory_path}/{file_name}"
    # download and save file
    with open(save_file, "wb") as output_file:
        # stream data save by each chunk
        for chunk in tqdm.tqdm(
            r.iter_content(chunk_size=chunk_size),
            total=num_bars,
            unit="KB",
            desc="Download Camunda BPM Run",
            leave=True,
            file=sys.stdout,
        ):

            output_file.write(chunk)


def generate_configuration():

    print(env_var)
    # fin = open("resources/application_configuration/base_template.yml", "rt")
    # # # output file to write the result to
    # fout = open("resources/application_configuration/default2.yml", "wt")
    # # for each line in the input file
    # for k,v in env_var.items():
                
    #     for line in fin:
    #         # read replace the string and write to output file
    #         fout.write(line.replace(k, v))
    #         print(k,v)
    
    # # close input and output files
    # fin.close()
    # fout.close()
    with open("resources/application_configuration/base_template.yml", "rt") as fin:
        with open("resources/application_configuration/default2.yml", "wt") as fout:
            
            for k,v in env_var.items():
                for line in fin:
                    fout.write(line.replace(k, "toast"))

def inplace_change(filename, old_string, new_string):
    file_name = "resources/application_configuration/default2.yml"
    # Safely read the input filename using 'with'
    with open(file_name) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(file_name, 'w') as f:
        print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)


def save_config():
    pass


def start_camunda():
    pass


def start():

    # start download
    download_file(version=13)
    # unzip file
    unzip_to_directory(version=13)
    # set permission
    chmod_start_sh()
    # configure?
    generate_configuration()
    # add resource files?
    # copy_resources()
    # start?


if __name__ == "__main__":
    start()
