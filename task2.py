
import json
from pydantic import BaseModel, Field, ValidationError


# 1. Create the Pydantic model
class TicketInfo(BaseModel):
    customer_name: str
    product: str
    issue_type: str
    urgency: int = Field(ge=1, le=5)
    summary: str


# 2. Five free-text tickets
tickets = [
    "Priya reports that the mobile app crashes during login. Urgent.",
    "Rahul cannot download his invoice from the website.",
    "Anita wants to update her account email address.",
    "Kiran says the payment was deducted twice.",
    "Meena reports that the website is running very slowly."
]


# 3. Simulated model responses
# The first response is deliberately invalid to demonstrate retry.

def get_model_response(ticket, attempt, previous_error=None):
    # First ticket: simulate invalid urgency, then correct it
    if "Priya" in ticket:
        customer = {
            "customer_name": "Priya",
            "product": "Mobile App",
            "issue_type": "Technical",
            "urgency": 7 if attempt == 1 else 4,
            "summary": "App crashes during login"
        }

    elif "Rahul" in ticket:
        customer = {
            "customer_name": "Rahul",
            "product": "Website",
            "issue_type": "Technical",
            "urgency": 3,
            "summary": "Cannot download invoice"
        }

    elif "Anita" in ticket:
        customer = {
            "customer_name": "Anita",
            "product": "Account Portal",
            "issue_type": "Account",
            "urgency": 2,
            "summary": "Wants to update account email"
        }

    elif "Kiran" in ticket:
        customer = {
            "customer_name": "Kiran",
            "product": "Payment System",
            "issue_type": "Billing",
            "urgency": 5,
            "summary": "Payment deducted twice"
        }

    else:
        customer = {
            "customer_name": "Meena",
            "product": "Website",
            "issue_type": "Technical",
            "urgency": 3,
            "summary": "Website is running slowly"
        }

    return json.dumps(customer)


# 4. Validate and retry up to 3 times
def extract_ticket(ticket):
    for attempt in range(1, 4):
        response = get_model_response(ticket, attempt)

        try:
            result = TicketInfo.model_validate_json(response)
            print(f"Attempt {attempt}: success")
            return {
                "success": True,
                "data": result.model_dump()
            }

        except ValidationError as error:
            print(f"Attempt {attempt}: validation error")
            print(error)

            # In a real LLM workflow, send this error
            # back to the model for correction.
            if attempt < 3:
                print("Retrying with validation feedback...")

    return {
        "success": False,
        "error": "Failed validation after 3 attempts."
    }


# 5. Process five tickets
if __name__ == "__main__":
    for number, ticket in enumerate(tickets, start=1):
        print(f"\nTicket {number}: {ticket}")
        result = extract_ticket(ticket)

        if result["success"]:
            print("Validated data:", result["data"])
        else:
            print("Failure result:", result["error"])