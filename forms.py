from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required


class OrderForm(Form):
	items = SelectField()
