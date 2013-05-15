import os
from flask import Flask, render_template, request
from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required
import stripe
from auth import requires_auth
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from models import User, Operator, Item



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
# Checkout Stuff
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

@app.route('/truck/<truck>')
def truck_page(truck):
    items = session.query(Item).filter(Item.operator_id==truck).all()
    return render_template('truckPage.html', items = items)

#index
@app.route('/index')
def index():
    operators = [instance for instance in session.query(Operator)]
    print operators
    print operators[0]
    return render_template('index.html',trucks = operators)

if __name__ == '__main__':
    app.run(debug=True)