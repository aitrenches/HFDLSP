## Documentation

## Initial Project Setup

- Create a Neo4j database instance.
- Clone the project on Github
- Copy the existing .env.sample file by running `cp .env.sample .env`
- Update the `NEO4J_DATABASE_URL` to your created Neo4j database instance. 

### Add dataset to your application

- Select a dataset from the list of datasets, and add it to your Neo4j database by running `python3 src/manage.py fetch_dataset --dataset <dataset-name>`
- Verify that the dataset has been added to your database.

### Available Datasets

- `wikipedia`
- `tree-of-knowledge`
- `hotpot_qa`
- `timeQA`

## Start the server

Start the app server by running `python3 src/manage.py startapp`.