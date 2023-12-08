from django_neomodel import DjangoNode
from neomodel import StringProperty


class HuggingFaceDataset(DjangoNode):
    name = StringProperty(unique_index=True)
