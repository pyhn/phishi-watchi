from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_content = request.form['email']
        # Placeholder for analyzer logic
        result = "SAFE"  # Replace with real analysis later
        return render_template('result.html', result=result)
    return render_template('index.html')
