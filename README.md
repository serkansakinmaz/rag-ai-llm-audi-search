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

## Step 1
In the main.py, run the block in the Step 1
```
print("Splitting chapters...")
split_file_by_token_count(input_file, output_text_chunks_directory)
```
