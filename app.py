from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

# Create a new task or bulk add tasks
@app.route('/v1/tasks', methods=['POST'])
def create_tasks():
    data = request.get_json()

    #if only one task is present
    if 'tasks' not in data:
        if 'title' not in data:
            return jsonify({'error': 'Title is required for task'}), 400
        
        new_task = {
            'id': len(tasks) + 1,
            'title': data['title'],
            'completed': data.get('is_completed', False)
        }

        tasks.append(new_task)
        return jsonify({'id': new_task['id']}), 201
        
    #input error handling
    if not isinstance(data['tasks'], list):
        return jsonify({'error': 'Tasks should be provided in a list'}), 400

    #if bulk tasks are present
    created_tasks = []

    for task_data in data['tasks']:
        if 'title' not in task_data:
            return jsonify({'error': 'Title is required for each task'}), 400

        new_task = {
            'id': len(tasks) + 1,
            'title': task_data['title'],
            'completed': task_data.get('is_completed', False)
        }

        tasks.append(new_task)
        created_tasks.append({'id': new_task['id']})

    return jsonify({'tasks': created_tasks}), 201

# Bulk delete tasks
@app.route('/v1/tasks', methods=['DELETE'])
def delete_tasks():
    data = request.get_json()

    if 'tasks' not in data or not isinstance(data['tasks'], list):
        return jsonify({'error': 'Tasks should be provided in a list'}), 400

    task_ids_to_delete = {task['id'] for task in data['tasks']}

    global tasks
    tasks = [task for task in tasks if task['id'] not in task_ids_to_delete]

    return jsonify({'message': 'Tasks deleted successfully'}), 204

# List all tasks
@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    formatted_tasks = [{'id': task['id'], 'title': task['title'], 'is_completed': task['completed']} for task in tasks]
    return jsonify({'tasks': formatted_tasks})

# Get a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify({'id': task['id'], 'title': task['title'], 'is_completed': task['completed']})
    return jsonify({'error': 'There is no task at that id'}), 404

# Delete a specified task
@app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'message': 'Task deleted successfully'}), 204

# Edit the title or completion of a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'There is no task at that id'}), 404

    data = request.get_json()
    
    if 'title' in data:
        task['title'] = data['title']

    if 'is_completed' in data:
        task['completed'] = data['is_completed']

    return jsonify({'message': 'Task updated successfully'}), 204

if __name__ == '__main__':
    app.run(debug=True)
