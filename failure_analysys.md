Objective
Evaluate the product manual RAG system, identify weak answers, classify failures, and apply improvements.

Failure Analysis
No.	Test question	Failure type	Suggested fix
1	How do I reset my password?	Retrieval	Improve query matching and retrieve the relevant account-management chunk.
2	How can I update my email address?	Retrieval	Improve search terms for account-management content.
3	How do I download an invoice?	Retrieval	Include invoice and billing synonyms in retrieval.
4	How can I request a refund?	Retrieval	Improve matching for refund and payment-related questions.
5	How do I track an order?	Retrieval	Improve matching for order status and tracking terms.
6	Why is the application crashing?	Retrieval	Match troubleshooting terms and error descriptions.
7	What is the warranty period?	Retrieval	Return "I don't know." if warranty information is absent from the manual.
8	What is the CEO's phone number?	Generation	Enforce the rule to answer only from retrieved context.
9	What is my bank account balance?	Generation	Refuse to invent personal information not found in the manual.
10	What is tomorrow's weather?	Generation	Return "I don't know." when the manual does not contain the answer.
Important: These are example failure scenarios, not confirmed observed failures. Replace them with actual weak answers and their retrieved chunks after testing.

Improvements Applied
Split the PDF into chunks using RecursiveCharacterTextSplitter with chunk size 512 and overlap 50.

Stored page metadata in Chroma for source tracking.

Retrieved the top three chunks for each question.

Added a keyword matching threshold to reject questions with insufficient matching evidence.

Added an "I don't know." response for unsupported questions.

Returned source page information with answers.

Validation
The local test script reported 10/10 basic checks passing. This verifies expected response behavior, not complete factual accuracy.

Limitations
The current implementation uses local retrieval and keyword rules. It does not use a real LLM to generate answers or select tools. The failure scenarios above must be tested before they can be reported as actual failures.


