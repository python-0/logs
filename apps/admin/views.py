from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET', 'POST'])
def index():
    return render_template('admin/index.html')
