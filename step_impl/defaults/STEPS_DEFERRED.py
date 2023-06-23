# [DEFFERED] STEP FOR BLUEPRINT TABLE QUERY
# @step("Base product table query")
# def get_feature_request():

#     response = requests.get(os.getenv("isolated_test_protocol") + "://" + (os.getenv("isolated_test_domain")) + ":" + (os.getenv("isolated_test_port")) + "/products/" + data_store.suite.product_request_body['code'] + "/" + data_store.suite.product_request_body['version'])

#     data_store.scenario.get_product_request_response = response.json()
#     print(data_store.scenario.get_product_request_response)

#     Messages.write_message(data_store.scenario.get_product_request_response)

# [DEFERRED] STEP FOR REQUIRED FEATURES TABLE QUERY
# @step("Required features table query for product")
# def required_features_script():

#     query = "SELECT * \
#             FROM required_features \
#             WHERE owning_id = " + "'" + data_store.scenario.get_product_request_response['id'] + "' \
#             AND code = " + "'" + data_store.scenario.requiredFeatures[0]['code'] + "' \
#             AND version = " + "'" + data_store.scenario.requiredFeatures[0]['version'] + "' \
#             LIMIT 1"
    
#     data_store.scenario.required_features_records = execute_query(data_store.suite.db_product_registry_dbconn, data_store.suite.db_fetch_no_of_retries, data_store.suite.db_fetch_duration_interval, query, 1)
#     print(f"data_store.scenario.required_features_records: {data_store.scenario.required_features_records}")

# [DEFERRED] STEP FOR REQUIRED FEATURES TABLE ASSERTION
# @continue_on_failure([])
# @step("Assert that the required feature is created for product")
# def required_features_checking():
        
#         soft_assert(
#             data_store.scenario.get_product_request_response['id'] == data_store.scenario.required_features_records[0]['owning_id'], "data_store.scenario.get_product_request_response['id']: {} != data_store.scenario.required_features_records[0]['owning_id']: {}".format(data_store.scenario.get_product_request_response['id'], data_store.scenario.required_features_records[0]['owning_id'] )
#         )
        
#         soft_assert(
#             data_store.scenario.requiredFeatures[0]['code'] == data_store.scenario.required_features_records[0]['code'], "data_store.scenario.requiredFeatures[0]['code']: {} != data_store.scenario.required_features_records[0]['code']: {}".format(data_store.scenario.requiredFeatures[0]['code'], data_store.scenario.required_features_records[0]['code'] )
#         )

#         soft_assert(
#             data_store.scenario.requiredFeatures[0]['version'] == data_store.scenario.required_features_records[0]['version'], "data_store.scenario.requiredFeatures[0]['version']: {} != data_store.scenario.required_features_records[0]['version']: {}".format(data_store.scenario.requiredFeatures[0]['version'], data_store.scenario.required_features_records[0]['version'] )
#         )

#         verify_expectations()

# [DEFERRED] STEP FOR REQUIRED FEATURES TABLE QUERY
# @step("Optional features table query for product")
# def optional_feature_script():

#     query = "SELECT * \
#             FROM optional_features \
#             WHERE owning_id = " + "'" + data_store.scenario.get_product_request_response['id'] + "' \
#             AND code = " + "'" + data_store.scenario.optionalFeatures[0]['code'] + "' \
#             AND version = " + "'" + data_store.scenario.optionalFeatures[0]['version'] + "' \
#             LIMIT 1"
    
#     data_store.scenario.optional_features_records = execute_query(data_store.suite.db_product_registry_dbconn, data_store.suite.db_fetch_no_of_retries, data_store.suite.db_fetch_duration_interval, query, 1)
#     print(f"data_store.scenario.optional_features_records: {data_store.scenario.optional_features_records}")

# [DEFERRED] STEP FOR OPTIONAL FEATURES TABLE ASSERTION
# @continue_on_failure([])
# @step("Assert that the optional feature is created for product")
# def optional_features_checking():
     
#         soft_assert(
#             data_store.scenario.get_product_request_response['id'] == data_store.scenario.optional_features_records[0]['owning_id'], "data_store.scenario.get_product_request_response['id']: {} != data_store.scenario.optional_features_records[0]['owning_id']: {}".format(data_store.scenario.get_product_request_response['id'], data_store.scenario.optional_features_records[0]['owning_id'] )
#         )
        
#         soft_assert(
#             data_store.scenario.optionalFeatures[0]['code'] == data_store.scenario.optional_features_records[0]['code'], "data_store.scenario.optionalFeatures[0]['code']: {} != data_store.scenario.optional_features_records[0]['code']: {}".format(data_store.scenario.optionalFeatures[0]['code'], data_store.scenario.optional_features_records[0]['code'] )
#         )

#         soft_assert(
#             data_store.scenario.optionalFeatures[0]['version'] == data_store.scenario.optional_features_records[0]['version'], "data_store.scenario.optionalFeatures[0]['version']: {} != data_store.scenario.optional_features_records[0]['version']: {}".format(data_store.scenario.optionalFeatures[0]['version'], data_store.scenario.optional_features_records[0]['version'] )
#         )

#         verify_expectations()