import os
from flask import Flask, render_template, request
import stripe
from auth import requires_auth
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from models import User, Operator, Item, Order
stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

engine = create_engine("mysql://root:@localhost/Truckate")

SessionMkr = sessionmaker()
SessionMkr.configure(bind=engine)
session = SessionMkr()

app = Flask(__name__)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)

@app.route('/index')
def index():
    operators = [instance.location for instance in session.query(Operator)]
    print operators
    #bathrooms = session.query(Bathroom).all()
    #print bathrooms
    #return render_template('list.html', locs=locations, baths=bathrooms)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)