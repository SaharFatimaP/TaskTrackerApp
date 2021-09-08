from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cors = CORS(app, resources={
    r"/*":{
        "origin": "*"
    }
})

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tracker.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"{self.name}-{self.description}"


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


task_schema = TaskSchema()
task_schemas = TaskSchema(many=True)

#get api 
@app.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    serialize = jsonify(task_schemas.dump(tasks))
    #dump serialize into python object
    # serialize.headers.add("Access-Control-Allow-Origin", "*")
    return serialize


#post api

@app.route("/add_tasks/", methods=['GET', 'POST'])
def add_tasks():
    if request.method == 'POST':
        name = request.json['name']
        description = request.json['description']
        task = Task(name=name, description=description)
        db.session.add(task)
        db.session.commit()

        serialize_task = jsonify(task_schema.dump(task))
        # serialize_task.headers.add("Access-Control-Allow-Origin", "*")
        return serialize_task

    else:
        tasks = Task.query.all()
        serialize_tasks = jsonify(task_schemas.dump(tasks))
        # serialize_tasks.headers.add("Access-Control-Allow-Origin", "*")
        return serialize_tasks

  
#update api    
@app.route("/update_tasks/<int:id>", methods=['POST', 'GET'])
def update_tasks(id):
    task = Task.query.get(id)
    if(request.method == 'POST'):
        name = request.json['name']
        description = request.json['description']
       
        task.name = name
        task.description = description
        db.session.add(task)
        db.session.commit()

        task_dump = task_schema.dump(task)
        
        return jsonify(task_dump)

    else:
        task_dump = task_schema.dump(task)
        return jsonify(task_dump)

@app.route("/delete_tasks/<int:id>", methods=['DELETE'])
def delete_tasks(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    serialize = task_schema.dump(task)
    return jsonify(serialize)


if(__name__ == "__main__"):
    app.run(debug="True")