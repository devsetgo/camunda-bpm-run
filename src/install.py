# -*- coding: utf-8 -*-
from zipfile import ZipFile
import requests
from pathlib import Path
import tqdm
import logging
import os
import stat
import sys
import shutil
from dotenv import load_dotenv
import yaml
from logging_config import config_log
import settings
from loguru import logger

config_log()

save_directory = "camunda"
bpm_dir = "bpm_run"
resource_dir = "resources"

switch = {
    "postgres": {
        "DRIVER_TYPE": "postgresql",
        "DRIVER-CLASS-NAME": "org.postgresql.Driver",
        "file": "postgresql-42.2.13.jar",
    },
    "h2": {
        "DRIVER_TYPE": "h2",
        "DRIVER-CLASS-NAME": "org.h2.Driver",
        "file": "postgresql-42.2.13.jar",
    },
    "mariadb": {
        "DRIVER_TYPE": "mariadb",
        "DRIVER-CLASS-NAME": "org.mariadb.jdbc.Driver",
        "file": "mariadb-java-client-2.6.0.jar",
    },
    "oracle": {
        "DRIVER_TYPE": "oracle",
        "DRIVER-CLASS-NAME": "oracle.jdbc.OracleDriver",
        "file": "ojdbc10.jar",
    },
    "mssql": {
        "DRIVER_TYPE": "sqlserver",
        "DRIVER-CLASS-NAME": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        "file": "mssql-jdbc-8.2.2.jre11.jar",
    },
    "db2": {
        "DRIVER_TYPE": "db2",
        "DRIVER-CLASS-NAME": "com.ibm.db2.jcc.DB2Driver",
        "file": "jcc-11.5.0.0.jar",
    },
}


def set_db_driver(driver_type: str) -> str:

    data = switch[driver_type]
    result: str = data["DRIVER-CLASS-NAME"]
    logger.info(f"Setting Driver Class Name to {result}")
    return result


def unzip_to_directory(version: int):

    file_name: str = f"camunda-bpm-run-7.{version}.0.zip"
    logger.info(f"Unzipping {file_name}")
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
    logger.info(f"Unzipped file to {unzip_path}")


def chmod_start_sh():
    # unzip to
    unzip_path = Path.cwd().joinpath(bpm_dir)
    chmod_file = f"{unzip_path}/start.sh"
    st = os.stat(chmod_file)
    os.chmod(chmod_file, st.st_mode | stat.S_IEXEC)
    logger.info(f"Execution privilege set")


def copy_resources():

    resource_path = Path.cwd().joinpath(resource_dir)
    resource_build = Path.cwd().joinpath(bpm_dir)
    bpm_resource_location = f"{resource_build}/configuration/resources"
    # shutil.copytree(resource_path, bpm_resource_location)
    from distutils.dir_util import copy_tree

    logger.info("Starting copying of resources files")
    copy_tree(resource_path, bpm_resource_location)
    logger.info("Completed copying of resources files")


def download_file(version: int):

    # https://downloads.camunda.cloud/release/camunda-bpm/run/7.13/camunda-bpm-run-7.13.0.zip
    url: str = f"https://downloads.camunda.cloud/release/camunda-bpm/run/7.{version}/camunda-bpm-run-7.{version}.0.zip"
    logger.info(f"Downlaoding Camunda 7.{version} from {url}")
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
    logger.info(f"Download Completed")


def generate_configuration():
    logger.info(f"Begin configuration")
    create_template()
    # change variables
    ENV_VAR = settings.ENV_VAR

    for k, v in ENV_VAR.items():

        if k == "DRIVER-CLASS-NAME":
            v = set_db_driver(ENV_VAR["DRIVER_TYPE"])
        change_template_values(k, v)

    logger.info(f"Environmental variables have been set")

def change_template_values(key_name: str, value_name: str):

    file_name = "resources/application_configuration/default2.yml"
    # Read in the file
    with open(file_name, "r") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(key_name, value_name)
    logger.info(f"Setting value for {key_name}")
    # Write the file out again
    with open(file_name, "w") as file:
        file.write(filedata)


def create_template():
    from shutil import copyfile

    source = "resources/application_configuration/base_template.yml"
    target = "resources/application_configuration/default2.yml"
    logger.info(f"Copying file from {source}")
    copyfile(source, target)
    logger.info(f"File copied to {target}")


def start_camunda():
    pass


def start():

    logger.info("Starting download of Camunda BPM Run")
    # start download
    download_file(version=13)
    # unzip file
    logger.info("Starting unzip of Camunda BPM Run")
    unzip_to_directory(version=13)
    # set permission
    logger.info("Setting file permissions")
    chmod_start_sh()
    # configure?
    generate_configuration()
    # add resource files?
    copy_resources()
    # start?


if __name__ == "__main__":
    start()
