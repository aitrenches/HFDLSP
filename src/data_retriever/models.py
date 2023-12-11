from django_neomodel import DjangoNode
from neomodel import StringProperty, UniqueIdProperty


class HuggingFaceDataset(DjangoNode):
    uid = UniqueIdProperty()


class TreeOfKnowledgeDataset(HuggingFaceDataset):
    instruction = StringProperty()
    output = StringProperty()
