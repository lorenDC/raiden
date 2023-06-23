# Testing for VALID Products

Creation of valid data for basic feature API

table:/step_impl/inputs/products/create_valid_products.csv

## Successful scenarios for features API
Tags: features, ff
For successful creation of features

* Assemble product <prod_testCaseID> <prod_testCase>
* Assemble product objects <prod_code> <version> <active> <category> <name> <description> <sla> <owner_contact_mob> <owner_contact_email> <requiredFeatures_code> <requiredFeatures_version> <requiredFeatures_configs> <optionalFeatures_code> <optionalFeatures_version> <optionalFeatures_configs> <features_configs>
* Request post valid products
* The product request response code is "200"
* Assert Top Level Product Parent
* Assert required feature for products connection
* Assert optional feature for products connection