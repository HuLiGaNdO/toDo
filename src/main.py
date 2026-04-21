"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': 'Du musst noch dein Milch kaufen!', 'user_id': str(uuid.uuid4()), 'list_id': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': 'Du musst die Blätter ausdrucken', 'user_id': str(uuid.uuid4()), 'list_id': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'user_id': str(uuid.uuid4()), 'list_id': todo_list_3_id},
    {'id': todo_4_id, 'name': 'Eier', 'description': '', 'user_id': str(uuid.uuid4()), 'list_id': todo_list_1_id},
]

@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE', 'POST'])  # ← Step 2: добавлен POST
def handle_list(list_id):
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    if not list_item:
        abort(404)
    if request.method == 'GET':
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list_id'] == list_id])
    elif request.method == 'DELETE':
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return jsonify({'message': 'List deleted successfully'}), 204
    elif request.method == 'POST':                                      # ← Step 2
        data = request.get_json(force=True)
        if not data or 'name' not in data or 'description' not in data:
            abort(406)
        new_entry = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'description': data['description'],
            'user_id': str(uuid.uuid4()),
            'list_id': list_id
        }
        todos.append(new_entry)
        return jsonify(new_entry), 201

@app.route('/todo-list', methods=['POST'])
def add_new_list():
    new_list = request.get_json(force=True)
    if not new_list or 'name' not in new_list:
        abort(406)
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 201

@app.route('/lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)

@app.route('/entry/<entry_id>', methods=['PATCH', 'DELETE'])            # ← Step 3
def handle_entry(entry_id):
    entry = next((e for e in todos if e['id'] == entry_id), None)
    if not entry:
        abort(404)
    if request.method == 'PATCH':
        data = request.get_json(force=True)
        if not data:
            abort(406)
        if 'name' in data:
            entry['name'] = data['name']
        if 'description' in data:
            entry['description'] = data['description']
        return jsonify(entry), 200
    elif request.method == 'DELETE':
        todos.remove(entry)
        return jsonify({'message': 'Entry deleted'}), 204

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
