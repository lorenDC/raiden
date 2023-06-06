# Testing for INVALID Products

Creation of valid data for basic feature API

table:/step_impl/inputs/products/create_invalid_products.csv

## Declined scenarios for products API
Tags: products, pp
For declined creation of products

* Assemble product <prod_testCaseID> <prod_testCase>
* Assemble product objects <prod_code> <version> <active> <category> <name> <description> <sla> <owner_contact_mob> <owner_contact_email> <requiredFeatures_code> <requiredFeatures_version> <requiredFeatures_configs> <optionalFeatures_code> <optionalFeatures_version> <optionalFeatures_configs> <product_configs>
* Assemble product validation <err_text_code> <err_field> <err_message>
* Request post valid products
* The product request response code is "400"
* The product request response error text code
* The product request response error field
* The product request response error message    