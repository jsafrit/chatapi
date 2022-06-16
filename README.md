# ChatAPI for Python interview

Backend only for ChatAPI per the assignment specs 

Utilizing Flask, Flask_RESTful

Using sqlite database for persistent storage via SQLAlchemy

Simple test provided in test.py, but just as easily implemented on the cmdline
with curl or via Postman

To run ChatAPI locally:
- > source .venv/Scripts/activate
- > python main.py

To reset the database:
- > rm database.db
- > python -c "from main import db; db.create_all()"
  
To run the simple test script
- > python test.py


## Implemented classes/methods:
- User
  - get, post
- Session
  - get, post
- Message
  - get, post, delete


## Not yet implemented
- validation checks on some models
  - i.e. you can create sessions with invalid user_id
- An endpoint to provide all messages for a session 
- An endpoint to select next available analyst for a new session
- An endpoint to clean up sessions once they are completed

## Use Cases from assignment
- Client logins/enters into the chat using a nickname
  - possible via user endpoint
- Analyst enters into the chat using a nickname
  - possible via user endpoint
- Client can POST a message and GET messages by calling a WebApi
  - possible via message endpoint
- Analyst can POST a message and GET messages by calling a WebAPI
  - possible via message endpoint
- Client can communicate to only 1 analyst
  - can be assured using sessions to pair only one analyst to a client
- Analyst can communicate to 1 or more Clients at the same time.
  - session endpoint allows analyst in multiple sessions
- The chat server will do round robin in order to select an analyst that will attend a new chat
request.
  - pending implementation
- Clients can initiate the chat, analysts cannot.
  - needs logic on front end to enforce this constraint



