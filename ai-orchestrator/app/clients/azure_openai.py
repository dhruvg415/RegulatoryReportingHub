import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)

GPT4O_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT4O")
EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_EMBEDDING")


def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text
    )
    return response.data[0].embedding


def chat(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=GPT4O_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content