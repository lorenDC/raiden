from getgauge.python import data_store, Messages
import requests
import step_impl.conn_db as conn_db
import time, copy, os

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

# def string_format(data):
#     if "<timestamp>" in data:
#         return data.replace("<timestamp>", data_store.suite.datetimestamp)


#builder for features connection
def build_requiredFeatures_conn():

    # get current connections
    response = requests.get(os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/connections/" + data_store.suite.feature_request_body['requiredFeatures'][0]['code'] + "/" + data_store.suite.feature_request_body['requiredFeatures'][0]['version'])

    if(response.status_code == 200):
        data_store.scenario.response_conn = response.json()
        # declaring new list
        requiredFeatures_conn = []

        # # creating a clone of list
        for conn in data_store.scenario.response_conn:
            requiredFeatures_conn.append(conn)

        # conn payload
        type = data_store.suite.feature_type
        name = data_store.suite.feature_request_body['name']
        code = data_store.suite.feature_request_body['code']
        version = data_store.suite.feature_request_body['version']

        blueprint= {
            "type": type,
            "required": True,
            "name": name,
            "code": code,
            "version": version
        }
        
        requiredFeatures_conn.append(blueprint)
        data_store.suite.requiredFeatures_builder = requiredFeatures_conn
        print(f"[PASS] Required Feature Connection Builder!")
    else:
        data_store.suite.requiredFeatures_builder = (f"[FAIL] CHECK REQUIRED FEATURE!")
       
    return(data_store.suite.requiredFeatures_builder)

def build_optionalFeatures_conn():

    # get current connections
    response = requests.get(os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/connections/" + data_store.
    suite.feature_request_body['optionalFeatures'][0]['code'] + "/" + data_store.suite.feature_request_body['optionalFeatures'][0]['version'])
    
    if(response.status_code == 200):
        data_store.scenario.response_conn = response.json()
        # declaring new list
        optionalFeatures_conn = []

        # # creating a clone of list
        for conn in data_store.scenario.response_conn:
            optionalFeatures_conn.append(conn)

        # conn payload
        type = data_store.suite.feature_type
        name = data_store.suite.feature_request_body['name']
        code = data_store.suite.feature_request_body['code']
        version = data_store.suite.feature_request_body['version']

        blueprint= {
            "type": type,
            "required": False,
            "name": name,
            "code": code,
            "version": version
        }
        
        optionalFeatures_conn.append(blueprint)
        data_store.suite.optionalFeatures_builder = optionalFeatures_conn
        print(f"[PASS] Optional Feature Connection Builder!")
    else:
        data_store.suite.optionalFeatures_builder = (f"[FAIL] CHECK OPTIONAL FEATURE!")
       
    return(data_store.suite.optionalFeatures_builder)

#builder for products connection
def build_requiredProducts_conn():

    # get current connections
    response = requests.get(os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/connections/" + data_store.suite.product_request_body['requiredFeatures'][0]['code'] + "/" + data_store.suite.product_request_body['requiredFeatures'][0]['version'])

    if(response.status_code == 200):
        data_store.scenario.response_conn = response.json()
        # declaring new list
        requiredFeatures_conn = []

        # # creating a clone of list
        for conn in data_store.scenario.response_conn:
            requiredFeatures_conn.append(conn)

        # conn payload
        type = data_store.suite.product_type
        name = data_store.suite.product_request_body['name']
        code = data_store.suite.product_request_body['code']
        version = data_store.suite.product_request_body['version']

        blueprint= {
            "type": type,
            "required": True,
            "name": name,
            "code": code,
            "version": version
        }
        
        requiredFeatures_conn.append(blueprint)
        data_store.suite.requiredFeatures_builder = requiredFeatures_conn
        print(f"[PASS] Required Feature Connection Builder!")
    else:
        data_store.suite.requiredFeatures_builder = (f"[FAIL] CHECK REQUIRED FEATURE!")
       
    return(data_store.suite.requiredFeatures_builder)

def build_optionaProducts_conn():

    # get current connections
    response = requests.get(os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/connections/" + data_store.
    suite.product_request_body['optionalFeatures'][0]['code'] + "/" + data_store.suite.product_request_body['optionalFeatures'][0]['version'])
    
    if(response.status_code == 200):
        data_store.scenario.response_conn = response.json()
        # declaring new list
        optionalFeatures_conn = []

        # # creating a clone of list
        for conn in data_store.scenario.response_conn:
            optionalFeatures_conn.append(conn)

        # conn payload
        type = data_store.suite.product_type
        name = data_store.suite.product_request_body['name']
        code = data_store.suite.product_request_body['code']
        version = data_store.suite.product_request_body['version']

        blueprint= {
            "type": type,
            "required": False,
            "name": name,
            "code": code,
            "version": version
        }
        
        optionalFeatures_conn.append(blueprint)
        data_store.suite.optionalFeatures_builder = optionalFeatures_conn
        print(f"[PASS] Optional Feature Connection Builder!")
    else:
        data_store.suite.optionalFeatures_builder = (f"[FAIL] CHECK OPTIONAL FEATURE!")
       
    return(data_store.suite.optionalFeatures_builder)