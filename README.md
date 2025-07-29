<img width="477" height="643" alt="Screenshot 2025-07-29 at 10 54 23" src="https://github.com/user-attachments/assets/a6a180d4-b519-43cf-96ef-c67aa790347d" />

# Audi Q5 Manual Q&A with Azure AI Search & GPT-4o
This project demonstrates how to build a Retrieval-Augmented Generation (RAG) pipeline using:

Azure AI Search

Azure AI Foundry

Azure OpenAI (text-embedding-large-3, GPT-4o)

Audi Q5 Manual as Source Data

Local Python Environment with uv

LLM to generate meaningful responses from indexed manual data

We upload the Audi Q5 owner's manual to Azure AI Search and use GPT-4o to generate intelligent answers to user questions based on the manual.


# Create Azure AI Search Service
Provision an Azure AI Search instance via the Azure portal or CLI.
You'll use this to index and query your Audi Q5 manual.
https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search

# Deploy Azure OpenAI [embeddings]
https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#embeddings

# Deploy Azure OpenAI [GPT 4]
-Embeddings Model: text-embedding-ada-002 or text-embedding-large-3
-LLM Model: gpt-4o
Ensure both models are deployed in the Azure OpenAI Studio and ready for use.
https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#gpt-4o-and-gpt-4-turbo

# Setup local python enviroment
We're using uv for dependency management.
## init
uv init
## pull the dependencies
uv add -r requemements.txt

# Prepare data for the application

## Step 1 - Prepare data for splitting
Open main.py and run the first block to split the manual into token-limited chunks.
```
print("Splitting chapters...")
split_file_by_token_count(input_file, output_text_chunks_directory)
```
## Step 2 - Split the files
Ensure the chunks are generated and stored in the specified directory.
```
with open("chunks.json", "r") as f:
    chapters = json.load(f)
# Process each chapter and save the chunk object to a JSON file
print("Processing chapters...")
for i, chapter in enumerate(chapters):
    print(f"Processing chapter {i+1}/{len(chapters)}: {chapter['file']}")
    chunk = get_chunk_object(chapter, output_text_chunks_directory)

    file_name = chapter["file"].split(".")[0]

    print("Write file...")
    # write chunk into JSON file into output directory
    with open(f"{output_vector_chunks_directory}/{file_name}.json", "w") as f:
        json.dump(chunk, f, indent=4)
```
## Step 3 - Create an index
Use the SDK or REST API to define and create your index schema.
```
print("Creating search index...")
create_search_index(search_index_name)
print(f"Search index '{search_index_name}' created.")
```
## Step 4 - Upload data to index
Upload the tokenized chunks to Azure AI Search using batch operations.
```
print("Uploading chunks to search index...")
list_of_files = os.listdir(output_vector_chunks_directory)
for file in list_of_files:
    print(file)
    if file.endswith(".json"):
        filepath = os.path.join(output_vector_chunks_directory, file)
        upload_chunk_document(filepath, search_index_name)
        print(f"Uploaded {file} to search index.")
```

## Step 5 - Test the Azure AI Search
```uv run generate_api_response_json.py```
## Step 6 - Run the Full RAG application
```uv run rag.py```

# Ask questions :

“Why tire pressure warning ?”

<img width="979" height="292" alt="Screenshot 2025-07-29 at 11 10 22" src="https://github.com/user-attachments/assets/2e0e3290-fbbc-414d-97f6-f5b81ee0c63a" />


The system searches the manual using Azure AI Search and generates a clear, LLM-enhanced response via GPT-4o.
