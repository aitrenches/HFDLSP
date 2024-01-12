from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponseBadRequest
from data_retriever.models import TimeQADataset, HotpotQADataset, TreeOfKnowledgeDataset
from HFDLSP.settings import DATASET_IDS
from data_retriever.models import TimeQADataset, HotpotQADataset, TreeOfKnowledgeDataset


@require_GET
def answer_view(request):
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
            dataset = TreeOfKnowledgeDataset.nodes.first_or_none(
                question=user_query)
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


@require_GET
def fetch_dataset_from_neo4j(request, dataset_name):
    user_query = request.GET.get("query")

    try:
        if not user_query or not dataset_name:
            return HttpResponseBadRequest({"error": "No query provided."})

        timeQADataset = TimeQADataset.nodes.first_or_none(question=user_query)
        result_time = TimeQADataset.answers.value if timeQADataset else None

        if result_time:
            return JsonResponse({"result": result_time})

        hotpotQADataset = HotpotQADataset.nodes.first_or_none(
            question=user_query)
        result_hotpot = HotpotQADataset.answer if hotpotQADataset else None

        if result_hotpot:
            return JsonResponse({"result": result_hotpot})

        treeOfKnowledgeDataset = TreeOfKnowledgeDataset.nodes.first_or_none(
            question=user_query)
        result_tree = TreeOfKnowledgeDataset.answer if treeOfKnowledgeDataset else None

        if result_tree:
            return JsonResponse({"result": result_tree})

        return JsonResponse({"result": "No answer found."})
    except Exception as e:
        print(e)
        return JsonResponse({"error": "An unknown error occurred."})
