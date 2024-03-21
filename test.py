from flask import Flask, render_template, request

app = Flask(__name__)


# Define a route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')


# Define a route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    # name = request.form['name']
    return f'super random number'


if __name__ == '__main__':
    app.run(debug=True)
