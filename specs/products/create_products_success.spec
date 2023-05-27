# Testing for VALID Products

Creation of valid data for basic feature API

table:/step_impl/inputs/products/create_valid_products.csv

## Successful scenarios for features API
Tags: features, ff
For successful creation of features

* Assemble product <prod_testCaseID> <prod_testCase>
* Assemble product objects <prod_code> <version> <active> <category> <name> <description> <sla> <owner_contact_mob> <owner_contact_email> <requiredFeatures_code> <requiredFeatures_version> <requiredFeatures_configs> <optionalFeatures_code> <optionalFeatures_version> <optionalFeatures_configs> <features_configs>
* Request post valid products
* Base product table query
* The product request response code is "200"
* Assert that the base product is created
* Required features table query for product
* Assert that the required feature is created for product
* Optional features table query for product
* Assert that the optional feature is created for product