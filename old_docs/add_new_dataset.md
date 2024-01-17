## Adding a new dataset

### Configure settings

- Add the dataset to data_retriever/settings.py. The key would be ID of the dataset and the value would be should be the name from Hugging face.

## Add fetch method

- In data_retriever/service.py, update the `fetch_huggingface_dataset` method by adding a new condition that fetches the data from hugging face.

## Add database insert method

- In data_retriever/service.py, update the `insert_dataset_into_neo4j` method by adding a new condition that adds the dataset into the Neo4j database.

And with that you should be able to add the dataset by running `python3 src/manage.py fetch_dataset --dataset <dataset_id>`
