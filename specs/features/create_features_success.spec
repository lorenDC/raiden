# Testing for VALID Features

Creation of valid data for basic feature API

table:/step_impl/inputs/features/create_valid_features.csv

## Successful scenarios for features API
Tags: features, ff
For successful creation of features

* Assemble feature <feat_testCaseID> <feat_testCase>
* Assemble feature objects <feat_code> <version> <active> <category> <name> <description> <sla> <owner_contact_mob> <owner_contact_email> <requiredFeatures_code> <requiredFeatures_version> <requiredFeatures_configs> <optionalFeatures_code> <optionalFeatures_version> <optionalFeatures_configs> <features_configs>
* Request post valid features
* Base features table query
* The feature request response code is "200"
* Assert that the base feature is created
* Required features table query for features
* Assert that the required feature is created for features
* Optional features table query for features
* Assert that the optional feature is created for features