from flask import Flask,render_template

# Create a Flask instance
app = Flask(__name__)

# Define a route (URL path) and its function
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return "This is the About page."

@app.route('/contact')
def contact():
    return "Contact us at contact@example.com"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
