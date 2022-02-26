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

@app.route('/books')
def books():
    if 'user' in session:
        user = session['user']
        books = database.getUser(user['email'])['books']
        books_ = []
        for book in books:
            books_.append(database.getBook(book))
        return render_template('books.html', books=books_, user=user)

@app.route('/newBook', methods=['POST'])
def newBook():
    if 'user' in session:
        name = request.form['name']
        if name.replace(' ', '') == '':
            return redirect(url_for('books'))
        database.createBook(session['user']['_id'], name)
        return redirect(url_for('books'))
    return redirect(url_for('home'))

@app.route('/book/<bookID>')
def book(bookID):
    if 'user' in session:
        book = database.getBook(bookID)
        chapters = book['chapterOrder']
        chapters_ = []
        for chapter in chapters:
            chapters_.append(database.getBook(bookID)['chapters'][chapter])
        return render_template('book.html', book=book, chapters=chapters_, user=session['user'])
    return redirect(url_for('home'))

@app.route('/newchapter/<bookid>', methods=['POST'])
def newChapter(bookid):
    if 'user' in session:
        name = request.form['name']
        if name.replace(' ', '') == '':
            return redirect(url_for('book', bookID=bookid))
        database.createChapter(bookid, name)
        return redirect(url_for('book', bookID=bookid))
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
