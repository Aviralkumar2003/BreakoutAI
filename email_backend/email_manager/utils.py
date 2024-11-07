# email_manager/utils.py
import requests

def generate_email_content(template, data_row):
    # Replace placeholders in the template with actual values from the data_row dictionary
    for key, value in data_row.items():
        template = template.replace(f"{{{{ {key} }}}}", str(value))
    return template

def send_email_via_sendgrid(to_email, subject, content):
    headers = {
        'Authorization': 'Bearer YOUR_SENDGRID_API_KEY',
        'Content-Type': 'application/json',
    }
    data = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": "your_email@example.com"},
        "subject": subject,
        "content": [{"type": "text/plain", "value": content}]
    }
    response = requests.post('https://api.sendgrid.com/v3/mail/send', headers=headers, json=data)
    return response.status_code