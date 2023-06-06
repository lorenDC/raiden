from getgauge.python import step, data_store, Messages, continue_on_failure
from smart_assertions import soft_assert, verify_expectations
from step_impl.conn_db import execute_query
import step_impl.common as common
import requests  
import os

##Assemble product testcases    
@step("Assemble product <prod_testCaseID> <prod_testCase>")
def feature_testCases(prod_testCaseID, prod_testCase):
    data_store.scenario.prod_testCaseID = prod_testCaseID
    data_store.scenario.prod_testCase = prod_testCase

##Assemble validation objects for feature
@step("Assemble product validation <err_text_code> <err_field> <err_message>")
def feature_validation(err_text_code,err_field,err_message):
     
    # store err_text_code
    data_store.scenario.err_text_code = err_text_code

    data_store.scenario.err_field = err_field

    # store err_message
    data_store.scenario.err_message = err_message

##Assemble objects for feature
@step("Assemble product objects <prod_code> <version> <active> <category> <name> <description> <sla> <owner_contact_mob> <owner_contact_email> <requiredFeatures_code> <requiredFeatures_version> <requiredFeatures_configs> <optionalFeatures_code> <optionalFeatures_version> <optionalFeatures_configs> <product_configs>")
def req_body(prod_code, version, active, category, name, description, sla, owner_contact_mob, owner_contact_email, requiredFeatures_code,requiredFeatures_version, requiredFeatures_configs,optionalFeatures_code,optionalFeatures_version,optionalFeatures_configs,product_configs):
    
    # format storing of version
    if not(version):
        data_store.scenario.product_version = common.parent_version('PRODUCT', prod_code)
    else:
        data_store.scenario.product_version = version      

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
    data_store.scenario.product_request_body = {
        "code": prod_code,
        "version": data_store.scenario.product_version,
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
        "configs": product_configs
    }
    print("data_store.scenario.request_body: {}".format(data_store.scenario.product_request_body))

@continue_on_failure([])
@step("Request post valid products")
def post_feature_request():
    response = requests.request(
        method= "POST",
        url= os.getenv("api_raiden_protocol") + "://" + (os.getenv("api_raiden_domain")) + "/products",
        json= data_store.scenario.product_request_body
    )

    # store response
    
    data_store.scenario.post_product_request_response_code = response.status_code

    if (response.status_code != 200):
        data_store.scenario.post_product_request_response = response.json()
    
        print(type(response.json()))
        print(response.json())

        Messages.write_message("Encountered error! {}".format(data_store.scenario.post_product_request_response))
    else:    
        Messages.write_message("The {code} {version} is added!".format(**data_store.scenario.product_request_body))

@step("Base product table query")
def get_feature_request():

    response = requests.get(os.getenv("api_raiden_protocol") + "://" + (os.getenv("api_raiden_domain")) + "/products/" + data_store.scenario.product_request_body['code'] + "/" + data_store.scenario.product_request_body['version'])

    data_store.scenario.get_product_request_response = response.json()
    print(data_store.scenario.get_product_request_response)

    Messages.write_message(data_store.scenario.get_product_request_response)
   

@continue_on_failure([])
@step("The product request response code is <response_code>")
def response_code_checking(response_code):

    soft_assert (
        data_store.scenario.post_product_request_response_code == int(response_code), "data_store.scenario.post_product_request_response_code: {} != response_code: {}".format(data_store.scenario.post_product_request_response_code, response_code)
    )

    verify_expectations()

    Messages.write_message("data_store.scenario.post_product_request_response_code: {} == response_code {}: ".format(data_store.scenario.post_product_request_response_code, response_code) )

@continue_on_failure([])
@step("Assert that the base product is created")
def base_product_checking():
        
        #code
        soft_assert(
            data_store.scenario.product_request_body['code'] == data_store.scenario.get_product_request_response['code'], "data_store.scenario.product_request_body['code']: {} != data_store.scenario.get_product_request_response['code']: {}".format(data_store.scenario.product_request_body['code'], data_store.scenario.get_product_request_response['code'])
        )

        # version
        soft_assert(
            data_store.scenario.product_request_body['version'] == data_store.scenario.get_product_request_response['version'], "data_store.scenario.product_request_body['version']: {} != data_store.scenario.get_product_request_response['version']: {}".format(data_store.scenario.product_request_body['version'], data_store.scenario.get_product_request_response['version'])
        )

        # active
        soft_assert(
            data_store.scenario.product_request_body['active'] == str(data_store.scenario.get_product_request_response['active']), "data_store.scenario.product_request_body['active']: {} != data_store.scenario.get_product_request_response['active']: {}".format(data_store.scenario.product_request_body['active'], str(data_store.scenario.get_product_request_response['active']))
        )

        # category
        soft_assert(
            data_store.scenario.product_request_body['category'] == data_store.scenario.get_product_request_response['category'], "data_store.scenario.product_request_body['category']: {} != data_store.scenario.get_product_request_response['category']: {}".format(data_store.scenario.product_request_body['category'], data_store.scenario.get_product_request_response['category'])
        )

        # name
        soft_assert(
            data_store.scenario.product_request_body['name'] == data_store.scenario.get_product_request_response['name'], "data_store.scenario.product_request_body['name']: {} != data_store.scenario.get_product_request_response['name']: {}".format(data_store.scenario.product_request_body['name'], data_store.scenario.get_product_request_response['name'])
        )

        # description
        soft_assert(
            data_store.scenario.product_request_body['description'] == data_store.scenario.get_product_request_response["description"], "data_store.scenario.product_request_body['description']: {} != data_store.scenario.get_product_request_response['description']: {}".format(data_store.scenario.product_request_body['description'], data_store.scenario.get_product_request_response['description'])
        )  

        #sla
        soft_assert(
            data_store.scenario.product_request_body['sla'] == data_store.scenario.get_product_request_response['sla'], "data_store.scenario.product_request_body['sla']: {} != data_store.scenario.get_product_request_response['sla']: {}".format(data_store.scenario.product_request_body['sla'], data_store.scenario.get_product_request_response['sla'])
        )

        #ownerContactDetails - mobileNumber
        soft_assert(
            data_store.scenario.product_request_body['ownerContactDetails']['mobileNumber'] == data_store.scenario.get_product_request_response['ownerContactDetails']['mobileNumber'], "data_store.scenario.product_request_body['ownerContactDetails']['mobileNumber']: {} != data_store.scenario.get_product_request_response['ownerContactDetails']['mobileNumber']: {}".format(data_store.scenario.product_request_body['ownerContactDetails']['mobileNumber'], data_store.scenario.get_product_request_response['ownerContactDetails']['mobileNumber'])
        )

        #ownerContactDetails - email
        soft_assert(
            data_store.scenario.product_request_body['ownerContactDetails']['email'] == data_store.scenario.get_product_request_response['ownerContactDetails']['email'], "data_store.scenario.product_request_body['ownerContactDetails']['email']: {} != data_store.scenario.get_product_request_response['owner_contact_email']: {}".format(data_store.scenario.product_request_body['ownerContactDetails']['email'], data_store.scenario.get_product_request_response['ownerContactDetails']['email'])
        )

        verify_expectations()

@step("Required features table query for product")
def required_features_script():

    query = "SELECT * \
            FROM required_features \
            WHERE owning_id = " + "'" + data_store.scenario.get_product_request_response['id'] + "' \
            AND code = " + "'" + data_store.scenario.requiredFeatures[0]['code'] + "' \
            AND version = " + "'" + data_store.scenario.requiredFeatures[0]['version'] + "' \
            LIMIT 1"
    
    data_store.scenario.required_features_records = execute_query(data_store.suite.db_product_registry_dbconn, data_store.suite.db_fetch_no_of_retries, data_store.suite.db_fetch_duration_interval, query, 1)
    print(f"data_store.scenario.required_features_records: {data_store.scenario.required_features_records}")

@continue_on_failure([])
@step("Assert that the required feature is created for product")
def required_features_checking():
        
        soft_assert(
            data_store.scenario.get_product_request_response['id'] == data_store.scenario.required_features_records[0]['owning_id'], "data_store.scenario.get_product_request_response['id']: {} != data_store.scenario.required_features_records[0]['owning_id']: {}".format(data_store.scenario.get_product_request_response['id'], data_store.scenario.required_features_records[0]['owning_id'] )
        )
        
        soft_assert(
            data_store.scenario.requiredFeatures[0]['code'] == data_store.scenario.required_features_records[0]['code'], "data_store.scenario.requiredFeatures[0]['code']: {} != data_store.scenario.required_features_records[0]['code']: {}".format(data_store.scenario.requiredFeatures[0]['code'], data_store.scenario.required_features_records[0]['code'] )
        )

        soft_assert(
            data_store.scenario.requiredFeatures[0]['version'] == data_store.scenario.required_features_records[0]['version'], "data_store.scenario.requiredFeatures[0]['version']: {} != data_store.scenario.required_features_records[0]['version']: {}".format(data_store.scenario.requiredFeatures[0]['version'], data_store.scenario.required_features_records[0]['version'] )
        )

        verify_expectations()

@step("Optional features table query for product")
def optional_feature_script():

    query = "SELECT * \
            FROM optional_features \
            WHERE owning_id = " + "'" + data_store.scenario.get_product_request_response['id'] + "' \
            AND code = " + "'" + data_store.scenario.optionalFeatures[0]['code'] + "' \
            AND version = " + "'" + data_store.scenario.optionalFeatures[0]['version'] + "' \
            LIMIT 1"
    
    data_store.scenario.optional_features_records = execute_query(data_store.suite.db_product_registry_dbconn, data_store.suite.db_fetch_no_of_retries, data_store.suite.db_fetch_duration_interval, query, 1)
    print(f"data_store.scenario.optional_features_records: {data_store.scenario.optional_features_records}")

@continue_on_failure([])
@step("Assert that the optional feature is created for product")
def optional_features_checking():
     
        soft_assert(
            data_store.scenario.get_product_request_response['id'] == data_store.scenario.optional_features_records[0]['owning_id'], "data_store.scenario.get_product_request_response['id']: {} != data_store.scenario.optional_features_records[0]['owning_id']: {}".format(data_store.scenario.get_product_request_response['id'], data_store.scenario.optional_features_records[0]['owning_id'] )
        )
        
        soft_assert(
            data_store.scenario.optionalFeatures[0]['code'] == data_store.scenario.optional_features_records[0]['code'], "data_store.scenario.optionalFeatures[0]['code']: {} != data_store.scenario.optional_features_records[0]['code']: {}".format(data_store.scenario.optionalFeatures[0]['code'], data_store.scenario.optional_features_records[0]['code'] )
        )

        soft_assert(
            data_store.scenario.optionalFeatures[0]['version'] == data_store.scenario.optional_features_records[0]['version'], "data_store.scenario.optionalFeatures[0]['version']: {} != data_store.scenario.optional_features_records[0]['version']: {}".format(data_store.scenario.optionalFeatures[0]['version'], data_store.scenario.optional_features_records[0]['version'] )
        )

        verify_expectations()


#negative testing
@continue_on_failure([])
@step("The product request response error text code")
def error_text_code():

    soft_assert(
         data_store.scenario.post_product_request_response['errors'][0]['code'] == data_store.scenario.err_text_code, "data_store.scenario.post_product_request_response['errors'][0]['code'] {} != data_store.scenario.err_text_code: {}".format(data_store.scenario.post_product_request_response['errors'][0]['code'], data_store.scenario.err_text_code)
    )
    verify_expectations()

    Messages.write_message("data_store.scenario.post_product_request_response['errors'][0]['code'] {} == data_store.scenario.err_text_code: {}".format(data_store.scenario.post_product_request_response['errors'][0]['code'], data_store.scenario.err_text_code))

@continue_on_failure([])
@step("The product request response error field")
def error_field():
     
    soft_assert(
        data_store.scenario.post_product_request_response['errors'][0]['field'] == data_store.scenario.err_field, "data_store.scenario.post_product_request_response['errors'][0]['field']: {} != data_store.scenario.err_field: {}".format(data_store.scenario.post_product_request_response['errors'][0]['field'], data_store.scenario.err_field)
    )

    Messages.write_message("data_store.scenario.post_product_request_response['errors'][0]['field']: {} == data_store.scenario.err_field: {}".format(data_store.scenario.post_product_request_response['errors'][0]['field'], data_store.scenario.err_text_code))

@continue_on_failure([])
@step("The product request response error message")
def error_message():
     
     soft_assert(
          data_store.scenario.post_product_request_response['errors'][0]['errorMessage'] == data_store.scenario.err_message, "data_store.scenario.post_product_request_response['errors'][0]['errorMessage']: {} != data_store.scenario.err_message: {}".format(data_store.scenario.post_product_request_response['errors'][0]['errorMessage'], data_store.scenario.err_message)
     )
     verify_expectations()

     Messages.write_message("data_store.scenario.post_product_request_response['errors'][0]['errorMessage']: {} == data_store.scenario.err_message: {}".format(data_store.scenario.post_product_request_response['errors'][0]['errorMessage'], data_store.scenario.err_message))