# sandbox-todoapp-steps
MVC Model, CRUD implementations, POST vs GET, using AJAX fetch, definiting several routes and their route handlers.

## Some notes as we go along with this development
### notes about using JINJA in index.html
1. <!-- use a Jinja for loop to iterate through and display a DATA list, then have it print the description attribute-->
2. <!-- {% %} how to start and end a string block in Jinja-->
3. <!-- {{ ... }} how to start and end a print statement-->
4. ==> Jinja is a templating engine in Flask
#### If-statements in Jinja
{% if todo.completed %}
<ul>
{% for user in users %}
    <li>{{ user.completed|e }}</li>
{% endfor %}
</ul>
{% enfif %}

### notes about the 3 ways of getting user data in FLASK
Method 1: URL Query params ==> /foo?field1=value1 ==> value1 = request.args.get('field1')

Method 2: Forms ==> use request.form ==> username = request.form.get('username') == name attribute on the element
    e.g. input type="text" value="morangi" id="user" name="username"

Method 3: JSON ==> application/json ==> use request.data ==> data_string = request.data ... data_dictionary = json.loads(data_string)

### CHANGING the traditional HTML form that we were using in order to create to-do items using AJAX requests that FETCH in order to create to-do items instead

AIM: show updated todo list after hitting the CREATE button without refreshing the whole page all the time
1. Add a SCRIPT in the body tag of our VIEW
   the script will; 1) we send the POST request 2) then it returns a json, then 3) we use that json response to append a child
2. Add a CATCH block to catch any errors; via a div , with a hidden class, define the hidden attributes under style in head tag
3. On the controller (in app.py); update --> request.form.get('description', '') to --> request.get_json()['key'] AND return json data (via jsonify)

### U in CRUD -- Update
- add check boxes next to do items and update its status true/false
- 
