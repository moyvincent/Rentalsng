from flask import Blueprint, Flask, redirect, render_template, url_for
from flask_login import current_user, login_required
from rent.auth import login_manager
from rent.db import db, Item
from rent.form import ItemForm
import base64

app = Flask(__name__)

# Initialize the login manager
login_manager.init_app(app)

# Register the blueprint for the items module
items_app = Blueprint('items', __name__)

@items_app.route('/')
def allItems():
    items = Item.query.all()
    return render_template('rentals.html', items=items)

@items_app.route('/rentals/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        photo_data = None
        photo_file = form.photo.data
        if photo_file:
            photo_data = base64.b64encode(photo_file.read()).decode('utf-8')
        item = Item(title=form.title.data, description=form.description.data, price=form.price.data, location=form.location.data, photo=photo_data, user_id=current_user.id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('items.allItems'))
    return render_template('new_item.html', form=form)