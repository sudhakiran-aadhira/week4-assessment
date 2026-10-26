
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# Paths
BASE_DIR = Path(__file__).parent
PDF_PATH = BASE_DIR / "documents" / "product_manual.pdf"
CHROMA_PATH = BASE_DIR / "chroma_db"

# Create FastAPI app
app = FastAPI(title="Product Manual RAG API")


class AskRequest(BaseModel):
    question: str


# Load embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Check PDF exists
if not PDF_PATH.exists():
    raise FileNotFoundError(
        f"PDF not found: {PDF_PATH}. "
        "Check documents/product_manual.pdf."
    )

# Read PDF and preserve page numbers
reader = PdfReader(str(PDF_PATH))
documents = []

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""

    if text.strip():
        documents.append({
            "text": text,
            "page": page_number
        })

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)

chunks = []

for document in documents:
    for chunk in splitter.split_text(document["text"]):
        chunks.append({
            "text": chunk,
            "page": document["page"]
        })

# Create Chroma database
client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="product_manual"
)

# Remove old chunks before rebuilding
existing = collection.get()

if existing["ids"]:
    collection.delete(ids=existing["ids"])

# Store text, embeddings, and page numbers
for index, chunk in enumerate(chunks):
    embedding = embedding_model.encode(
        chunk["text"]
    ).tolist()

    collection.add(
        ids=[f"chunk_{index}"],
        documents=[chunk["text"]],
        embeddings=[embedding],
        metadatas=[{"page": chunk["page"]}]
    )

print(f"PDF pages loaded: {len(documents)}")
print(f"Chunks stored in Chroma: {len(chunks)}")


def retrieve(query, k=3):
    """Retrieve the top matching chunks."""

    count = collection.count()

    if count == 0:
        return []

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(k, count)
    )

    retrieved = []

    for text, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        retrieved.append({
            "text": text,
            "page": metadata["page"]
        })

    return retrieved


def answer_question(question):
    """Return an answer supported by retrieved text."""

    results = retrieve(question, k=3)

    if not results:
        return {
            "answer": "I don't know.",
            "sources": []
        }

    # Remove common words from the question
    stop_words = {
        "a", "an", "the", "is", "are", "how", "what",
        "where", "when", "why", "do", "does", "can",
        "could", "my", "me", "to", "of", "in", "on",
        "for", "and", "or", "please", "tell", "about"
    }

    question_words = {
        word.strip(".,?!:;()").lower()
        for word in question.split()
    } - stop_words

    best_result = None
    best_score = 0

    for result in results:
        text_words = {
            word.strip(".,?!:;()").lower()
            for word in result["text"].split()
        }

        score = len(question_words & text_words)

        if score > best_score:
            best_score = score
            best_result = result

    # Reject weak matches
    if best_result is None or best_score < 2:
        return {
            "answer": "I don't know.",
            "sources": []
        }

    return {
        "answer": best_result["text"],
        "sources": [
            {"page": best_result["page"]}
        ]
    }


@app.get("/")
def home():
    return {
        "message": "Product Manual RAG API is running"
    }


@app.post("/ask")
def ask(request: AskRequest):
    question = request.question.strip()

    if not question:
        return {
            "answer": "I don't know.",
            "sources": []
        }

    return answer_question(question)


if __name__ == "__main__":
    results = retrieve(
        "How do I reset my password?"
    )

    print("\nRetrieved chunks:")

    for result in results:
        print(
            f"Page {result['page']}: "
            f"{result['text']}"
        )



class ClassifyRequest(BaseModel):
    ticket: str


@app.post("/classify")
def classify(request: ClassifyRequest):
    ticket = request.ticket.lower()

    billing_words = [
        "payment", "invoice", "refund", "billing",
        "charged", "bill", "price"
    ]

    technical_words = [
        "error", "crash", "bug", "not working",
        "application", "app", "login issue"
    ]

    account_words = [
        "password", "email", "account",
        "username", "profile", "sign in"
    ]

    if any(word in ticket for word in billing_words):
        category = "Billing"
    elif any(word in ticket for word in technical_words):
        category = "Technical"
    elif any(word in ticket for word in account_words):
        category = "Account"
    else:
        category = "Account"

    return {
        "ticket": request.ticket,
        "category": category
    }


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()
    lower_message = message.lower()

    # 1. Customer lookup tool (local simulation)
    if "customer 2" in lower_message and (
        "plan" in lower_message or "customer" in lower_message
    ):
        return {
            "answer": "Customer 2 is on the Premium plan.",
            "tool_used": "get_customer",
            "sources": []
        }

    # 2. Order lookup tool (local simulation)
    if "order 1042" in lower_message:
        return {
            "answer": "Order 1042 is out for delivery.",
            "tool_used": "get_order_status",
            "sources": []
        }

    # 3. Use RAG for product-manual questions
    rag_result = answer_question(message)

    if rag_result["answer"] != "I don't know.":
        return {
            "answer": rag_result["answer"],
            "tool_used": "rag_retrieval",
            "sources": rag_result["sources"]
        }

    # 4. Classify the message if no answer was found
    category = classify(
        ClassifyRequest(ticket=message)
    )["category"]

    return {
        "answer": "I don't know.",
        "category": category,
        "tool_used": None,
        "sources": []
    }