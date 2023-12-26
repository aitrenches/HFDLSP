from datasets import load_dataset
from neomodel import db
from .models import (
    TreeOfKnowledgeDataset,
    HotpotQADataset,
    TimeQADataset,
)

from HFDLSP.settings import DATASET_IDS


def fetch_huggingface_dataset(dataset_id):
    dataset_name = DATASET_IDS.get(dataset_id)
    if dataset_id == "tree_of_knowledge":
        return load_dataset(dataset_name, split="train")

    if dataset_id == "hotpot_qa":
        return load_dataset(dataset_name, "distractor", split="train")

    if dataset_id == "time_qa":
        return load_dataset(dataset_name, split="train")


def insert_dataset_into_neo4j(dataset_id, dataset):
    if dataset_id == "tree_of_knowledge":
        with db.transaction:
            for data in dataset:
                TreeOfKnowledgeDataset.create(
                    {
                        "question": data["instruction"],
                        "answer": data["output"],
                    }
                )

    if dataset_id == "hotpot_qa":
        with db.transaction:
            for data in dataset:
                HotpotQADataset.create(
                    {
                        "question": data["question"],
                        "answer": data["answer"],
                        "context": data["context"],
                    }
                )

    if dataset_id == "time_qa":
        with db.transaction:
            for data in dataset:
                TimeQADataset.create(
                    {
                        "question": data["question"],
                        "answer": data["targets"],
                        "context": data["context"],
                    }
                )
