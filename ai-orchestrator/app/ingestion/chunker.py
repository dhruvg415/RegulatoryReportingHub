from typing import List, Dict
import tiktoken


def get_tokenizer(model: str = "text-embedding-3-large"):
    return tiktoken.encoding_for_model(model)


def chunk_text(
    text: str,
    max_tokens: int = 800,
    overlap: int = 100,
    model: str = "text-embedding-3-large"
) -> List[Dict]:
    """
    Split text into overlapping chunks suitable for embeddings.

    Returns:
        List of dicts:
        {
          "chunk_index": int,
          "text": str,
          "token_count": int
        }
    """
    tokenizer = get_tokenizer(model)
    tokens = tokenizer.encode(text)

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)

        chunks.append({
            "chunk_index": chunk_index,
            "text": chunk_text,
            "token_count": len(chunk_tokens)
        })

        chunk_index += 1
        start += max_tokens - overlap

    return chunks