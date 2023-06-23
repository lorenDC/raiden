from getgauge.python import step, data_store, Messages, continue_on_failure
from smart_assertions import soft_assert, verify_expectations
from step_impl.conn_db import execute_query
from step_impl.common import build_requiredFeatures_conn, build_optionalFeatures_conn
import requests  
import os
import time


##Assemble feature testcases
@step("Assemble feature <feat_testCaseID> <feat_testCase>")
def feature_testCases(feat_testCaseID, feat_testCase):
    data_store.scenario.feat_testCaseID = feat_testCaseID
    data_store.scenario.feat_testCase = feat_testCase

##Assemble validation objects for feature
@step("Assemble feature validation <err_text_code> <err_field> <err_message>")
def feature_validation(err_text_code,err_field,err_message):
     
    # store err_text_code
    data_store.scenario.err_text_code = err_text_code

    data_store.scenario.err_field = err_field

    # store err_message
    data_store.scenario.err_message = err_message

##Assemble objects for feature
@step("Assemble feature objects <feat_code> <version> <active> <category> <name> <description> <sla> <owner_contact_mob> <owner_contact_email> <requiredFeatures_code> <requiredFeatures_version> <requiredFeature_configs> <optionalFeatures_code> <optionalFeatures_version> <optionalFeatures_configs> <features_configs>")
def req_body(feat_code, version, active, category, name, description, sla, owner_contact_mob, owner_contact_email, requiredFeatures_code,requiredFeatures_version, requiredFeatures_configs,optionalFeatures_code,optionalFeatures_version,optionalFeatures_configs,features_configs):

    ##[DEFERRED] format storing of version
    # if not(version):
    #     data_store.scenario.feature_version = common.parent_version('FEATURE', feat_code)
    # else:
    #     data_store.scenario.feature_version = version

    # store type
    data_store.suite.feature_type = 'FEATURE'

    # format storing of required features
    if not(requiredFeatures_code or requiredFeatures_version):
        requiredFeatures = []
        data_store.scenario.requiredFeatures = requiredFeatures
    else:
        data_store.scenario.requiredFeatures = [{
            "code": requiredFeatures_code,
            "version": requiredFeatures_version,
            "configs": requiredFeatures_configs
        }]

    # format storing of optional features   
    if not(optionalFeatures_code or optionalFeatures_version):
        optionalFeatures = []
        data_store.scenario.optionalFeatures = optionalFeatures
    else:
        data_store.scenario.optionalFeatures = [{
            "code": optionalFeatures_code,
            "version": optionalFeatures_version,
            "configs": optionalFeatures_configs
        }]

    # storing of request body
    data_store.suite.feature_request_body = {
        "code": feat_code,
        "version": version,
        "active": active,
        "category": category,
        "name": name,
        "description": description,
        "sla": sla,
        "ownerContactDetails": {
            "mobileNumber": owner_contact_mob,
            "email": owner_contact_email
        },
        "requiredFeatures": data_store.scenario.requiredFeatures,
        "optionalFeatures": data_store.scenario.optionalFeatures,
        "configs": features_configs
    }

    print(f"data_store.scenario.request_body: {data_store.suite.feature_request_body}")

    Messages.write_message(f"data_store.scenario.request_body: {data_store.suite.feature_request_body}")

@continue_on_failure([])
@step("Request post valid features")
def post_feature_request():

    if (data_store.scenario.requiredFeatures):
        build_requiredFeatures_conn()
    
    if (data_store.scenario.optionalFeatures):
        build_optionalFeatures_conn()

    response = requests.post(
        url=os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/features",
        json= data_store.suite.feature_request_body
    )

    time.sleep(20) 
    
    # store response  
    data_store.scenario.post_feature_request_response_code = response.status_code

    if (response.status_code != 200):
        data_store.scenario.post_feature_request_response = response.json()

        print(f"[FAIL] RESPONSE: {data_store.scenario.post_feature_request_response}")

        Messages.write_message(f"[FAIL] RESPONSE: {data_store.scenario.post_feature_request_response}")

    else:
        print(f"[PASS] STATUS {response.status_code}: {data_store.suite.feature_request_body['code']} & {data_store.suite.feature_request_body['version']}")
        
        Messages.write_message(f"[PASS] STATUS {response.status_code}: {data_store.suite.feature_request_body['code']} & {data_store.suite.feature_request_body['version']}")  
   
@continue_on_failure([])
@step("The feature request response code is <response_code>")
def response_code_checking(response_code):

    soft_assert (
        data_store.scenario.post_feature_request_response_code == int(response_code), "[FAIL] data_store.scenario.feature_request_response_code: {} != response_code: {}".format(data_store.scenario.post_feature_request_response_code, response_code)
    )

    verify_expectations()

    print(f"[PASS] data_store.scenario.feature_request_response_code: {data_store.scenario.post_feature_request_response_code} == response_code {response_code}")

    Messages.write_message("[PASS] data_store.scenario.feature_request_response_code: {} == response_code {}: ".format(data_store.scenario.post_feature_request_response_code, response_code))

@continue_on_failure([])
@step("Assert Top Level Feature Parent")
def feature_parent_assertions():
    
    response = requests.get(os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/features/" + data_store.suite.feature_request_body['code'] + "/" + data_store.suite.feature_request_body['version'])

    data_store.scenario.get_feature_request_response = response.json()
    print(f"[RESPONSE]: {data_store.scenario.get_feature_request_response}")

    Messages.write_message(f"[RESPONSE]: {data_store.scenario.get_feature_request_response}")
        
    #code
    soft_assert(
        data_store.suite.feature_request_body['code'] == data_store.scenario.get_feature_request_response['code'], "[FAIL] data_store.suite.feature_request_body['code']: {} != data_store.scenario.get_feature_request_response['code']: {}".format(data_store.suite.feature_request_body['code'], data_store.scenario.get_feature_request_response['code'])
    )

    print(f"[PASS] data_store.suite.feature_request_body['code']: {data_store.suite.feature_request_body['code']} == data_store.scenario.get_feature_request_response['code']: {data_store.scenario.get_feature_request_response['code']}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['code']: {data_store.suite.feature_request_body['code']} == data_store.scenario.get_feature_request_response['code']: {data_store.scenario.get_feature_request_response['code']}")

    # version
    soft_assert(
        data_store.suite.feature_request_body['version'] == data_store.scenario.get_feature_request_response['version'], "[FAIL] data_store.suite.feature_request_body['version']: {} != data_store.scenario.get_feature_request_response['version']: {}".format(data_store.suite.feature_request_body['version'], data_store.scenario.get_feature_request_response['version'])
    )

    print(f"[PASS] data_store.suite.feature_request_body['version']: {data_store.suite.feature_request_body['version']} == data_store.scenario.get_feature_request_response['version']: {data_store.scenario.get_feature_request_response['version']}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['version']: {data_store.suite.feature_request_body['version']} == data_store.scenario.get_feature_request_response['version']: {data_store.scenario.get_feature_request_response['version']}")

    # isActive
    soft_assert(
        data_store.suite.feature_request_body['active'] == str(data_store.scenario.get_feature_request_response['active']), "[FAIL] data_store.suite.feature_request_body['active']: {} != data_store.scenario.get_feature_request_response['active']: {}".format(data_store.suite.feature_request_body['active'], str(data_store.scenario.get_feature_request_response['active']))
    )

    print(f"[PASS] data_store.suite.feature_request_body['active']: {data_store.suite.feature_request_body['active']} == data_store.scenario.get_feature_request_response['active']: {str(data_store.scenario.get_feature_request_response['active'])}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['active']: {data_store.suite.feature_request_body['active']} == data_store.scenario.get_feature_request_response['active']: {str(data_store.scenario.get_feature_request_response['active'])}")

    # category
    soft_assert(
        data_store.suite.feature_request_body['category'] == data_store.scenario.get_feature_request_response['category'], "[FAIL] data_store.suite.feature_request_body['category']: {} != data_store.scenario.get_feature_request_response['category']: {}".format(data_store.suite.feature_request_body['category'], data_store.scenario.get_feature_request_response['category'])
    )

    print(f"[PASS] data_store.suite.feature_request_body['category']: {data_store.suite.feature_request_body['category']} == data_store.scenario.get_feature_request_response['category']: {data_store.scenario.get_feature_request_response['category']}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['category']: {data_store.suite.feature_request_body['category']} == data_store.scenario.get_feature_request_response['category']: {data_store.scenario.get_feature_request_response['category']}")

    # name
    soft_assert(
        data_store.suite.feature_request_body['name'] == data_store.scenario.get_feature_request_response['name'], "[FAIL] data_store.suite.feature_request_body['name']: {} != data_store.scenario.get_feature_request_response['name']: {}".format(data_store.suite.feature_request_body['name'], data_store.scenario.get_feature_request_response['name'])
    )

    print(f"[PASS] data_store.suite.feature_request_body['name']: {data_store.suite.feature_request_body['name']} == data_store.scenario.get_feature_request_response['name']: {data_store.scenario.get_feature_request_response['name']}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['name']: {data_store.suite.feature_request_body['name']} == data_store.scenario.get_feature_request_response['name']: {data_store.scenario.get_feature_request_response['name']}")    

    # description
    soft_assert(
        data_store.suite.feature_request_body['description'] == data_store.scenario.get_feature_request_response["description"], "[FAIL] data_store.suite.feature_request_body['description']: {} != data_store.scenario.get_feature_request_response['description']: {}".format(data_store.suite.feature_request_body['description'], data_store.scenario.get_feature_request_response['description'])
    ) 

    print(f"[PASS] data_store.suite.feature_request_body['description']: {data_store.suite.feature_request_body['description']} == data_store.scenario.get_feature_request_response['description']: {data_store.scenario.get_feature_request_response['description']}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['description']: {data_store.suite.feature_request_body['description']} == data_store.scenario.get_feature_request_response['description']: {data_store.scenario.get_feature_request_response['description']}")

    #sla
    soft_assert(
        data_store.suite.feature_request_body['sla'] == data_store.scenario.get_feature_request_response['sla'], "[FAIL] data_store.suite.feature_request_body['sla']: {} != data_store.scenario.base_feature_records['sla']: {}".format(data_store.suite.feature_request_body['sla'], data_store.scenario.get_feature_request_response['sla'])
    )

    print(f"[PASS] data_store.suite.feature_request_body['sla']: {data_store.suite.feature_request_body['sla']} == data_store.scenario.base_feature_records['sla']: {data_store.scenario.get_feature_request_response['sla']}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['sla']: {data_store.suite.feature_request_body['sla']} == data_store.scenario.base_feature_records['sla']: {data_store.scenario.get_feature_request_response['sla']}")    

    #ownerContactDetails - mobileNumber
    soft_assert(
        data_store.suite.feature_request_body['ownerContactDetails']['mobileNumber'] == data_store.scenario.get_feature_request_response['ownerContactDetails']['mobileNumber'], "[FAIL] data_store.suite.feature_request_body['ownerContactDetails']['mobileNumber']: {} != data_store.scenario.get_feature_request_response['ownerContactDetails']['mobileNumber']: {}".format(data_store.suite.feature_request_body['ownerContactDetails']['mobileNumber'], data_store.scenario.get_feature_request_response['ownerContactDetails']['mobileNumber'])
    )

    print(f"[PASS] data_store.suite.feature_request_body['ownerContactDetails']['mobileNumber']: {data_store.suite.feature_request_body['ownerContactDetails']['mobileNumber']} == data_store.scenario.get_feature_request_response['ownerContactDetails']['mobileNumber']: {data_store.scenario.get_feature_request_response['ownerContactDetails']['mobileNumber']}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['ownerContactDetails']['mobileNumber']: {data_store.suite.feature_request_body['ownerContactDetails']['mobileNumber']} == data_store.scenario.get_feature_request_response['ownerContactDetails']['mobileNumber']: {data_store.scenario.get_feature_request_response['ownerContactDetails']['mobileNumber']}")

    #ownerContactDetails - email
    soft_assert(
        data_store.suite.feature_request_body['ownerContactDetails']['email'] == data_store.scenario.get_feature_request_response['ownerContactDetails']['email'], "[FAIL] data_store.suite.feature_request_body['ownerContactDetails']['email']: {} != data_store.scenario.get_feature_request_response['owner_contact_email']: {}".format(data_store.suite.feature_request_body['ownerContactDetails']['email'], data_store.scenario.get_feature_request_response['ownerContactDetails']['email'])
    )

    print(f"[PASS] data_store.suite.feature_request_body['ownerContactDetails']['email']: {data_store.suite.feature_request_body['ownerContactDetails']['email']} == data_store.scenario.get_feature_request_response['owner_contact_email']: {data_store.scenario.get_feature_request_response['ownerContactDetails']['email']}")

    Messages.write_message(f"[PASS] data_store.suite.feature_request_body['ownerContactDetails']['email']: {data_store.suite.feature_request_body['ownerContactDetails']['email']} == data_store.scenario.get_feature_request_response['owner_contact_email']: {data_store.scenario.get_feature_request_response['ownerContactDetails']['email']}")

    #requiredFeatures
    if (data_store.scenario.requiredFeatures):
        #requiredFeatures_code
        soft_assert(
            data_store.scenario.requiredFeatures[0]['code'] == data_store.scenario.get_feature_request_response['requiredFeatures'][0]['code'], "[FAIL] data_store.scenario.requiredFeatures['code']: {} != data_store.scenario.get_feature_request_response['requiredFeatures']['code']: {}".format(data_store.scenario.requiredFeatures[0]['code'], data_store.scenario.get_feature_request_response['requiredFeatures'][0]['code'])
        )

        print(f"[PASS] data_store.scenario.requiredFeatures['code']: {data_store.scenario.requiredFeatures[0]['code']} == data_store.scenario.get_feature_request_response['requiredFeatures']['code']: {data_store.scenario.get_feature_request_response['requiredFeatures'][0]['code']}")

        Messages.write_message(f"[PASS] data_store.scenario.requiredFeatures['code']: {data_store.scenario.requiredFeatures[0]['code']} == data_store.scenario.get_feature_request_response['requiredFeatures']['code']: {data_store.scenario.get_feature_request_response['requiredFeatures'][0]['code']}")

        #requiredFeatures_version
        soft_assert(
            data_store.scenario.requiredFeatures[0]['version'] == data_store.scenario.get_feature_request_response['requiredFeatures'][0]['version'], "[FAIL] data_store.scenario.requiredFeatures[0]['version']: {} != data_store.scenario.get_feature_request_response['requiredFeatures'][0]['version']: {}".format(data_store.scenario.requiredFeatures[0]['version'], data_store.scenario.get_feature_request_response['requiredFeatures'][0]['version'])
        )

        print(f"[PASS] data_store.scenario.requiredFeatures[0]['version']: {data_store.scenario.requiredFeatures[0]['version']} == data_store.scenario.get_feature_request_response['requiredFeatures'][0]['version']: {data_store.scenario.get_feature_request_response['requiredFeatures'][0]['version']}")

        Messages.write_message(f"[PASS] data_store.scenario.requiredFeatures[0]['version']: {data_store.scenario.requiredFeatures[0]['version']} == data_store.scenario.get_feature_request_response['requiredFeatures'][0]['version']: {data_store.scenario.get_feature_request_response['requiredFeatures'][0]['version']}")
    else:
        #for null requiredFeature
        soft_assert(
            data_store.scenario.requiredFeatures == data_store.scenario.get_feature_request_response['requiredFeatures'], "[FAIL] data_store.scenario.requiredFeatures: {} != data_store.scenario.get_feature_request_response['requiredFeatures']: {}".format(data_store.scenario.requiredFeatures, data_store.scenario.get_feature_request_response['requiredFeatures'])
        )

    #optionalFeatures
    if (data_store.scenario.optionalFeatures):
        #optionalFeatures_code
        soft_assert(
            data_store.scenario.optionalFeatures[0]['code'] == data_store.scenario.get_feature_request_response['optionalFeatures'][0]['code'], "[FAIL] data_store.scenario.optionalFeatures[0]['code']: {} != data_store.scenario.get_feature_request_response['optionalFeatures'][0]['code']: {}".format(data_store.scenario.optionalFeatures[0]['code'], data_store.scenario.get_feature_request_response['optionalFeatures'][0]['code'])
        )

        print(f"[PASS] data_store.scenario.optionalFeatures[0]['code']: {data_store.scenario.optionalFeatures[0]['code']} == data_store.scenario.get_feature_request_response['optionalFeatures'][0]['code']: {data_store.scenario.get_feature_request_response['optionalFeatures'][0]['code']}")

        Messages.write_message(f"[PASS] data_store.scenario.optionalFeatures['code']: {data_store.scenario.optionalFeatures[0]['code']} == data_store.scenario.get_feature_request_response['optionalFeatures'][0]['code']: {data_store.scenario.get_feature_request_response['optionalFeatures'][0]['code']}")

        #optionalFeatures_version
        soft_assert(
            data_store.scenario.optionalFeatures[0]['version'] == data_store.scenario.get_feature_request_response['optionalFeatures'][0]['version'], "[FAIL] data_store.scenario.optionalFeatures[0]['version']: {} != data_store.scenario.get_feature_request_response['optionalFeatures'][0]['version']: {}".format(data_store.scenario.optionalFeatures[0]['version'], data_store.scenario.get_feature_request_response['optionalFeatures'][0]['version'])
        )

        print(f"[PASS] data_store.scenario.optionalFeatures[0]['version']: {data_store.scenario.optionalFeatures[0]['version']} == data_store.scenario.get_feature_request_response['optionalFeatures'][0]['version']: {data_store.scenario.get_feature_request_response['optionalFeatures'][0]['version']}")

        Messages.write_message(f"[PASS] data_store.scenario.optionalFeatures[0]['version']: {data_store.scenario.optionalFeatures[0]['version']} == data_store.scenario.get_feature_request_response['optionalFeatures'][0]['version']: {data_store.scenario.get_feature_request_response['optionalFeatures'][0]['version']}")
    else:
        #for null optionalFeature
        soft_assert(
            data_store.scenario.optionalFeatures == data_store.scenario.get_feature_request_response['optionalFeatures'], "[FAIL] data_store.scenario.optionalFeatures: {} != data_store.scenario.get_feature_request_response['optionalFeatures']: {}".format(data_store.scenario.requiredFeatures, data_store.scenario.get_feature_request_response['optionalFeatures'])
        )

    verify_expectations()

@continue_on_failure([])
@step("Assert required feature for features connection")
def required_features_script():

    if not(data_store.scenario.requiredFeatures == []):

        response = requests.get(os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/connections/" + data_store.scenario.requiredFeatures[0]['code'] + "/" + data_store.scenario.requiredFeatures[0]['version'])

        data_store.scenario.get_required_features_conn = response.json()

        expected_column_names = ["type", "required", "name", "code", "version"]

        soft_assert(
            list(data_store.scenario.get_required_features_conn[0].keys()) == expected_column_names, "[FAIL] data_store.scenario.get_required_features_conn[0].keys(): {} != expected_column_names: {}".format(data_store.scenario.get_required_features_conn[0].keys(), expected_column_names)
        )
    
        for i in range(len(data_store.scenario.get_required_features_conn)):
            for key in data_store.scenario.get_required_features_conn[i]:
                if key == 'type':
                    soft_assert(
                        data_store.scenario.get_required_features_conn[i][key] == data_store.suite.requiredFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_required_features_conn['type']: {} != data_store.suite.requiredFeatures_builder['type']: {}".format(data_store.scenario.get_required_features_conn[i][key], data_store.suite.requiredFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_required_features_conn['type']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['type']: {data_store.suite.requiredFeatures_builder[i].get(key)}")

                    Messages.write_message(f"[PASS] data_store.scenario.get_required_features_conn['type']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['type']: {data_store.suite.requiredFeatures_builder[i].get(key)}")

                elif key == 'required':
                    soft_assert(
                        data_store.scenario.get_required_features_conn[i][key] == data_store.suite.requiredFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_required_features_conn['required']: {} != data_store.suite.requiredFeatures_builder['required']: {}".format(data_store.scenario.get_required_features_conn[i][key], data_store.suite.requiredFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_required_features_conn['required']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['required']: {data_store.suite.requiredFeatures_builder[i].get(key)}")
                    
                    Messages.write_message(f"[PASS] data_store.scenario.get_required_features_conn['required']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['required']: {data_store.suite.requiredFeatures_builder[i].get(key)}")

                elif key == 'name':
                    soft_assert(
                        data_store.scenario.get_required_features_conn[i][key] == data_store.suite.requiredFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_required_features_conn['name']: {} != data_store.suite.requiredFeatures_builder['name']: {}".format(data_store.scenario.get_required_features_conn[i][key], data_store.suite.requiredFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_required_features_conn['name']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['name']: {data_store.suite.requiredFeatures_builder[i].get(key)}")  

                    Messages.write_message(f"[PASS] data_store.scenario.get_required_features_conn['name']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['name']: {data_store.suite.requiredFeatures_builder[i].get(key)}") 

                elif key == 'code':
                    soft_assert(
                        data_store.scenario.get_required_features_conn[i][key] == data_store.suite.requiredFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_required_features_conn['code']: {} != data_store.suite.requiredFeatures_builder['code']: {}".format(data_store.scenario.get_required_features_conn[i][key], data_store.suite.requiredFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_required_features_conn['code']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['code']: {data_store.suite.requiredFeatures_builder[i].get(key)}")  

                    Messages.write_message(f"[PASS] data_store.scenario.get_required_features_conn['code']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['code']: {data_store.suite.requiredFeatures_builder[i].get(key)}")

                elif key == 'version':
                    soft_assert(
                        data_store.scenario.get_required_features_conn[i][key] == data_store.suite.requiredFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_required_features_conn['version']: {} != data_store.suite.requiredFeatures_builder['version']: {}".format(data_store.scenario.get_required_features_conn[i][key], data_store.suite.requiredFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_required_features_conn['version']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['version']: {data_store.suite.requiredFeatures_builder[i].get(key)}")

                    Messages.write_message(f"[PASS] data_store.scenario.get_required_features_conn['version']: {data_store.scenario.get_required_features_conn[i][key]} == data_store.suite.requiredFeatures_builder['version']: {data_store.suite.requiredFeatures_builder[i].get(key)}")
    else:
        print(f"[INFO] No required features in payload: {data_store.scenario.requiredFeatures}")    

        Messages.write_message(f"[INFO] No required features in payload: {data_store.scenario.requiredFeatures}")

@continue_on_failure([])
@step("Assert optional feature for features connection")
def optional_features_script():

    if not(data_store.scenario.optionalFeatures == []):

        response = requests.get(os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/connections/" + data_store.scenario.optionalFeatures[0]['code'] + "/" + data_store.scenario.optionalFeatures[0]['version'])

        data_store.scenario.get_optional_features_conn = response.json()

        expected_column_names = ["type", "required", "name", "code", "version"]

        soft_assert(
            list(data_store.scenario.get_optional_features_conn[0].keys()) == expected_column_names, "[FAIL] data_store.scenario.get_optional_features_conn[0].keys(): {} != expected_column_names: {}".format(data_store.scenario.get_optional_features_conn[0].keys(), expected_column_names)
        )
    
        for i in range(len(data_store.scenario.get_optional_features_conn)):
            for key in data_store.scenario.get_optional_features_conn[i]:
                if key == 'type':
                    soft_assert(
                        data_store.scenario.get_optional_features_conn[i][key] == data_store.suite.optionalFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_optional_features_conn['type']: {} != data_store.suite.optionalFeatures_builder['type']: {}".format(data_store.scenario.get_optional_features_conn[i][key], data_store.suite.optionalFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_optional_features_conn['type']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['type']: {data_store.suite.optionalFeatures_builder[i].get(key)}")

                    Messages.write_message(f"[PASS] data_store.scenario.get_optional_features_conn['type']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['type']: {data_store.suite.optionalFeatures_builder[i].get(key)}")

                elif key == 'required':
                    soft_assert(
                        data_store.scenario.get_optional_features_conn[i][key] == data_store.suite.optionalFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_optional_features_conn['required']: {} != data_store.suite.optionalFeatures_builder['required']: {}".format(data_store.scenario.get_optional_features_conn[i][key], data_store.suite.optionalFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_optional_features_conn['required']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['required']: {data_store.suite.optionalFeatures_builder[i].get(key)}")

                    Messages.write_message(f"[PASS] data_store.scenario.get_optional_features_conn['required']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['required']: {data_store.suite.optionalFeatures_builder[i].get(key)}")

                elif key == 'name':
                    soft_assert(
                        data_store.scenario.get_optional_features_conn[i][key] == data_store.suite.optionalFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_optional_features_conn['name']: {} != data_store.suite.optionalFeatures_builder['name']: {}".format(data_store.scenario.get_optional_features_conn[i][key], data_store.suite.optionalFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_optional_features_conn['name']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['name']: {data_store.suite.optionalFeatures_builder[i].get(key)}") 

                    Messages.write_message(f"[PASS] data_store.scenario.get_optional_features_conn['name']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['name']: {data_store.suite.optionalFeatures_builder[i].get(key)}") 

                elif key == 'code':
                    soft_assert(
                        data_store.scenario.get_optional_features_conn[i][key] == data_store.suite.optionalFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_optional_features_conn['code']: {} != data_store.suite.optionalFeatures_builder['code']: {}".format(data_store.scenario.get_optional_features_conn[i][key], data_store.suite.optionalFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_optional_features_conn['code']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['code']: {data_store.suite.optionalFeatures_builder[i].get(key)}")  

                    Messages.write_message(f"[PASS] data_store.scenario.get_optional_features_conn['code']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['code']: {data_store.suite.optionalFeatures_builder[i].get(key)}")

                elif key == 'version':
                    soft_assert(
                        data_store.scenario.get_optional_features_conn[i][key] == data_store.suite.optionalFeatures_builder[i].get(key), "[FAIL] data_store.scenario.get_optional_features_conn['version']: {} != data_store.suite.optionalFeatures_builder['version']: {}".format(data_store.scenario.get_optional_features_conn[i][key], data_store.suite.optionalFeatures_builder[i].get(key))
                    )

                    print(f"[PASS] data_store.scenario.get_optional_features_conn['version']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['version']: {data_store.suite.optionalFeatures_builder[i].get(key)}")

                    Messages.write_message(f"[PASS] data_store.scenario.get_optional_features_conn['version']: {data_store.scenario.get_optional_features_conn[i][key]} == data_store.suite.optionalFeatures_builder['version']: {data_store.suite.optionalFeatures_builder[i].get(key)}")
    else:
        print(f"[INFO] No optional features in payload: {data_store.scenario.optionalFeatures}")    

        Messages.write_message(f"[INFO] No optional features in payload: {data_store.scenario.optionalFeatures}")                          

#negative testing
@continue_on_failure([])
@step("The feature request response error text code")
def error_text_code():

    soft_assert(
         data_store.scenario.post_feature_request_response['errors'][0]['code'] == data_store.scenario.err_text_code, "[FAIL] data_store.scenario.post_feature_request_response['errors'][0]['code']: {} != data_store.scenario.err_text_code: {}".format(data_store.scenario.post_feature_request_response['errors'][0]['code'], data_store.scenario.err_text_code)
    )
    
    print(f"[PASS] data_store.scenario.post_feature_request_response['errors'][0]['code']: {data_store.scenario.post_feature_request_response['errors'][0]['code']} == data_store.scenario.err_text_code: {data_store.scenario.err_text_code}")

    Messages.write_message(f"[PASS] data_store.scenario.post_feature_request_response['errors'][0]['code']: {data_store.scenario.post_feature_request_response['errors'][0]['code']} == data_store.scenario.err_text_code: {data_store.scenario.err_text_code}")

    verify_expectations()

@continue_on_failure([])
@step("The feature request response error field")
def error_field():
    
    soft_assert(
        data_store.scenario.post_feature_request_response['errors'][0]['field'] == data_store.scenario.err_field, "[FAIL] data_store.scenario.post_feature_request_response['errors'][0]['field']: {} != data_store.scenario.err_field: {}".format(data_store.scenario.post_feature_request_response['errors'][0]['field'], data_store.scenario.err_field)
    )

    print(f"[PASS] data_store.scenario.post_feature_request_response['errors'][0]['field']: {data_store.scenario.post_feature_request_response['errors'][0]['field']} == data_store.scenario.err_field: {data_store.scenario.err_field}")

    Messages.write_message(f"[PASS] data_store.scenario.post_feature_request_response['errors'][0]['field']: {data_store.scenario.post_feature_request_response['errors'][0]['field']} == data_store.scenario.err_field: {data_store.scenario.err_field}")

    verify_expectations()

@continue_on_failure([])
@step("The feature request response error message")
def error_message():
     
    soft_assert(
          data_store.scenario.post_feature_request_response['errors'][0]['errorMessage'] == data_store.scenario.err_message, "[FAIL] data_store.scenario.post_feature_request_response['errors'][0]['errorMessage']: {} != data_store.scenario.err_message: {}".format(data_store.scenario.post_feature_request_response['errors'][0]['errorMessage'], data_store.scenario.err_message)
    )
     
    print(f"[PASS] data_store.scenario.post_feature_request_response['errors'][0]['errorMessage'] {data_store.scenario.post_feature_request_response['errors'][0]['errorMessage']} == data_store.scenario.err_message: {data_store.scenario.err_message}")

    Messages.write_message(f"[PASS] data_store.scenario.post_feature_request_response['errors'][0]['errorMessage'] {data_store.scenario.post_feature_request_response['errors'][0]['errorMessage']} == data_store.scenario.err_message: {data_store.scenario.err_message}")

    verify_expectations()