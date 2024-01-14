from django.http import JsonResponse, HttpResponseBadRequest
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import api_view
from HFDLSP.decorators import api_key_auth
from HFDLSP.settings import DATASET_IDS
from .service import fetch_dataset_answer_by_question


@extend_schema(
    description="Get an answer to a question from a dataset.",
    methods=["GET"],
    parameters=[
        OpenApiParameter(
            name="query",
            description="The query/question you want to get an answer to.",
            required=True,
            type=str,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    "Example 1",
                    value="explain chemistry",
                ),
            ],
        ),
        OpenApiParameter(
            name="dataset",
            description="The ID of the dataset to query as specified in the app.",
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
                    "description": "The string containing the answer to the query.",
                },
            },
        },
        500: {
            "properties": {
                "error": {
                    "type": "string",
                    "description": "The error that occured while trying to fetch the answer to the query.",
                },
            },
        },
        400: {
            "properties": {
                "error": {
                    "type": "string",
                    "description": "The error that occured as a result of a bad input.",
                },
            },
        },
    },
)
@api_key_auth
@api_view(["GET"])
def answer_view(request):
    user_query = request.GET.get("query").lower()
    dataset_id = request.GET.get("dataset")

    try:
        if not user_query:
            return HttpResponseBadRequest({"error": "No query provided."})
        if not dataset_id:
            return HttpResponseBadRequest({"error": "No dataset provided."})
        if not DATASET_IDS.get(dataset_id):
            return HttpResponseBadRequest({"error": "The dataset ID is invalid."})

        result = fetch_dataset_answer_by_question(dataset_id, user_query)

        if not result:
            return JsonResponse({"result": "No answer found."})
        return JsonResponse({"result": result})
    except Exception as e:
        print(e)
        return JsonResponse({"error": "An unknown error occurred."})
