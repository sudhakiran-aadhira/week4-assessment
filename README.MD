Customer Support AI Assistant
1. Purpose
This project demonstrates a customer support assistant that answers product-manual questions, classifies support tickets, and handles sample customer and order queries.

2. Architecture
User / UI
    |
    v
FastAPI Application
    |
    +---- /ask ------> Chroma Vector Store
    |                    |
    |                    v
    |              Product Manual PDF
    |
    +---- /classify -> Local Ticket Classification Rules
    |
    +---- /chat -----> Sample CRM Tool / Order Tool
                           |
                           v
                       PostgreSQL or SQLite
Note: The current project uses local keyword rules and retrieval. It does not currently use a real LLM. The sample order database is SQLite (orders.db), not PostgreSQL.

3. Requirements
Python 3.12

Project dependencies installed in a virtual environment

Product manual at documents/product_manual.pdf

4. Setup
Open PowerShell in the project directory:

cd C:\Users\DELL5400\Desktop\customer-support-ai
py -m venv .venv
.\.venv\Scripts\Activate.ps1
Install the dependencies used by the project:

pip install fastapi uvicorn pypdf langchain-text-splitters sentence-transformers chromadb requests
5. Environment Variables
No trainer-provided LLM API key was available. The current local implementation does not require an LLM API key. Never commit secret keys or the .env file.

6. Run the API
py -m uvicorn task4:app --reload
Open the interactive API page:

http://127.0.0.1:8000/docs

7. Example Requests
Product manual question
POST /ask

{"question": "How can I reset my password?"}
Ticket classification
POST /classify

{"ticket": "I was charged twice"}
Customer/order chat
POST /chat

{"message": "Which plan is customer 2 on?"}
Unsupported question
POST /ask

{"question": "What is the CEO's personal phone number?"}
The expected behavior for unsupported questions is I don't know.

8. Tests
The local test script reported 10/10 basic checks passing. These checks do not establish complete factual accuracy or real LLM functionality.

Run the API in one terminal and the test script in another:

py test_task4.py
9. Limitations
Ticket classification uses local keyword rules.

Document answers use retrieval and keyword matching.

Chat tool selection uses local rules for sample scenarios.

Real LLM-generated answers and model-based tool selection are not implemented.

The failure-analysis examples must be validated against actual observed failures.

10. Demo Plan
Show a product-manual question using /ask.

Show ticket classification using /classify.

Show a sample customer or order query using /chat.

Ask an unsupported question and demonstrate the refusal.

Explain the current limitations honestly.