from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Configure email settings
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
SMTP_USERNAME = 'runtime-shopping@outlook.com'
SMTP_PASSWORD = '@sdproj123'
SENDER_EMAIL = 'runtime-shopping@outlook.com'
RECIPIENT_EMAIL = 'heyet48454@asuflex.com'


@app.route('/')
def index():
    return render_template('payment_form.html')

@app.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        amount = request.form['amount']
        payment_method = request.form['payment_method']

        # Generate the payment receipt
        receipt = {
            'name': name,
            'email': email,
            'amount': amount,
            'payment_method': payment_method
        }

        # Send the receipt via email
        send_email(receipt)

        return render_template('payment_receipt.html', receipt=receipt)

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
