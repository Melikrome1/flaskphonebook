
from flask import Flask, render_template, flash, redirect, url_for
from app import app
from app.forms import AddressForm


@app.route('/address_forms', methods=['GET', 'POST'])
def address_forms():
    form = AddressForm()
    if form.validate_on_submit():
        flash(f'{form.first_name.data} {form.last_name.data} has been added to the address book', 'success')
        print(f'First Name: {form.first_name.data}')
        print(f'Last Name: {form.last_name.data}')
        print(f'Phone Number: {form.phone_number.data}')
        print(f'Address: {form.address.data}')
        return redirect(url_for('index'))
    return render_template('address_forms.html', form=form)


@app.route('/')
def index():
    return render_template('index.html')


