import os
from flask import Flask, render_template, request
from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required
import stripe
from auth import requires_auth
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from models import User, Operator, Item, Order, OrderItems



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
def checkout(amount):
    return render_template('checkout.html', key=stripe_keys['publishable_key'], amount = amount)

@app.route('/charge', methods=['POST'])
def charge():
    print request.form
    # Amount in cents
    customer = stripe.Customer.create(
        email='customer@example.com',
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Truckate Order'
    )

    return render_template('charge.html', amount=amount)


@app.route('/truck/<truck>',methods=['GET','POST'])
def truck_page(truck):
    items = session.query(Item).filter(Item.operator_id==truck)
    if request.method == 'POST':
        user = User()
        user.firstName = request.form.get('firstName')
        user.lastName = request.form.get('lastName')
        user.email = request.form.get('email')
        session.add(user)
        session.commit()
        order = Order()
        order.operator_id = truck
        order.user = user
        order.status = 'created'
        session.add(order)
        session.commit()
        amount = 0
        for item_id in request.form.getlist('item'):
            orderitem = OrderItems()
            orderitem.order_id = order.id
            orderitem.item_id = item_id
            item = items.filter(Item.id == item_id).first()
            amount += item.price
            session.add(orderitem)
            session.commit()
        amount += 50
        return render_template('checkout.html',amount = amount)
    else:
        return render_template('truckPage.html', items = items.all())

@app.route('/orders/<truck>')
def truck_page(truck):
    open_orders = session.query(Order).filter(Order.status=='paid').all()
    print open_orders[0].order_item[0].item
    return render_template('line.html', orders = open_orders)

#index
@app.route('/index')
def index():
    operators = [instance for instance in session.query(Operator)]
    return render_template('index.html',trucks = operators)


@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)