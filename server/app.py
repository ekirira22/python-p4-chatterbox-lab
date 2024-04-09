from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import DatabaseError

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        try:
            messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
            response = make_response(messages, 200)
        except DatabaseError as e:
            error_msg = str(e.orig)
            response_body = {
                "messages": error_msg
            }
            response = make_response(response_body, 404)

    elif request.method == 'POST':
        data = request.get_json()

        message_body = Message(
            username = data.get('username'),
            body = data.get('body'),
        )

        try:
            db.session.add(message_body)
            db.session.commit()

            response = make_response(message_body.to_dict(), 201)
        except DatabaseError as e:
            db.session.rollback()
            error_msg = str(e.orig)
            response_body = {
                "messages": error_msg
            }
            response = make_response(response_body, 500)

    return response
        
    
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        if not message:
            response_body = {
                "message" : "Does not exist",
            }
            response = make_response(response_body, 404)
            return response
        
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data.get(attr))
        
        db.session.add(message)
        db.session.commit()
        response = make_response(message.to_dict(), 200)
        

    elif request.method == 'DELETE':
        if message:
            db.session.delete(message)
            db.session.commit()
            response_body = {
                "deleted" : True,
            }
            response = make_response(response_body, 200)
        else:
            response_body = {
                "message" : "Message not found",
            }
            response = make_response(response_body, 200)

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
