<img width="1200" height="1600" alt="image" src="https://github.com/user-attachments/assets/c30834f6-244a-44cd-917a-299ba1812791" />


# Create Azure AI Search Service
https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search

# Deploy Azure OpenAI [embeddings]
https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#embeddings

# Deploy Azure OpenAI [GPT 4]
https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#gpt-4o-and-gpt-4-turbo

# Setup local python enviroment

## init
uv init
## pull the dependencies
uv add -r requemements.txt

# Prepare data for the application

## Step 1 - Prepare data for split
In the main.py, run the block in the Step 1
```
print("Splitting chapters...")
split_file_by_token_count(input_file, output_text_chunks_directory)
```
## Step 2 - Split the files
In the main.py, run the block in the Step 1
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
```
print("Creating search index...")
create_search_index(search_index_name)
print(f"Search index '{search_index_name}' created.")
```
## Step 4 - Upload data to index
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
## Step 6 - Run the application
```uv run rag.py```
