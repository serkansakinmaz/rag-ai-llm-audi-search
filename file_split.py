import os
import json

import tiktoken

MAX_TOKENS = 1000  # Maximum number of tokens for chunks


def num_tokens_from_string(string: str) -> int:
    """
    Returns the number of tokens in a string using the cl100k_base encoding."""

    encoding = tiktoken.get_encoding(encoding_name="cl100k_base")
    num_tokens = len(encoding.encode(string, disallowed_special=()))
    return num_tokens


def split_content_into_chunks(content: str, max_tokens: int) -> list:
    """
    Splits the content into smaller chunks, each with a maximum of `max_tokens` tokens.
    """
    encoding = tiktoken.get_encoding(encoding_name="cl100k_base")
    tokens = encoding.encode(content, disallowed_special=())
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk = encoding.decode(chunk_tokens)
        chunks.append(chunk)
        start = end

    return chunks


def split_file_by_token_count(input_file: str, output_dir: str, max_tokens: int = MAX_TOKENS):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    chunks = split_content_into_chunks(content, max_tokens)

    chunk_metadata = []
    for i, chunk in enumerate(chunks):
        filename = f"chunk_{i + 1:03}.txt"
        path = os.path.join(output_dir, filename)

        with open(path, "w", encoding="utf-8") as out_file:
            out_file.write(chunk)

        chunk_metadata.append({
            "chunk": i + 1,
            "file": filename,
            "tokens": num_tokens_from_string(chunk)
        })

    with open("chunks.json", "w", encoding="utf-8") as json_file:
        json.dump(chunk_metadata, json_file, indent=4)

    print(f"✅ Splitting completed! {len(chunks)} chunks saved to '{output_dir}'.")
