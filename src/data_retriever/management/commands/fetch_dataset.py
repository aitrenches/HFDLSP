from django.core.management.base import BaseCommand
from ...service import fetch_huggingface_dataset
from ...settings import DATASET_IDS


class Command(BaseCommand):
    help = "Fetch a dataset from Hugging Face and insert it into Neo4j"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dataset",
            type=str,
            help="Hugging Face dataset (default: wikipedia)",
        )

    def handle(self, *args, **kwargs):
        dataset_name = kwargs["dataset"].lower()
        dataset_id = DATASET_IDS.get(dataset_name)

        if not dataset_id:
            self.stderr.write(self.style.ERROR(f"Unknown dataset: {dataset_name}"))
            return

        dataset = fetch_huggingface_dataset(dataset_id)
        if not dataset:
            self.stderr.write(
                self.style.ERROR(f"Failed to fetch dataset: {dataset_name}")
            )
            return
        print(dataset["train"])
        # neo4j_instance = insert_dataset_into_neo4j(dataset)

        # self.stdout.write(
        #     self.style.SUCCESS(
        #         f"Successfully fetched and inserted dataset: {neo4j_instance.name}"
        #     )
        # )
