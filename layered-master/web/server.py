from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books')
def users():
    db_session = db.getSession(engine)
    users = db_session.query(entities.Book)
    data = users[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype = 'application/json')

@app.route('/users')
def users2():
    db_session = db.getSession(engine)
    users2 = db_session.query(entities.User)
    data = users2[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype = 'application/json')

@app.route('/messages')
def users3():
    db_session = db.getSession(engine)
    users3 = db_session.query(entities.Message)
    data = users3[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype = 'application/json')

@app.route('/create_test_books', methods = ['GET'])
def create_test_books():
    db_session = db.getSession(engine)
    book = entities.Book(name="Head First HTML5", isbn="12345", title="Head first about HTML5")
    db_session.add(book)
    db_session.commit()
    return "Test books created!"

@app.route('/create_test_messages', methods = ['GET'])
def create_test_messages():
    db_session = db.getSession(engine)
    message = entities.Message( content="Hola", user_from_id=1, user_to_id = 2)
    db_session.add(message)
    db_session.commit()
    return "Test message created!"

@app.route('/create_test_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user = entities.User(code="201810456", name="Mateo", lastname="Noel", password="*****")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls = connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, 'message': "Not found"}
    return Response(message, status=404, mimetype='application/json')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('0.0.0.0'))
