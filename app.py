from flask import Flask, request, render_template
import json

app = Flask(__name__)

#GET (HOME)
@app.route('/', methods=['GET']) 
def load_tasks(): 
    with open('tasks.json', 'r') as task_file: 
        tasks = json.load(task_file) 
    return render_template('index.html', tasks = tasks) 

#GET
@app.route('/tasks', methods=['GET'])
def save_tasks(): 
    with open('tasks.json', 'r') as task_file: 
        return json.load(task_file) 
    
#POST (add) 
@app.route('/tasks', methods=['POST']) 
def create_tasks():

    add_task = request.json

    id = add_task.get('id')
    description = add_task.get('description')
    category = add_task.get('category')
    status = add_task.get('status')

    if not id:
        return ({'error': 'ID is required'}), 400
    if not description:
        return ({'error': 'Description is required'}), 400
    if not category:
        return ({'error': 'Category is required'}), 400
    if not status:
        return ({'error': 'Status is required'}), 400

    
    with open('tasks.json', 'r') as tasks_file:
        tasks = json.load(tasks_file)

    for task in tasks:
        if task['id'] == id:
            return ({'error': 'This ID already exists'}), 400
        
    new_task =  {
        
        'id': id,
        'description': description,
        'category': category,
        'status': status
    }

    tasks.append(new_task) 

    with open('tasks.json', 'w') as tasks_file:
        tasks = json.dump(tasks, tasks_file, indent=4)

    return (new_task), 201

#GET (finds id)
@app.route('/tasks/<int:task_id>', methods=['GET'])
def find_task(task_id):
    with open('tasks.json', 'r') as tasks_file:
        tasks = json.load(tasks_file)

    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        
        return ({'message': 'Task was not found'}), 404
    
    return (task)
#DELETE (delete task)
@app.route('/tasks/<int:tasks_id>', methods=['DELETE'])
def delete_task(tasks_id):
    with open('tasks.json', 'r') as tasks_file:
        tasks = json.load(tasks_file)
    
    delete_task = None
    for task in tasks:
        if task['id'] == tasks_id:
            delete_task = task
            break

    if not delete_task:
        return ({'error': 'Task not found'}), 404
    
    tasks.remove(delete_task)

    with open('tasks.json', 'w') as tasks_file:
        tasks = json.dump(tasks, tasks_file, indent=4)

    return ({'message': 'Task has been deleted'}), 200

#PUT (updates task)
@app.route('/tasks/<int:tasks_id>', methods=['PUT'])
def update_task(tasks_id):
    with open('tasks.json', 'r') as tasks_file:
        tasks = json.load(tasks_file)
    
    update_task = request.json
    task_update = False
    
    for task in tasks:
        if task['id'] == tasks_id:
            
            task.update({
                'description': update_task.get('description', task['description']),
                'category': update_task.get('category', task['category']),
                'status': update_task.get('status', task['status'])
            })
            task_update = True
            break
    
    if not task_update:
        return ({'error': 'Task does not exist'}), 404

    with open('tasks.json', 'w') as tasks_file:
        tasks = json.dump(tasks, tasks_file, indent=4)

    return ({'message': 'Task was succesfully updated'}), 200

        
    
#PUT (completes task)            
@app.route('/tasks/<int:tasks_id>/complete', methods=['PUT'])
def task_is_completed(tasks_id):
    with open('tasks.json', 'r') as tasks_file:
        tasks = json.load(tasks_file)

    for task in tasks:
        if task['id'] == tasks_id:
            task['status'] = 'complete'            

            with open('tasks.json', 'w') as tasks_file:
                tasks = json.dump(tasks, tasks_file, indent=4)

                return ({'message': 'Task is now marked as completed', 'task': task}), 200
    
    return ({'error': 'Task not found'}), 404
        
#GET (show categories)
@app.route('/tasks/categories', methods=['GET'])
def get_category():
    with open('tasks.json', 'r') as tasks_file:
        tasks = json.load(tasks_file)

    categories = []

    for task in tasks:
        if task['category'] not in categories:
            categories.append(task['category'])

    return ({'categories': categories}), 200

#GET (show in categories)
@app.route('/tasks/categories/<category_name>', methods=['GET'])
def get_task_in_category(category_name):
    with open('tasks.json', 'r') as tasks_file:
        tasks = json.load(tasks_file)

    categories = []

    category_name = category_name.lower()

    for task in tasks:
        if task['category'].lower() == category_name:
            categories.append(task)

    if not categories:
        return ({'error': 'No tasks in this category'}), 404
    
    return ({'tasks': categories}), 200


if __name__ == "__main__":
    app.run(debug=True)
