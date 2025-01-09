from flask import Flask
from public import public
from admin import admin
from hod import hod
from teacher import teacher
from student import student
from staff import staff
from principal import principal

app=Flask(__name__)

app.secret_key='car'

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(hod)
app.register_blueprint(teacher)
app.register_blueprint(student)
app.register_blueprint(staff)
app.register_blueprint(principal)

app.run(debug=True,port=5004)