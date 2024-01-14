from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import api_view
from HFDLSP.decorators import api_key_auth
from HFDLSP.settings import DATASET_IDS
from .service import fetch_huggingface_dataset, insert_dataset_into_neo4j


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="dataset",
            description="The ID of the dataset to import from HuggingFace to the Neo4j database.",
            required=True,
            type=str,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    "Example 1",
                    value="tree_of_knowledge",
                ),
            ],
        ),
    ],
    responses={
        200: {
            "properties": {
                "result": {
                    "type": "string",
                    "description": "A success mesage containing the result of the operation.",
                },
            },
        },
        500: {
            "properties": {
                "error": {
                    "type": "string",
                    "description": "The error that occured while trying to import the dataset.",
                },
            },
        },
        400: {
            "properties": {
                "error": {
                    "type": "string",
                    "description": "The error that occured as a result of an invalid dataset ID.",
                },
            },
        },
    },
)
@api_key_auth
@api_view(["GET"])
def fetch_dataset_view(request):
    dataset_id = request.GET.get("dataset")
    if dataset_id not in DATASET_IDS:
        return JsonResponse({"error": "The dataset ID is invalid."}, status=400)
    dataset = fetch_huggingface_dataset(dataset_id)
    try:
        insert_dataset_into_neo4j(dataset_id, dataset)
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "error": "Error while inserting dataset into Neo4j.",
            },
            status=500,
        )
    return JsonResponse({"result": "Dataset inserted into Neo4j."})
