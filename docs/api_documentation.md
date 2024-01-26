This page contains information about the APIs available in the project, you can check out the [Swagger documentation](https://hfdlsp.trenches.ai/swagger-ui/) for detailed information about each of the endpoints.

## Authentication

When setting up the app, you can add an environment variable `API_KEY` as specified in the project settings. This API Key is what you will need to provide when making API requests to the app via the `Authorization` header.

## Endpoints

### Dataset retrieval endpoint

`GET /fetch_dataset?dataset=<dataset_id>`

This endpoint allows you to add a new dataset from HuggingFace into your Neo4j database instance. The `dataset_id` should be provided as configured in your project settings.

### Dataset query endpoint

`GET /result?dataset=<dataset_id>&query=<query>`

This endpoint allows you to retrieve the result to a query from a dataset. The dataset needs to have first been added for you to be able to get a valid result.

For more information and sample requests and responses, please check out the Swagger API doc.
