from django.http import JsonResponse
from django.views.decorators.http import require_GET
from HFDLSP.settings import DATASET_IDS
from .service import fetch_huggingface_dataset, insert_dataset_into_neo4j


@require_GET
def fetch_dataset_view(request):
    dataset_id = request.GET.get("dataset")
    if dataset_id not in DATASET_IDS:
        return JsonResponse(
            {"success": False, "error": "The dataset ID is invalid."}, status=400
        )
    dataset = fetch_huggingface_dataset(dataset_id)
    try:
        insert_dataset_into_neo4j(dataset_id, dataset)
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "success": False,
                "error": "Error while inserting dataset into Neo4j.",
            },
            status=500,
        )
    return JsonResponse({"success": True, "message": "Dataset inserted into Neo4j."})
