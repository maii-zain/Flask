from flask import Flask, redirect, render_template, request
app = Flask(__name__)


users=[]
def get_next_id():
    if len(users)!=0:
        return users[-1]['id']+1
    else :
        return 1
     
     
@app.route('/users')
def get_users():
    name = request.args.get('name')
    age = request.args.get('age')
    location = request.args.get('location')
    
    if name is not None or age is not None or location is not None:
        users.append({"id": get_next_id(), "name": name, "age": age, "location": location})
        
  
    
    if users:
        return render_template('users.html', MyUsers=users)
    else:
        return "<h1>Empty list of users</h1>"


@app.route('/delete/<int:id>') 
def delete_user(id):
    if id != None and len(users) !=0 : 
        for i in range(len(users)):
            if users[i]['id']==id:
                del users[i]
                print("Found and Delete")
                break

    return redirect('/users')

@app.route('/update/<int:id>') 
def update_user(id):
    updated_name = request.args.get('name')
    updated_age = request.args.get('age')
    updated_location = request.args.get('location')

    for user in users:
        if user['id'] == id:
            if updated_name is not None:
                user['name'] = updated_name
            if updated_age is not None:
                user['age'] = updated_age
            if updated_location is not None:
                user['location'] = updated_location
            break

    return redirect('/users')

               
    
  


@app.route('/')
def hello_world():
   return "Welcome guest"

if __name__ == '__main__':
    app.run(debug=True)
