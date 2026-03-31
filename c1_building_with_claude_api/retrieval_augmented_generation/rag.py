import os
from typing import Literal

import voyageai

from c1_building_with_claude_api.retrieval_augmented_generation.chunk_text import (
    chunk_by_section,
)
from c1_building_with_claude_api.retrieval_augmented_generation.vectore_index import (
    VectorIndex,
)


def generate_embedding(
    client: voyageai.Client,
    chunks,
    input_type: Literal["query"] = "query",
    model: str = "voyage-3-large",
):
    is_list = isinstance(chunks, list)
    input = chunks if is_list else [chunks]
    result = client.embed(input, model, input_type)
    return result.embeddings if is_list else result.embeddings[0]


if __name__ == "__main__":
    client: voyageai.Client = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"))

    with open("./report.md", "r") as f:
        text = f.read()

    chunks = chunk_by_section(text)
    embeddings = generate_embedding(client, chunks)

    store = VectorIndex()

    for embedding, chunk in zip(embeddings, chunks):
        store.add_vector(embedding, {"content": chunk})

    user_query = "What did the software engineering department did last year?"
    user_embedding = generate_embedding(client, user_query)

    results = store.search(user_embedding, 2)

    for doc, distance in results:
        print(distance, "\n", doc["content"][:200], "\n")
