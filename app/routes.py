
from flask import Flask, render_template, flash, redirect, url_for
from app import app
from app.forms import AddressForm
from app.models import Address
from app import db

@app.route('/address_forms', methods=['GET', 'POST'])
def address_forms():
    form = AddressForm()
    if form.validate_on_submit():
        address = Address(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            address=form.address.data
        )
        db.session.add(address)
        db.session.commit()
        flash(f'{form.first_name.data} {form.last_name.data} has been added to the address book', 'success')
        return redirect(url_for('index'))
    return render_template('address_forms.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddressForm()
    if form.validate_on_submit():
        flash(f'{form.first_name.data} {form.last_name.data} has been added to the address book', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)








