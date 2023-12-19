from django_neomodel import DjangoNode
from django.utils import timezone
from neomodel import StringProperty, UniqueIdProperty, DateProperty


class HuggingFaceDataset(DjangoNode):
    uid = UniqueIdProperty()
    created_at = DateProperty(default=timezone.now().date())


class TreeOfKnowledgeDataset(HuggingFaceDataset):
    instruction = StringProperty()
    output = StringProperty()


class HotpotQADataset(HuggingFaceDataset):
    question = StringProperty()
    answer = StringProperty()
    type = StringProperty()
    level = StringProperty()
    supporting_facts = StringProperty()
    context = StringProperty()


class WikipediaDataset(HuggingFaceDataset):
    title = StringProperty()
    text = StringProperty()
    url = StringProperty()


class TimeQA(HuggingFaceDataset):
    level = StringProperty()
    question = StringProperty()
    idx = StringProperty()
    context = StringProperty()
