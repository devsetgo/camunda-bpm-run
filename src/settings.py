from dotenv import load_dotenv
import os

USE_ENV = os.getenv("USE_ENV")

if USE_ENV != "docker":
    load_dotenv()

LOGURU_RETENTION = os.getenv("LOGURU_RETENTION")
LOGURU_ROTATION = os.getenv("LOGURU_ROTATION")
LOGURU_LOGGING_LEVEL = os.getenv("LOGURU_LOGGING_LEVEL")

ENV_VAR = {
    "TEST": "bob",
    "RUN_APPS": os.getenv("RUN_APPS"),
    "USER_NAME": os.getenv("USER_NAME"),
    "PASSWORD": os.getenv("PASSWORD"),
    # Options [postgres, mariadb, h2, oracle, mssql, db2]
    "DRIVER_TYPE": os.getenv("DRIVER_TYPE"),
    "DB_URI": os.getenv("DB_URI"),
    "DB_NAME": os.getenv("DB_NAME"),
    "DRIVER-CLASS-NAME": "none",
}
