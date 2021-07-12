import json
import os

import stripe
from flask import Flask, request, render_template, jsonify, redirect, url_for

stripe.api_key = os.environ['STRIPE_SECRET_KEY']
endpoint_secret = os.environ['STRIPE_ENDPOINT_SECRET']


app = Flask(__name__,
            static_url_path='',
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))


# Home route
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
    # Just hardcoding amounts here to avoid using a database
    item = request.args.get('item')
    title = None
    amount = None
    error = None

    if item == '1':
        title = 'The Art of Doing Science and Engineering'
        amount = 2300
    elif item == '2':
        title = 'The Making of Prince of Persia: Journals 1985-1993'
        amount = 2500
    elif item == '3':
        title = 'Working in Public: The Making and Maintenance of Open Source'
        amount = 2800
    else:
        # Included in layout view, feel free to assign error
        error = 'No item selected'

    return render_template('checkout.html', title=title, amount=amount, error=error)


# Success route
@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')


# Create Payment Route
@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:

        intent = stripe.PaymentIntent.create(
            amount=2300,
            currency='usd'
        )
        # print("Intent: ", intent)

        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


# Webhook for confirmation
@app.route("/webhooks", methods=["POST"])
def stripe_webhook():
    #print("Processing webhook...")
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    #print("Payload: ", payload)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "charge.succeeded":
        print("Payment was successful.")

    return "Success", 200



if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
