
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

output = Path("documents/product_manual.pdf")
output.parent.mkdir(exist_ok=True)

pdf = canvas.Canvas(str(output), pagesize=letter)

pages = [
    (
        "Account Management",
        "Customers can update their registered email address in "
        "Account Settings. To reset a password, select Forgot Password "
        "on the login page and follow the instructions sent by email."
    ),
    (
        "Billing and Payments",
        "Customers can view invoices in the Billing section. "
        "If a payment is deducted twice, contact customer support "
        "with the transaction reference. Refund processing times "
        "depend on the payment provider."
    ),
    (
        "Order Tracking",
        "Customers can track an order using the order ID in Order History. "
        "The order page displays the latest available delivery status. "
        "Contact support if the tracking information is not updated."
    ),
    (
        "Technical Troubleshooting",
        "If the mobile application crashes, restart the application "
        "and check for updates. If the problem continues, clear the "
        "application cache and contact technical support."
    ),
    (
        "Security",
        "Never share your password or verification code. Use a strong "
        "password and update it if you suspect unauthorized access. "
        "Contact support if you notice suspicious account activity."
    )
]

for title, content in pages:
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(72, 730, title)

    pdf.setFont("Helvetica", 12)
    y = 680

    for line in content.split(". "):
        pdf.drawString(72, y, line.strip())
        y -= 30

    pdf.showPage()

pdf.save()

print(f"Sample manual created: {output}")