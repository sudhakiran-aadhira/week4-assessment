
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "orders.db"


# Tool 1: Mock CRM customer data
customers = {
    1: {"customer_id": 1, "name": "Arun", "plan": "Basic"},
    2: {"customer_id": 2, "name": "Priya", "plan": "Premium"},
    3: {"customer_id": 3, "name": "Rahul", "plan": "Standard"}
}


def get_customer(customer_id):
    customer = customers.get(customer_id)

    if customer is None:
        return {
            "success": False,
            "error": f"Customer {customer_id} not found"
        }

    return {
        "success": True,
        "data": customer
    }


# Create a small SQLite orders table
def setup_database():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            status TEXT NOT NULL
        )
    """)

    connection.execute("""
        INSERT OR IGNORE INTO orders (order_id, status)
        VALUES (1042, 'Out for delivery')
    """)

    connection.commit()
    connection.close()


# Tool 2: Get order status from SQLite
def get_order_status(order_id):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        "SELECT order_id, status FROM orders WHERE order_id = ?",
        (order_id,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return {
            "success": False,
            "error": f"Order {order_id} not found"
        }

    return {
        "success": True,
        "data": dict(row)
    }


# Tool schemas: describe the tools and their arguments
tool_schemas = [
    {
        "name": "get_customer",
        "description": "Find a customer and their plan",
        "parameters": {
            "customer_id": "integer"
        }
    },
    {
        "name": "get_order_status",
        "description": "Find the status of an order",
        "parameters": {
            "order_id": "integer"
        }
    }
]


# Only registered tools can execute
available_tools = {
    "get_customer": get_customer,
    "get_order_status": get_order_status
}


def execute_tool(tool_name, arguments):
    tool = available_tools.get(tool_name)

    if tool is None:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        return tool(**arguments)
    except (TypeError, ValueError) as error:
        return {
            "success": False,
            "error": f"Invalid tool arguments: {error}"
        }


# Simulated tool selection for use without an LLM API
def select_tools(question):
    question = question.lower()
    selected = []

    if "customer 2" in question or "customer" in question:
        import re
        match = re.search(r"customer\s+(\d+)", question)
        if match:
            selected.append(
                ("get_customer", {"customer_id": int(match.group(1))})
            )

    if "order" in question:
        import re
        match = re.search(r"order\s+(\d+)", question)
        if match:
            selected.append(
                ("get_order_status", {"order_id": int(match.group(1))})
            )

    return selected


def answer_question(question):
    calls = select_tools(question)
    results = []

    for tool_name, arguments in calls:
        result = execute_tool(tool_name, arguments)
        print(f"Tool: {tool_name}({', '.join(f'{k}={v}' for k, v in arguments.items())})")
        results.append((tool_name, result))

    if not results:
        print("Answer: I could not identify a tool to answer that question.")
        return

    # Build a clean answer from the tool results
    messages = []

    for tool_name, result in results:
        if not result["success"]:
            messages.append(result["error"])
        elif tool_name == "get_customer":
            data = result["data"]
            messages.append(
                f"Customer {data['customer_id']} is on the "
                f"{data['plan']} plan"
            )
        elif tool_name == "get_order_status":
            data = result["data"]
            messages.append(
                f"order {data['order_id']} is "
                f"{data['status'].lower()}"
            )

    print("Answer: " + " and ".join(messages) + ".")


if __name__ == "__main__":
    setup_database()

    print("TEST 1: Two tools in one question")
    answer_question(
        "Which plan is customer 2 on and where is order 1042?"
    )

    print("\nTEST 2: Unknown customer")
    print(json.dumps(execute_tool(
        "get_customer", {"customer_id": 999}
    ), indent=2))

    print("\nTEST 3: Non-existent tool")
    print(json.dumps(execute_tool(
        "delete_customer", {"customer_id": 2}
    ), indent=2))

    print("\nTEST 4: Unknown order")
    print(json.dumps(execute_tool(
        "get_order_status", {"order_id": 9999}
    ), indent=2))