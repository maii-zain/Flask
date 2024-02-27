from bson import ObjectId
from flask import Flask, redirect, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='template')
app.config["MONGO_URI"]="mongodb://127.0.0.1:27017/flask"
mongo=PyMongo(app)

@app.route("/")
def DefaultPage():
    return render_template('Index.html')

@app.route('/AddUser', methods=['GET', 'POST'])
def AddUser():
    if request.method == 'GET':
       return render_template('AddUser.html') 

    elif request.method =='POST':
        name = request.form.get('name')
        age = request.form.get('age')
        Course = request.form.get('Course')
        Branch = request.form.get('Branch')
        if name and age and Course and Branch: 
            mongo.db.instructor.insert_one({'name': name, 'age': age,  'Course': Course, 'Branch': Branch})
    return redirect('/UsersList')

@app.route('/UsersList')
def ListUsers():
    data = list(mongo.db.instructor.find({}))
    return render_template('UserList.html', users=data)

@app.route('/EditUser/<string:_id>', methods=['GET', 'POST'])
def EditUser(_id):
    user = mongo.db.instructor.find_one({'_id': ObjectId(_id) })
    if request.method == 'POST':
        user['name'] = request.form.get('name')
        user['age'] = request.form.get('age')
        user['Course'] = request.form.get('Course')
        user['Branch'] = request.form.get('Branch')
        mongo.db.instructor.update_one({'_id': ObjectId(_id)}, {'$set': user})
        return redirect('/UsersList')
    return render_template('EditUser.html', user=user)

@app.route('/DeleteUser/<string:_id>')
def DeleteUser(_id):
    mongo.db.instructor.delete_one({'_id': ObjectId(_id)})
    return redirect('/UsersList')

if __name__ == '__main__':
    app.run(debug=True)
