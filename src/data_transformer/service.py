from HFDLSP.models import TimeQADataset, HotpotQADataset, TreeOfKnowledgeDataset


def fetch_dataset_answer_by_question(dataset_id, question):
    if dataset_id == "tree_of_knowledge":
        dataset = TreeOfKnowledgeDataset.nodes.first_or_none(question=question)
        if dataset:
            return dataset.answer

    if dataset_id == "hotpot_qa":
        dataset = HotpotQADataset.nodes.first_or_none(question=question)
        if dataset:
            return dataset.answer

    if dataset_id == "time_qa":
        dataset = (
            TimeQADataset.nodes.first_or_none(question=question)
            .fetch_relations("answers")
            .answers.first_or_none()
        )
        if dataset:
            return dataset.value
