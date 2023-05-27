from getgauge.python import data_store, Messages
import psycopg2
import step_impl.conn_db as conn_db
import time

def increment_ver(version):
    version = version.split('.')

    if(int(version[2]) == 9):
        version[1] = str(int(version[1]) + 1)
        version[2] = str(0)    
    elif(int(version[2]) != 9):
        version[2] = str(int(version[2]) + 1)
    elif(int(version[1]) == 9):
        version[0] = str(int(version[0]) + 1) 
        version[1] = str(0)
        version[2] = str(0)        

    return '.'.join(version)

def parent_version(type, code):

    latest_version = "SELECT max(version) as version \
                    FROM blueprints \
                    WHERE type = " + "'" + type + "' \
                    AND code = " + "'" + code + "' \
                    LIMIT 1"
    
    data_store.suite.parent_version = (conn_db.execute_query(data_store.suite.db_product_registry_dbconn, data_store.suite.db_fetch_no_of_retries, data_store.suite.db_fetch_duration_interval, latest_version, 1))
    
    if not(data_store.suite.parent_version[0]['version']):
        data_store.suite.parent_version[0]['version'] = '0.0.1'
        print(data_store.suite.parent_version[0]['version'])
    else:
        data_store.suite.parent_version[0]['version'] = increment_ver(data_store.suite.parent_version[0]['version'])
        print(data_store.suite.parent_version[0]['version']) 

    return (data_store.suite.parent_version[0]['version'])

def string_format(data):
    if "<timestamp>" in data:
        return data.replace("<timestamp>", data_store.suite.datetimestamp)