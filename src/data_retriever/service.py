from datasets import load_dataset


def fetch_huggingface_dataset(dataset_id):
    if dataset_id == "wikipedia":
        try:
            dataset = load_dataset("roneneldan/TinyStories")
            return dataset
        except Exception as e:
            print(e)
    elif dataset_id == "roneneldan/TinyStories":
        try:
            dataset = load_dataset("roneneldan/TinyStories")
            return dataset
        except Exception as e:
            print(e)
    return None
