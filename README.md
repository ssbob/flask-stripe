# Stripe/Flask/Python Test Integration

This is a simple test integration with Stripe elements, and a custom payment flow, using Flask on Python for simplicity.

## Useful links

- [Stripe Payment Dashboard](https://dashboard.stripe.com/test/payments) - gotta make sure you get paid right?
- [Stripe API Keys](https://dashboard.stripe.com/test/apikeys) - you need these often, make sure you put them in
  your `.env` file for safe keeping.
- [Stripe Integration Builder Docs](https://stripe.com/docs/payments/integration-builder) - this was critical in getting
  the custom payment flow to work (mostly).
- [Stripe Payment Intent API Docs](https://stripe.com/docs/api/payment_intents/object) - this is important to understand
  the structure of the `PaymentIntent` object.
- [Stripe Payment Charge API Docs](https://stripe.com/docs/api/charges/object) - needed to parse out the `Charge ID` for
  confirmations.
- [Stripe CLI Docs](https://stripe.com/docs/stripe-cli) - great reference for how to utilize the Stripe CLI.

## How does it work?

This simple web-app uses some basic "store" concepts, like buying an item (a book in this case), and getting sent to a "
checkout" page to purchase. Stripe has 2 primary paths at this point to facilitate the purchase.

- The first is Stripe checkout, which would redirect a user to a pre-built checkout page hosted/managed by Stripe, then
  redirect the user back to the e-commerce page (success/failure).
- The second is using Stripe elements, which gives the store owner, the ability to build their own payment flow, but in
  the background still provides normal Stripe functionality.

In this example, it was built using a custom payment flow. The user clicks on a book to buy, and is sent to a checkout
page where they can input their CC information, Stripe (behind the scenes) processes the payment and responds back with
success/failure to the store.

## Why did I build it the way I did?

To start, I stuck with examples provided by Stripe on their GitHub
page [Stripe Samples](https://github.com/stripe-samples). Along with the various API docs, and sample explanations
provided on their docs page, [Stripe Integration Builder](https://stripe.com/docs/payments/integration-builder). I also
ended up finding an example of Stripe and Flask using Stripe Checkouts (the other path listed above), found
here, [Flask Stripe Tutorial](https://testdriven.io/blog/flask-stripe-tutorial/).

### The more difficult parts / recommendations for others

- Some hard parts were getting the Javascript files from the Stripe Integration Builder working with the custom HTML (
  Hint: use the example HTML from the Stripe Integration Builder examples as a starting point, was very helpful).
- Second was passing data to and from the various routes in Flask without a database. Keep in mind, this is a very
  simple example, all it proves is that Stripe is processing payments, but isn't a real e-commerce page as it lacks a "
  cart", or delivery, or accounts.

### What would I do differently?

- If I was going to build this out a second time, I would probably end up using [Django](https://www.djangoproject.com/)
  as the web framework as it makes making an eCommerce site pretty easy. Some of the examples on the Stripe docs use
  Django instead of Flask on the custom payment and webhook process. Nothing against Flask, it just was something new I
  was learning while building this simple test, and that meant I struggled a bit more.
- I would include a simple database (SQLite, Postgres), which means I don't have to ship data around from
  class/function (Flask Route) to class/function, instead I can make DB calls. Perhaps not the most efficient
  performance wise, but for a simple eCommerce site, the volume would not be an issue.
- While I like the idea of a custom payment flow, Stripe Checkout makes a lot of sense, as it eases the burden of the
  developer and makes Stripe do the heavy lifting. I think I would probably go that route next time.

## What doesn't work?

This is a "sort of" a doesn't work thing, it's working, but I am sure I am going about it all wrong (aka the "hacky"
approach).

One of the issues I encountered was trying to redirect the user to the `success` template via the `webhook` route.
However, it was not working, and after numerous attempts, I looked elsewhere. What I found was in `client.js`, I can
force the redirect using the `document.location.href` function, which forces the browser window to a different URL. With
this mechanism, I pass the `paymentIntentId` value from the card confirmation function (also in `client.js`). Within
that Flask route, I use the Stripe API to retrieve the `PaymentIntent` object, and parse out
the `charge confirmation ID`, and amount. Then render that in the `success` template. I am sure there is a more elegant
solution to this, but it works consistently, so I am calling this a win!

## How do I use this?

To get started, clone the repository and run pip3 to install dependencies:

```
git clone https://github.com/marko-stripe/sa-takehome-project-python 
cd sa-takehome-project-python
pip3 install -r requirements.txt
```

Then setup your keys by changing the values in the .env file:

```
STRIPE_PUBLISHABLE_KEY=your publishable key here
STRIPE_SECRET_KEY=your secret key here
STRIPE_ENDPOINT_SECRET=your endpoint secret here
```

Then run the application locally:

```
flask run
```

If you want to be able to verify payment locally (i.e., not having to log in to your payment dashboard), then make sure
to install the stripe [CLI](https://stripe.com/docs/stripe-cli). Then in a console window launch the following CLI
command:

```
stripe listen --forward-to localhost:5000/webhooks
```

NOTE: if you change this repository, and the route for webhooks is changed, then substitute that value above.

Further, if you want to confirm payment, and the webhook is working correctly, you can run the following command (
again, part of the CLI) from another terminal:

```
stripe trigger payment_intent.succeeded
```

Navigate to [http://localhost:5000](http://localhost:5000) to view the index page.

Pick a book, and click on `Purchase`.

Enter your credit card details (NUM, EXP, and CVC).

For testing purposes, you can use the following:

```
NUM  4242 4242 4242 4242
EXP  Any Month/Year in the future
CVC  Any 3 digit combination
```

This number will auto-approve the transaction. You can find out more information on the Stripe Integration
Builder [doc](https://stripe.com/docs/payments/integration-builder).

You can also confirm transactions on your [Payments Dashboard](https://dashboard.stripe.com/test/payments).

Good luck!
