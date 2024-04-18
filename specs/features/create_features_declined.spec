# Testing for INVALID Features

Creation of valid data for basic feature API

table: step_impl/inputs/features/create_invalid_features.csv

## Declined scenarios for features API	
Tags: features, ff	
For declined creation of features

* Assemble feature <feat_testCaseID> <feat_testCase>
* Assemble feature objects <feat_code> <version> <active> <category> <name> <description> <sla> <owner_contact_mob> <owner_contact_email> <requiredFeatures_code> <requiredFeatures_version> <requiredFeatures_configs> <optionalFeatures_code> <optionalFeatures_version> <optionalFeatures_configs> <features_configs>
* Assemble feature validation <err_text_code> <err_field> <err_message>
* Request post valid features
* The feature request response code is "400"
* The feature request response error text code
* The feature request response error field
* The feature request response error message    