from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponseBadRequest
from data_retriever.models import TimeQADataset
from HFDLSP.settings import DATASET_IDS


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

    dataset = None
    if dataset_id == DATASET_IDS["TimeQADataset"]:
        dataset = TimeQADataset.objects.get(name=dataset_id).questions.filter(
            text=user_query
        )

    if not dataset:
        return JsonResponse({"result": "No answer found."})

    answer = dataset[0].answers.all()[0].text
    return JsonResponse({"result": answer})
