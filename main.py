from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from random import choice

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class SessionModel(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100), nullable=False)
    analyst = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Session(client={self.client}, analyst={self.analyst}, sid={self.sid})"


class MessagesModel(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"""Message(message_id={self.message_id}, session_id={self.session_id}, author={self.author}" \
               f"text={self.text})"""

# db.create_all()


session_post_args = reqparse.RequestParser()
session_post_args.add_argument("client", type=str, help="Name of Client assigned", required=True)
session_post_args.add_argument("analyst", type=str, help="Name of Analyst assigned", required=True)

resource_session_fields = {
    'sid': fields.Integer,
    'client': fields.String,
    'analyst': fields.String
}


message_post_args = reqparse.RequestParser()
message_post_args.add_argument("session_id", type=str, help="Id of the session.", required=True)
message_post_args.add_argument("author", type=str, help="Sender of the message", required=True)
message_post_args.add_argument("text", type=str, help="The message", required=True)

resource_message_fields = {
    'message_id': fields.Integer,
    'session_id': fields.Integer,
    'author': fields.String,
    'text': fields.String
}


class Session(Resource):
    @marshal_with(resource_session_fields)
    def get(self, session_id):
        result = SessionModel.query.filter_by(sid=session_id).first()
        if not result:
            abort(404, message="Could not find that id")
        return result

    @marshal_with(resource_session_fields)
    def post(self):
        args = session_post_args.parse_args()
        # if result := SessionModel.query.filter_by(id=video_id).first():
        #     abort(409, message="id is taken")
        session = SessionModel(client=args['client'], analyst=args['analyst'])
        db.session.add(session)
        db.session.commit()
        return session, 201


class Messages(Resource):
    @marshal_with(resource_message_fields)
    def get(self, message_id):
        result = MessagesModel.query.filter_by(message_id=message_id).first()
        if not result:
            abort(404, message="Could not find that message id")
        return result

    @marshal_with(resource_message_fields)
    def post(self):
        args = message_post_args.parse_args()
        message = MessagesModel(session_id=args['session_id'], author=args['author'], text=args['text'])
        db.session.add(message)
        db.session.commit()
        return message, 201


class Analyst(Resource):
    analyst = ["Bob", "Charlie", "Dave", "Edgar", "Frank", "Gary", "Harv"]

    def get(self):
        return jsonify({"analyst": choice(self.analyst)})


class Client(Resource):
    def get(self):
        pass


api.add_resource(Session, "/session/<int:session_id>", "/session/")
api.add_resource(Messages, "/messages/<int:message_id>", "/messages/")
api.add_resource(Analyst, "/get_anal/")

if __name__ == "__main__":
    app.run(debug=True)
