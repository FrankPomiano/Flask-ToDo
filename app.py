from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Simple in-memory database for demonstration
todos = []

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if data and 'task' in data:
        new_todo = {
            'id': len(todos) + 1,
            'task': data['task'],
            'completed': False
        }
        todos.append(new_todo)
        return jsonify(new_todo), 201
    return jsonify({"error": "Task field missing"}), 400

@app.route('/api/todos/<int:todo_id>/complete', methods=['PUT'])
def set_complete(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    initial_len = len(todos)
    todos = [todo for todo in todos if todo['id'] != todo_id]
    if len(todos) < initial_len:
        return jsonify({"success": True})
    return jsonify({"error": "Todo not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)