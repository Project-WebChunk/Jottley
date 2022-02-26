from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from authlib.integrations.flask_client import OAuth
from loginpass import create_flask_blueprint, Discord
from databases import Database

app = Flask(__name__)
oauth = OAuth(app)
app.config.from_pyfile('config.py')
backends = [Discord]
database = Database(app.config['MONGO_URI'])

@app.route('/')
def home():
    if 'user' in session:
        return render_template('user.html', user=session['user'])
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/changename', methods=['POST'])
def changename():
    if 'user' in session:
        name = request.form['name']
        database.updateName(session['user']['email'], name)
        email = session['user']['email']
        session.pop('user', None)
        session['user'] = database.getUser(email)
        return redirect(url_for('home'))
    return redirect(url_for('home'))

def handle_authorize(remote, token, user_info):
    if database.userExists(user_info['email']):
        session['user'] = database.getUser(user_info['email'])
    else:
        database.addUser(user_info['email'])
        session['user'] = database.getUser(user_info['email'])
    return redirect(url_for('home'))


bp = create_flask_blueprint(backends, oauth, handle_authorize)
app.register_blueprint(bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
