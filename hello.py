from flask import Flask, render_template, request,url_for,redirect
import json , requests, os
from db import initialize, createuser, finduser,getlist


cookies={}
username={}
item={}
items={}
cursor={}
connect={}

url ='https://hunter-todo-api.herokuapp.com/user'
app = Flask(__name__)



with open('data.json') as file:
	data = json.load(file)
	



@app.route('/', methods=['GET','POST'])
def register():

	##try:
	c,conn =initialize()
	global cursor
	global connect
	cursor=c
	connect=conn
		##return("okay")
	##except Exception as e:
		##return (str(e))
		
	if request.method=='POST':
		user=request.form['newusername']	
		output=createuser(user,c,conn)
		
		'''r= requests.post('https://hunter-todo-api.herokuapp.com/user', json={'username':user})
		text = json.loads(r.text)
		print(text)'''
		print(output)
		if output==False:
			return render_template('register.html')
		else:
			return redirect(url_for("login"))
	else:
		return render_template('register.html')


@app.route('/login')
def login():
	return render_template('login.html')




@app.route('/login', methods=['POST'])
def loginPost():
	user=request.form['username']
	global username
	global cookies
	
	username=user
	
	
	'''username={"username":user}
	r = requests.post('https://hunter-todo-api.herokuapp.com/auth', json={"username":user})

	text = json.loads(r.text) 
	print(text)
	cookies={"sillyauth":text["token"]}

	requests.post('https://hunter-todo-api.herokuapp.com/auth', cookies=cookies, json=username) '''
	
	output=finduser(username,cursor,connect)
	
	
	
	print(output)
	

	return redirect(url_for('todo'))




@app.route('/todo')
def todo():
	
	'''r=requests.get('https://hunter-todo-api.herokuapp.com/todo-item',cookies=cookies)
	text=json.loads(r.text)
	print(text)'''
	global items
	items = getlist(username,cursor,connect)
	return render_template('todo.html', tasks=items)



@app.route('/todo', methods=['POST'])
def todoPost():
	if 'add' in request.form:
	
		name=request.form['add'] #gets item name from input box
		item = {"content":name}	#stores item into json type file
		
		r=requests.post('https://hunter-todo-api.herokuapp.com/todo-item', cookies=cookies,json=item)	#posts item into API
		r=json.loads(r.text)
		print(r)
		r=requests.get('https://hunter-todo-api.herokuapp.com/todo-item',cookies=cookies)
		tasks=json.loads(r.text)
		print(tasks)
		
	""" else:
		requests.get('https://hunter-todo-api.herokuapp.com/todo-item',cookies=cookies) """
	
	return render_template('todo.html',tasks=tasks)

@app.route('/change/<string:id>')
def changePost(id):
	url ='https://hunter-todo-api.herokuapp.com/todo-item/' +id
	r=requests.get(url, cookies=cookies)
	
	global item
	item = json.loads(r.text)
	print(item)

	return redirect(url_for('edit',id=id))

@app.route('/edit<string:id>',methods=['GET','POST'])
def edit(id):
	url ='https://hunter-todo-api.herokuapp.com/todo-item/' +id
	if(request.method=='POST') :
		text=request.form['edit']
		item['content']=text
		print(text)
		print(item['content'])
		requests.put(url,cookies=cookies, json=item)
		return redirect(url_for('todo',id=id))
	else:
		requests.get(url,json=item)
		return render_template('edit.html',item=item)

	
	

@app.route('/delete/<string:id>')
def deletePost(id):
	url ='https://hunter-todo-api.herokuapp.com/todo-item/' +id
	r=requests.delete(url, cookies=cookies)
	
	return redirect(url_for('todo'))


	
@app.route('/done/<string:id>')
def donePost(id):
	url ='https://hunter-todo-api.herokuapp.com/todo-item/' +id
	r=requests.get(url, cookies=cookies)
	
	
	item = json.loads(r.text)
	item['completed']=True
	requests.put(url, cookies=cookies, json=item)

	return redirect(url_for('todo'))


@app.route('/logout',methods=['GET','POST'])
def logout():
	
	return render_template("logout.html")	


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)
