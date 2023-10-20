from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://evemwangi:Nima900##@localhost:5432/todoapp'
app.app_context().push()
db = SQLAlchemy(app)

class Todo(db.Model): # == MODEL
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<TODO {self.id} {self.description}>'

db.create_all()

@app.route('/')
def index(): 
    # == CONTROLLER
    # figures out what the user should view next (index.html), and Model to be modelled (data=...)
    # return a template pointing to index.html, and reading a data object, in this case a list of data from the Todo table
    # 1) accept user input from a request
    # 2) tell the Todo Model to create a todo item
    # 3) direct how the view should update upon creating a new todo item
    # below ==> READ part in CRUD
    return render_template('index.html', data=Todo.query.all())

@app.route('/todos/create', methods=['POST']) # == ROUTE
def create_todo(): # == ROUTE HANDLER
    #fetch the data submitted by the user, add an empty string as a default
    # description_input = request.form.get('description', '')

    error = False
    body = {} #empty dictionary == will hold our return data, that can persist after session.close() is called

    try:
        # use below line to replace above form get, to now get the JSOn that comes back from our AJAX request
        description_input = request.get_json()['description'] # gets the json body sent to it from index.html ==> body: JSON.stringify.... returns a dictionary, with key description

        #use the description received above to create a new Todo objet
        todo = Todo(description=description_input)
        # add the todo object to a db session == pending change, not yet commited
        db.session.add(todo)
        # commit the change
        db.session.commit()
        # next, tell the controller what to render to the user after committing a new record to the DB
        # in this case, we want to redirect to the index route and show the index.html page, with a fresh grab of all the new DB table values
        body['description'] = todo.description
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