from getgauge.python import before_scenario, before_step, before_suite, data_store
import datetime
import psycopg2
import step_impl.conn_db as conn_db
import step_impl.utils.conn_api_proxy as conn_api_proxy
import os
import cx_Oracle
import sys

@before_suite
def before_suite_hook(context):
    data_store.suite.active_profile = os.getenv('active_profile', 'test')
    try:
        if sys.platform.startswith("linux"):  # Linux OS
            cx_Oracle.init_oracle_client(lib_dir="/opt/oracle/instantclient_21_4")
        elif sys.platform.startswith("darwin"):  # MacOS
            cx_Oracle.init_oracle_client(lib_dir="lib/instantclient_19_8")
        elif sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):  # Windows OS
            cx_Oracle.init_oracle_client(lib_dir=r"lib\instantclient_21_6")
    except Exception as err:
        print("[ERROR]", err)
        sys.exit(1)
    # Set database retry values
    data_store.suite.db_fetch_no_of_retries = 600
    data_store.suite.db_fetch_duration_interval = 0.2  # sleeps for 200 ms
    # # Establish database connection
    conn_db.establish_conn_db()
    # Set API proxy settings
    data_store.suite.proxy_dict, data_store.suite.proxy_cert = conn_api_proxy.get_proxy_settings()
    print("APIs are running behind proxy setting:", data_store.suite.proxy_dict)
    print("using certificate file in:", data_store.suite.proxy_cert)

    # mark test suite start timestamp
    datetimestamp = datetime.datetime.now()
    data_store.suite.datetimestamp = (datetimestamp.strftime("%m%d%y%H%M%S"))

@before_suite
def before_suite_scenario(context):
    datetimestamp = datetime.datetime.now()
    data_store.suite.datetimestamp = (datetimestamp.strftime("%m%d%y%H%M%S"))
   
@before_scenario
def before_scenario_hook(context):
    # mark scenario start timestamp
    datetimestamp = datetime.datetime.now()
    data_store.scenario.datetimestamp = str(int(datetimestamp.strftime("%m%d%y%H%M%S")))

@before_step
def before_step_hook(context):
    # mark step start timestamp
    datetimestamp = datetime.datetime.now()
    data_store.scenario.step_timestamp = str(int(datetimestamp.strftime("%m%d%y%H%M%S")))
