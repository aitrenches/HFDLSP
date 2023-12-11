from datasets import load_dataset
from neomodel import db
from .models import TreeOfKnowledgeDataset


def fetch_huggingface_dataset(dataset_id):
    if dataset_id == "fblgit/tree-of-knowledge":
        dataset = load_dataset(dataset_id, split="train")
        return dataset


def insert_dataset_into_neo4j(dataset_id, dataset):
    if dataset_id == "fblgit/tree-of-knowledge":
        with db.transaction:
            for data in dataset:
                TreeOfKnowledgeDataset.create(data)
