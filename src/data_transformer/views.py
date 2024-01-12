from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponseBadRequest
from data_retriever.models import TimeQADataset, HotpotQADataset, TreeOfKnowledgeDataset
from HFDLSP.settings import DATASET_IDS
from data_retriever.models import TimeQADataset, HotpotQADataset, TreeOfKnowledgeDataset
from data_retriever.service import fetch_huggingface_dataset
from dotenv import load_dotenv
import os
import requests


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
def fetch_dataset_from_huggingface(request, dataset_id):
    try:
        api_key = request.headers.get("Authorization")

        if not api_key:
            return JsonResponse({"error": "API key is missing"}, status=401)

        if not validate_api_key(api_key):
            return JsonResponse({"error": "Invalid API key"}, status=401)

        huggingface_dataset = fetch_huggingface_dataset(dataset_id)

        huggingface_data = process_dataset(
            name=dataset_id, data=huggingface_dataset)
        huggingface_data.save()

        process_dataset(huggingface_dataset, dataset_id)

        return JsonResponse({"status": "success", "message": f"Fetching dataset for {dataset_id}."})
    except Exception as e:
        print(e)
        return JsonResponse({"error": "An unknown error occurred."})


def validate_api_key(api_key):
    return api_key == os.getenv("SECRET_KEY")


def process_dataset(huggingface_dataset, dataset_name):
    if dataset_name == "tree_of_knowledge":
        process_tree_of_knowledge_dataset(huggingface_dataset)
    elif dataset_name == "hotpot_qa":
        process_hotpot_qa_dataset(huggingface_dataset)
    elif dataset_name == "time_qa":
        process_time_qa_dataset(huggingface_dataset)


def process_tree_of_knowledge_dataset(huggingface_dataset):
    question = huggingface_dataset.get("question")
    answer = huggingface_dataset.get("answer")
    tree_of_knowledge_data = TreeOfKnowledgeDataset(
        question=question, answer=answer)
    tree_of_knowledge_data.save()


def process_hotpot_qa_dataset(huggingface_dataset):
    question = huggingface_dataset.get("question")
    answer = huggingface_dataset.get("answer")
    context = huggingface_dataset.get("context")
    hotpot_qa_data = HotpotQADataset(
        question=question, answer=answer, context=context)
    hotpot_qa_data.save()


def process_time_qa_dataset(huggingface_dataset):
    question = huggingface_dataset.get("question")
    answers = huggingface_dataset.get("answers", [])

    # Adjust context as needed
    time_qa_data = TimeQADataset(question=question, context="Some context")
    time_qa_data.save()

    for answer in answers:
        value = answer.get("value")
        time_qa_answer = TimeQADataset(value=value)
        time_qa_data.answers.connect(time_qa_answer)
