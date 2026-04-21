# toDo

REST API to manage todo lists and entries — with Python and Flask

# Dependencies versions

- Python 3.x
- Flask

# Starting and setting up

pip install -r requirements.txt
python src/main.py

# API specification / description

try the full API specification in `docs/todo-config.yaml`.

Method, Endpoint, Description


GET /todo-list/{list_id} Get all entries

POST /todo-list/{list_id} Add entry 

DELETE /todo-list/{list_id} Delete a list 

POST /todo-list Create a new list 

PATCH /entry/{entry_id} Update an entry 

DELETE /entry/{entry_id} Delete an entry 


# Development part

Server runs on `http://127.0.0.1:5000` by default.
