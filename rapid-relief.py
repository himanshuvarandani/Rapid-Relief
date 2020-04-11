from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/lerner_reg')
def lerner_reg():
    return render_template('lerner_reg.html')

@app.route('/lerner_login')
def lerner_login():
    return render_template('lerner_login.html')

@app.route('/lerner_dashboard')
def lerner_dashboard():
    return render_template('lerner_dashboard')



if __name__ == "__main__":
    app.run(debug=True)