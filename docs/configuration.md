# Configuration
Configuration of Camunda BPM Run

LOGURU_RETENTION
LOGURU_ROTATION
LOGURU_LOGGING_LEVEL

RUN_APPS
USER_NAME
PASSWORD

Options [postgres, mariadb, h2, oracle, mssql, db2]
DRIVER_TYPE
DB_URI
DB_NAME
DRIVER-CLASS-NAME

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