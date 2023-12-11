from django.core.management.base import BaseCommand
from ...service import fetch_huggingface_dataset, insert_dataset_into_neo4j
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
            return self.stderr.write(
                self.style.ERROR(f"No such dataset: {dataset_name}")
            )

        try:
            dataset = fetch_huggingface_dataset(dataset_id)
        except Exception as e:
            return self.stderr.write(f"Unable to fetch dataset: {self.style.ERROR(e)}")

        try:
            insert_dataset_into_neo4j(dataset_id, dataset)
        except Exception as e:
            return self.stderr.write(f"Unable to save dataset: {self.style.ERROR(e)}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully fetched and inserted dataset: {dataset_name}"
            )
        )
