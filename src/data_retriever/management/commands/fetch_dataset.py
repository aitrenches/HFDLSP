from django.core.management.base import BaseCommand
from ...service import fetch_huggingface_dataset, insert_dataset_into_neo4j
from HFDLSP.settings import DATASET_IDS


class Command(BaseCommand):
    help = "Fetch a dataset from Hugging Face and insert it into Neo4j"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dataset",
            type=str,
            help="Hugging Face dataset",
        )

    def handle(self, *args, **kwargs):
        dataset_id = kwargs["dataset"].lower()

        if not DATASET_IDS.get(dataset_id):
            return self.stderr.write(f"No such dataset: {dataset_id}")

        self.stdout.write(f"Fetching dataset: {dataset_id}")
        try:
            dataset = fetch_huggingface_dataset(dataset_id)
        except Exception as e:
            return self.stdout.write(f"Unable to fetch dataset: {self.style.ERROR(e)}")

        self.stdout.write(
            f"The dataset size is: {dataset.data.nbytes / 1e9} GB. Do you want to continue? [y/N]]"
        )

        if input("").lower() != "y":
            return self.stdout.write(self.style.NOTICE("Operation cancelled."))

        self.stdout.write(f"Inserting dataset: {dataset_id} into Neo4j")

        try:
            insert_dataset_into_neo4j(dataset_id, dataset)
        except Exception as e:
            return self.stderr.write(f"Unable to insert dataset: {self.style.ERROR(e)}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully fetched and inserted dataset: {dataset_id}"
            )
        )
