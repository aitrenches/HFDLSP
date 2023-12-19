from datasets import load_dataset
from neomodel import db
from .models import TreeOfKnowledgeDataset, HotpotQADataset, WikipediaDataset, TimeQA


def fetch_huggingface_dataset(dataset_id):
    if dataset_id == "wikipedia":
        return load_dataset("wikimedia/wikipedia", "20231101.en", split="train")

    if dataset_id == "fblgit/tree-of-knowledge":
        return load_dataset(dataset_id, split="train")

    if dataset_id == "hotpot_qa":
        return load_dataset(dataset_id, "distractor", split="train")
    
    if dataset_id == "timeQA":
        return load_dataset("hugosousa/TimeQA")


def insert_dataset_into_neo4j(dataset_id, dataset):
    if dataset_id == "wikipedia":
        with db.transaction:
            for data in dataset:
                WikipediaDataset.create(data)

    if dataset_id == "fblgit/tree-of-knowledge":
        with db.transaction:
            for data in dataset:
                TreeOfKnowledgeDataset.create(data)

    if dataset_id == "hotpot_qa":
        with db.transaction:
            for data in dataset:
                HotpotQADataset.create(data)
                
    if dataset_id == "timeQA":
        with db.transaction:
            for data in dataset:
                TimeQA.create(data)
