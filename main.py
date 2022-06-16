from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from random import choice

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class SessionModel(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    analyst_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Session(session_id={self.session_id}, client_id={self.client_id}, analyst_id={self.analyst_id})"


class MessageModel(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"""Message(message_id={self.message_id}, session_id={self.session_id}, author_id={self.author_id}" \
               f"text={self.text})"""


class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name}, role={self.role})"


# db.create_all()


session_post_args = reqparse.RequestParser()
session_post_args.add_argument("client_id", type=str, help="User ID of Client assigned", required=True)
session_post_args.add_argument("analyst_id", type=str, help="User ID of Analyst assigned", required=True)

resource_session_fields = {
    'session_id': fields.Integer,
    'client_id': fields.Integer,
    'analyst_id': fields.Integer
}


message_post_args = reqparse.RequestParser()
message_post_args.add_argument("session_id", type=str, help="Id of the session.", required=True)
message_post_args.add_argument("author_id", type=int, help="Id of sender of the message", required=True)
message_post_args.add_argument("text", type=str, help="The message body", required=True)

resource_message_fields = {
    'message_id': fields.Integer,
    'session_id': fields.Integer,
    'author_id': fields.String,
    'text': fields.String
}


user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name", type=str, help="Name of User", required=True)
user_post_args.add_argument("role", type=str, help="Role of User", required=True)

resource_user_fields = {
    'user_id': fields.Integer,
    'name': fields.String,
    'role': fields.String
}


class Session(Resource):
    @marshal_with(resource_session_fields)
    def get(self, session_id):
        result = SessionModel.query.filter_by(ssession_idid=session_id).first()
        if not result:
            abort(404, message="Could not find that session_id")
        return result

    @marshal_with(resource_session_fields)
    def post(self):
        args = session_post_args.parse_args()
        session = SessionModel(client_id=args['client_id'], analyst_id=args['analyst_id'])
        db.session.add(session)
        db.session.commit()
        return session, 201


class Message(Resource):
    @marshal_with(resource_message_fields)
    def get(self, message_id):
        result = MessageModel.query.filter_by(message_id=message_id).first()
        if not result:
            abort(404, message="Could not find that message_id")
        return result

    @marshal_with(resource_message_fields)
    def post(self):
        args = message_post_args.parse_args()
        message = MessageModel(session_id=args['session_id'], author_id=args['author_id'], text=args['text'])
        db.session.add(message)
        db.session.commit()
        return message, 201

    @marshal_with(resource_message_fields)
    def delete(self, message_id):
        result = MessageModel.query.filter_by(message_id=message_id).delete()
        if not result:
            abort(404, message="Could not find that message_id for deletion")
        db.session.commit()
        return '', 204


class User(Resource):
    @marshal_with(resource_user_fields)
    def get(self, user_id):
        result = UserModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404, message="Could not find that user_id")
        return result

    @marshal_with(resource_user_fields)
    def post(self):
        args = user_post_args.parse_args()
        user = UserModel(name=args['name'], role=args['role'])
        db.session.add(user)
        db.session.commit()
        return user, 201


api.add_resource(Session, "/session/<int:session_id>", "/session/")
api.add_resource(Message, "/message/<int:message_id>", "/message/")
api.add_resource(User, "/user/<int:user_id>", "/user/")

# api.add_resource(Analyst, "/get_anal/")

if __name__ == "__main__":
    app.run(debug=True)
