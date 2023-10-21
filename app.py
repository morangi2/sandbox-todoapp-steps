from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://evemwangi:Nima900##@localhost:5432/todoapp'
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model): # Child Model
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable = False, default = False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<TODO {self.id} {self.description}, list {self.list_id}>'

# db.create_all()

class TodoList(db.Model): #Parent model
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<ToDoLIST {self.id} {self.name}>'


@app.route('/todos/create', methods=['POST']) # == ROUTE
def create_todo(): # == ROUTE HANDLER
    #fetch the data submitted by the user, add an empty string as a default
    # description_input = request.form.get('description', '')

    error = False
    body = {} #empty dictionary == will hold our return data, that can persist after session.close() is called

    try:
        # use below line to replace above form get, to now get the JSOn that comes back from our AJAX request
        description_input = request.get_json()['description'] # gets the json body sent to it from index.html ==> body: JSON.stringify.... returns a dictionary, with key description
        listid_input = request.get_json()['list_id']

        #use the description received above to create a new Todo objet
        todo = Todo(description=description_input, list_id=listid_input)
        # add the todo object to a db session == pending change, not yet commited
        db.session.add(todo)
        # commit the change
        db.session.commit()
        # next, tell the controller what to render to the user after committing a new record to the DB
        # in this case, we want to redirect to the index route and show the index.html page, with a fresh grab of all the new DB table values
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description
        body['list_id'] = todo.list_id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close() # close connection before return statement
    if error:
        abort(500) #invoked in case of a databse error
    else:
        # import redirect and urslfor
        # default return ### == return redirect(url_for('index')) # index == name of our route handler that listens to changes on the index route. allows for a page refresh every time you create a todo
        # OR
        # return render_template('index.html', data=Todo.query.all())
        # OR return below if USING AJAX ==> we want to return a jsonobject that includes the new description
        # below brings an error because we are trying to still use an object (todo) after closing the session it was using
        """
        return jsonify({ #returns json data to the client
            'description':todo.description # add description from todo onject
        })
        """
        #instead implement it as below
        return jsonify(body)


@app.route('/todos/<delete_id>', methods=['DELETE'])
def set_deleted_todo(delete_id):
    try:
        Todo.query.filter_by(id=delete_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    #return redirect(url_for('index'))
    return jsonify({'success': True})


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index')) # grabs all the to-do items and refreshes the entire page of to-do items

#updating the above so that user doesn't see all the todo items, but rather just the list of todos, then later can click into it to see the items
@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', 
                           lists = TodoList.query.all(), 
                           active_list = TodoList.query.get(list_id), 
                           todos = Todo.query.filter_by(list_id=list_id).order_by('id').all())


@app.route('/')
def index(): 
    # == CONTROLLER
    # figures out what the user should view next (index.html), and Model to be modelled (data=...)
    # return a template pointing to index.html, and reading a data object, in this case a list of data from the Todo table
    # 1) accept user input from a request
    # 2) tell the Todo Model to create a todo item
    # 3) direct how the view should update upon creating a new todo item
    # below ==> READ part in CRUD
    # return render_template('index.html', todos=Todo.query.order_by('id').all()) # see all the todo items in the DB
    return redirect(url_for('get_list_todos', list_id=1)) #loads the route showing the get_list_todos
 


"""
THIS ONE HAD DUMMY DATA
def index():
    # return a template pointing to index.html, and reading a data object, in this case a dictionry*
    return render_template('index.html', data=[{
        'description': 'Todo 1'
    }, {
        'description': 'Todo 2'
    }, {
        'description': 'Todo 3'
    }]) 
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)