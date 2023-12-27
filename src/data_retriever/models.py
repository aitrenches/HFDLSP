from django_neomodel import DjangoNode
from django.utils import timezone
from neomodel import (
    StringProperty,
    UniqueIdProperty,
    DateProperty,
    RelationshipTo,
)


class HuggingFaceDataset(DjangoNode):
    uid = UniqueIdProperty()
    created_at = DateProperty(default=timezone.now().date())


class TreeOfKnowledgeDataset(HuggingFaceDataset):
    question = StringProperty()
    answer = StringProperty()


class HotpotQADataset(HuggingFaceDataset):
    question = StringProperty()
    answer = StringProperty()
    context = StringProperty()


class TimeQAAnswer(DjangoNode):
    value = StringProperty()


class TimeQADataset(HuggingFaceDataset):
    question = StringProperty()
    answers = RelationshipTo(TimeQAAnswer, "Answer")
    context = StringProperty()
