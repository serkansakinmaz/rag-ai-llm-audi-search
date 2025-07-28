import uuid
import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import EmbeddingsClient

load_dotenv("./.env", override=True)

api_key = os.getenv("EMBEDDINGS_MODEL_KEY")
endpoint = os.getenv("AZURE_AI_ENDPOINT_EMBEDDINGS")
embeddings_model_deployment = os.getenv("EMBEDDINGS_MODEL_DEPLOYMENT")


def get_client():

    client = EmbeddingsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))
    return client


def get_embeddings_vector(text):
    print("Call embeddings vector...")
    response = get_client().embed(input=text, model=embeddings_model_deployment)

    embedding = response.data[0].embedding

    print("Return embedding ...")

    return embedding


def get_chunk_object(chapter: dict, input_directory) -> dict:
    print("Open file")
    with open(f"{input_directory}/{chapter['file']}", "r") as f:
        chunk_content = f.read()
        vector = get_embeddings_vector(chunk_content)

    return {
        "id": str(uuid.uuid4()),
        "file": chapter["file"],
        "chunk_content": chunk_content,
        "vector": vector,
    }
