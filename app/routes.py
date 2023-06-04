from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import AddressForm, LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Address


@app.route('/address/new', methods=['GET', 'POST'])
@login_required
def new_address():
    if request.method == 'POST':
        # Retrieve address form data
        address = Address(user_id=current_user.id,)
        db.session.add(address)
        db.session.commit()

        flash('Address added successfully.')
        return redirect(url_for('address_list'))

    return render_template('new_address.html')


@app.route('/address_forms', methods=['GET', 'POST'])
@login_required
def address_forms():
    form = AddressForm()
    if form.validate_on_submit():
        address = Address(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            address=form.address.data,
            user_id=current_user.id
        )
        db.session.add(address)
        db.session.commit()
        flash(f'{form.first_name.data} {form.last_name.data} has been added to the address book', 'success')
        return redirect(url_for('index'))
    return render_template('address_forms.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = AddressForm()
    if form.validate_on_submit():
        flash(f'{form.first_name.data} {form.last_name.data} has been added to the address book', 'success')
        return redirect(url_for('index'))
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', form=form, addresses=addresses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('profile', username=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('profile.html', user=user, form=form)











