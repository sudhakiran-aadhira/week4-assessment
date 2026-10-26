Objective
Analyze possible failures in the Product Manual RAG Assistant and document fixes.

Test question	Possible failure type	Reason	Fix applied or planned
How do I reset my password?	Retrieval	The correct password instructions may not be among the top 3 chunks.	Use top-3 retrieval and preserve page metadata.
Where can I update my email address?	Retrieval	The relevant Account Management chunk may not rank first.	Improve query wording and verify retrieved chunks.
Where can I view invoices?	Generation	Retrieved text may not be converted into a clear answer.	Return the relevant retrieved text directly.
What if payment is deducted twice?	Retrieval	The question wording may differ from the manual.	Test alternate wording and review retrieval results.
How can I track my order?	Retrieval	The Order Tracking chunk may not be retrieved.	Check the retrieved chunks and adjust retrieval if needed.
What if the mobile app crashes?	Retrieval	The question may not match the manual wording closely enough.	Use semantic embeddings and top-3 retrieval.
What is the CEO's birthday?	Generation / refusal	The system might answer despite the manual not containing this information.	Return "I don't know." when evidence is insufficient.
What is the company's office address?	Generation / refusal	The retrieved text may be unrelated to the question.	Apply a relevance threshold before answering.
How many employees does the company have?	Generation / refusal	The manual does not provide the employee count.	Refuse unsupported questions.
What is the CEO's phone number?	Generation / refusal	The manual does not contain this information.	Return "I don't know." when evidence is insufficient.
Fix implemented
The /ask endpoint retrieves up to 3 chunks from Chroma and preserves the source page number. A keyword-overlap threshold was added to reject weak matches and return "I don't know." when evidence is insufficient.

Validation
The test script test_task4.py runs 6 answerable and 4 unanswerable questions. Its actual PASS/FAIL results should be reviewed before claiming the assistant meets the target.

Note: Failure types above are initial hypotheses. Confirm each one by comparing the retrieved chunks with the expected answer before submitting.

