from getgauge.python import data_store, Messages
import cx_Oracle
import psycopg2
import os
import datetime, time

def establish_conn_db():
    db_names = os.getenv("db_all_connection_names","").split(",")
    for db_name in db_names:
        print("Connecting to " + db_name + "...")
        print(os.getenv(db_name + "_connection_type"))
        print(os.getenv(db_name + "_host"))
        if(os.getenv(db_name + "_connection_type") == "POSTGRES"):
            data_store.suite[db_name + "_dbconn"] = psycopg2.connect(
                host=(os.getenv(db_name + "_host")), 
                database=(os.getenv(db_name + "_database")), 
                user=(os.getenv(db_name + "_user")), 
                password=(os.getenv(db_name + "_password")), 
                port=(os.getenv(db_name + "_port"))
            )
        elif(os.getenv(db_name + "_connection_type") == "ORACLE"):
            locals()[db_name + "_dsn"] = cx_Oracle.makedsn(
                os.getenv(db_name + "_host"), 
                os.getenv(db_name + "_port"), 
                sid=os.getenv(db_name + "_sid")
            )
            data_store.suite[db_name + "_dbconn"] = cx_Oracle.connect(
                os.getenv(db_name + "_user"), 
                os.getenv(db_name + "_password"), 
                locals()[db_name + "_dsn"], 
                encoding="UTF-8"
            )
        print("Successfully connected to " + db_name + "!")


def execute_query(conn, fetch_no_of_retries, fetch_duration_interval_in_sec, query, minimum_expected_record_count):
    print("Script to run: \n" + query)
    Messages.write_message("Script to run: \n" + query)
    column_names = []
    records = []
    with conn.cursor() as cursor:
        for no_of_tries in range(fetch_no_of_retries):
            cursor.execute(query)
            records = cursor.fetchall()
            print("Query executed {} time(s). Expected record(s) count: {} vs. Actual record(s) found: {}".format(no_of_tries + 1, minimum_expected_record_count, len(records)))
            if (len(records) < minimum_expected_record_count):
                print("Sleeping for " + str(fetch_duration_interval_in_sec) + "seconds...")
                time.sleep(fetch_duration_interval_in_sec)
            else:
                break    
        else:
            if (len(records) < minimum_expected_record_count):
                print("Waited for {} seconds but only {} records were found.".format( ((no_of_tries + 1) * fetch_duration_interval_in_sec), len(records)) )
                Messages.write_message("Waiter for {} seconds but only {} records were found.".format( ((no_of_tries + 1 ) *fetch_duration_interval_in_sec), len(records)))
        column_names = [desc[0] for desc in cursor.description]

    formatted_records = []
    for record in records:
            formatted_records.append( dict((column_name, record_cell) for column_name, record_cell in zip(column_names, record)) )
    Messages.write_message("formatted_records: \n" + str(formatted_records))

    return formatted_records