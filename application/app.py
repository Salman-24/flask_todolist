# importing the required PYPI modules:
from flask import Flask, render_template, url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy # for connection of the application to the database.
from datetime import datetime

# creating a new flask object:
app = Flask(__name__)

# setting up the database connection coniguration for the application:

# database location:
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

# database intiallization:
db = SQLAlchemy(app)

# database model:
class todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return("Task - {}".format(self.id))

# application routing functions:

# home page:
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST": # if new task is added.
        task_content = request.form["content"]
        new_task = todolist(content= task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return(redirect("/"))
        except:
            return("There was an error in adding values to the database.")

    else: # if no new task is added.
        tasks = todolist.query.order_by(todolist.date_created).all() # retrive all the data.
        return render_template("index.html", tasks = tasks)

# task deletion:
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = todolist.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return(redirect("/"))
    except:
        return("There was an error in deleting the value from the database.")

# task update:
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = todolist.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]
        
        try:
            db.session.commit()
            return(redirect("/"))
        except:
            return("There was an error in updating the value.")
        
    else:
        return render_template("update.html", task=task)

# calling the application:
if __name__ == "__main__":
    app.run(debug = True)