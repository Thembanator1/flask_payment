import random
from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

app = Flask(__name__)

# Configure email settings
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
SMTP_USERNAME = 'runtime-shopping@outlook.com'
SMTP_PASSWORD = '@sdproj123'
SENDER_EMAIL = 'runtime-shopping@outlook.com'
RECIPIENT_EMAIL = ''


@app.route('/')
def index():
    return render_template('payment_form.html')

# @app.route('/set_email', methods=['POST'])
# def set_email():
#     global RECIPIENT_EMAIL
#     if request.method == 'POST':
#         recipient_email = request.json.get('recipientEmail')
#         RECIPIENT_EMAIL = recipient_email
#         return {'success': True}
#     return {'success': False}


@app.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    global RECIPIENT_EMAIL
    if request.method == 'POST':
        card_description = request.form['card-description']
        name_on_card = request.form['name-on-card']
        card_number = request.form['card-number']
        expiry_month = request.form['expiry-month']
        expiry_year = request.form['expiry-year']
        cvv = request.form['cvv']
        RECIPIENT_EMAIL = 'gesod90877@andorem.com'
        amount = request.form['amount']

        # Generate the payment receipt
        receipt = {
            'card_description': card_description,
            'name_on_card': name_on_card,
            'card_number': card_number,
            'expiry_month': expiry_month,
            'expiry_year': expiry_year,
            'cvv': cvv,
            'amount': amount,
            'customer_email': RECIPIENT_EMAIL,
            'payment_date': date.today().strftime('%Y-%m-%d'),
            'order_number': str(random.randint(100000000, 999999999))
        }

        # Send the receipt via email
        send_email(receipt)

        return render_template('confirmation_page.html')

    return 'Method Not Allowed'


def send_email(receipt):
    # Create a multipart message container
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = 'Payment Receipt'

    # Create the HTML email body
    email_body = render_template('email_template.html', receipt=receipt)
    message.attach(MIMEText(email_body, 'html'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)


if __name__ == '__main__':
    app.run()
