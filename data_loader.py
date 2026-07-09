from google import genai
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv

# Load environment variables (ensure GEMINI_API_KEY is in your .env file)
load_dotenv()

# Initialize the Gemini client
client = genai.Client()

# Chunk it: break it down in smaller pieces and then embed those smaller pieces.
# Updated to Gemini's current active embedding model and dimensions
EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 3072

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)


def load_and_chunk_pdf(path: str):
    """Fetches the pdf, then loads it and chunks the text."""
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, "text", None)]
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Sends a request to Gemini, passes all the chunked texts,
    embeds them into vectors, and pulls out the numerical embeddings.
    """
    # Gemini uses 'contents' instead of 'input'
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=texts,
    )

    # Extract the embedding values from the response
    return [item.values for item in response.embeddings]

# Example Usage:
# if __name__ == "__main__":
#     chunks = load_and_chunk_pdf("sample.pdf")
#     embeddings = embed_texts(chunks)
#     print(f"Generated {len(embeddings)} embeddings of dimension {len(embeddings[0])}")