from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponseBadRequest
from data_retriever.models import TimeQADataset, HotpotQADataset, TreeOfKnowledgeDataset
from HFDLSP.settings import DATASET_IDS
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .authentication.custom_auth import ApiKeyAuthentication
from .utils.api_key_utils import generate_api_key

@authentication_classes([ApiKeyAuthentication])
@permission_classes([IsAuthenticated])
def answer_view(request):
    new_api_key = generate_api_key()
    user_query = request.GET.get("query")
    dataset_id = request.GET.get("dataset")

    try:
        if not user_query:
            return HttpResponseBadRequest({"error": "No query provided."})
        if not dataset_id:
            return HttpResponseBadRequest({"error": "No dataset provided."})
        if not DATASET_IDS.get(dataset_id):
            return HttpResponseBadRequest({"error": "The dataset ID is invalid."})

        result = None
        if dataset_id == "tree_of_knowledge":
            dataset = TreeOfKnowledgeDataset.nodes.first_or_none(question=user_query)
            result = dataset.answer if dataset else None

        if dataset_id == "hotpot_qa":
            dataset = HotpotQADataset.nodes.first_or_none(question=user_query)
            result = dataset.answer if dataset else None

        if dataset_id == "time_qa":
            dataset = (
                TimeQADataset.nodes.first_or_none(question=user_query)
                .fetch_relations("answers")
                .answers.first_or_none()
            )
            result = dataset.value if dataset else None

        if result:
            return JsonResponse({"result": result})

        return JsonResponse({"result": "No answer found."})
    except Exception as e:
        print(e)
        return JsonResponse({"error": "An unknown error occurred."})
