from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponseBadRequest
from data_retriever.models import TimeQADataset, HotpotQADataset, TreeOfKnowledgeDataset
from HFDLSP.settings import DATASET_IDS
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title="HFDLSP API")


@require_GET
def answer_view(request):
    user_query = request.GET.get("query")
    dataset_id = request.GET.get("dataset")

    if not user_query:
        return HttpResponseBadRequest({"error": "No query provided."})
    if not dataset_id:
        return HttpResponseBadRequest({"error": "No dataset provided."})
    if not DATASET_IDS.get(dataset_id):
        return HttpResponseBadRequest({"error": "The dataset ID is invalid."})

    if dataset_id == "tree_of_knowledge":
        dataset = TreeOfKnowledgeDataset.objects.get(name=dataset_id).questions.filter(
            text=user_query
        )
        return JsonResponse({"result": dataset[0].answer})

    if dataset_id == "hotpot_qa":
        dataset = HotpotQADataset.objects.get(name=dataset_id).questions.filter(
            text=user_query
        )
        return JsonResponse({"result": dataset[0].answers.all()[0].text})

    if dataset_id == "time_qa":
        dataset = TimeQADataset.objects.get(name=dataset_id).questions.filter(
            text=user_query
        )
        return JsonResponse({"result": dataset[0].answers.all()[0].text})

    return JsonResponse({"result": "No answer found."})
