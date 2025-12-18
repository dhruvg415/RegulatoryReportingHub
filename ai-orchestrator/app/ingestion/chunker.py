import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")


def chunk_text(text: str, max_tokens: int = 800):
    words = text.split("\n")
    chunks = []
    current = []

    for line in words:
        current.append(line)
        tokens = len(tokenizer.encode("\n".join(current)))
        if tokens > max_tokens:
            chunks.append("\n".join(current[:-1]))
            current = [line]

    if current:
        chunks.append("\n".join(current))

    return chunks