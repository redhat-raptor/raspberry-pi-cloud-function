[![Build Status](https://dev.azure.com/redhatraptor/redhatraptor/_apis/build/status/redhat-raptor.raspberry-pi-cloud-function?branchName=main)](https://dev.azure.com/redhatraptor/redhatraptor/_build/latest?definitionId=1&branchName=main)

# raspberry-pi-cloud-function

This repo uses Serverless framework to:
1. Create HTTP endpoints
1. HTTP endpoints trigger Azure functions
1. Azure functions validate the requests and insert data into Azure CosmosDB
