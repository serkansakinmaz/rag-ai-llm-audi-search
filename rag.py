import json
import os
from dotenv import load_dotenv

from openai import AzureOpenAI

load_dotenv("./.env", override=True)

api_key = os.getenv("AZURE_AI_KEY")
endpoint_ai = os.getenv("AZURE_AI_ENDPOINT")
api_key_ai_search = os.getenv("AI_SEARCH_KEY")
endpoint_ai_search = os.getenv("AI_SEARCH_ENDPOINT")
search_index_name = os.getenv("AI_SEARCH_INDEX")
deployment = os.getenv("AI_MODEL_DEPLOYMENT_NAME")
api_version = "2024-12-01-preview"


def get_openai_client():
    """
    Returns an instance of the AzureOpenAI client.
    """
    return AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint_ai,
        api_key=api_key,
    )


def get_response(messages):
    """
    Returns a response from the OpenAI client.
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        messages=messages,
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": endpoint_ai_search,
                        "index_name": search_index_name,
                        "authentication": {
                            "type": "api_key",
                            "key": api_key_ai_search,
                        },
                        "top_n_documents": 3,
                        "fields_mapping": {
                            "filepath_field": "file",
                            "content_fields": ["chunk_content"],
                            "vector_fields": ["vector"],
                        },
                    },
                }
            ]
        },
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=deployment,
    )
    return response


messages = [
    {
        "role": "system",
        "content": "You are an expert in the Audi Q5 Owner's Manual 2018 QS",
    }
]


while True:
    user_input = input("User: what is your question? (type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    messages.append({"role": "user", "content": user_input})

    client = get_openai_client()

    response = get_response(messages)
    print(response.choices[0].message.content)
    citations = response.choices[0].message.context["citations"]
    if citations:
        print("Citations:")
        for citation in citations:
            print(f" - {citation['title']}: {citation['filepath']}")
    else:
        print("No citations found.")
    messages.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )
