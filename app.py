from flask import Flask, render_template, request, redirect, jsonify
import sqlite3 as sql
app = Flask(__name__, static_folder="static_dir")


@app.route("/entry", methods=["GET"])
def fun_get():
	print("here")
	s={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select course_name,course_id from course")
		for row in cur:  
			c=0
			st=""
			f=0
			for x in row:
				if(c%2==0):
					st=x
				else:
					f=x
				c+=1
				s[st]=x	
		con.commit()
	con.close()
	return render_template("index.html",msg=s)

@app.route("/entry", methods=["POST"])
def func_post():
	print ("in 2")
	topic=request.args.get('id')
	topic=str(topic)
	print (topic)
	s=[]
	s.clear()
	rowid = None
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("INSERT INTO course (course_name) VALUES (?)",[topic])
		con.commit()
		row = cur.execute("SELECT * FROM course where course_id = (?)" , [cur.lastrowid]).fetchone()
	con.close()
	return jsonify({'course_id': row[0], 'course_name': row[1]})

@app.route("/entry", methods=["DELETE"])
def func_del():
	print ("in 3")
	ss=request.args.get('id')
	print ("from DELETE-> "+ss)
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("DELETE From course where course_name=(?)",[ss])
		con.commit()
	con.close()
	j=1
	s={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select course_name,course_id from course")
		for row in cur:  
			c=0
			f=0
			for x in row:
				if(c%2==0):
					st=x
				else:
					f=x
				c+=1
				s[st]=x	
		con.commit()
	con.close()
	# print (s)
	return render_template("index.html",msg=s)

@app.route("/course/<variable>", methods=["GET"])
def fun_course(variable):
	print ("course --> "+variable)
	s={}
	c_name=variable.replace('-',' ')
	cid=1
	with sql.connect("hack.db") as con:
		curr=con.cursor()
		curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (curr.fetchone()[0])
		con.commit()
	con.close()

	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT title from problem where course_id=(?)",[cid])
		for row in cur:  
			c=0
			st=""
			f=0
			for x in row:
				if(c%2==0):
					st=x
				else:
					f=x
				c+=1
				s[st]=x	
		con.commit()
	con.close()
	return render_template("course.html",cn=variable, msg=s)

@app.route("/course/<variable>", methods=["POST"])
def fun_cpost(variable):
	title=request.form["title"]
	problem=request.form["problem"]
	canswer=request.form["canswer"]
	wanswer1=request.form["wanswer1"]
	wanswer2=request.form["wanswer2"]
	wanswer3=request.form["wanswer3"]
	c_name=variable.replace('-',' ')
	cid=1
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (cur.fetchone()[0])
		cur=con.cursor()
		cur.execute("INSERT INTO problem (title,problem,canswer,wanswer1,wanswer2,wanswer3,course_id) VALUES (?,?,?,?,?,?,?)",(title,problem,canswer,wanswer1,wanswer2,wanswer3,cid))
		con.commit()
	con.close()
	s={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select title from problem where course_id=(?)",[cid])
		for row in cur:  
			c=0
			st=""
			f=0
			for x in row:
				if(c%2==0):
					st=x
				else:
					f=x
				c+=1
				s[st]=x	
		con.commit()
	con.close()
	print (s)
	return render_template("course.html",cn=variable, msg=s)

@app.route("/course/<variable>", methods=["DELETE"])
def cdelete(variable):
	c_name=variable.replace('-',' ')
	ss=request.args.get('id')
	print ("from DELETE-> "+ss)
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("delete from problem where problem.problem_id in (select problem_id from problem JOIN course ON problem.course_id=course.course_id where course_name=(?) and title=(?))",(c_name,ss))
		con.commit()
	con.close()
	j=1
	s={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select title from problem where course_id=(?)",[cid])
		for row in cur:  
			c=0
			st=""
			f=0
			for x in row:
				if(c%2==0):
					st=x
				else:
					f=x
				c+=1
				s[st]=x	
		con.commit()
	con.close()
	return render_template("course.html",cn=variable, msg=s)

@app.route("/problem/<variable>", methods=["GET"])
def display(variable):
	print ("varr--> "+ variable)
	c_name=variable.replace('-',' ')
	cid=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT * FROM problem WHERE title= (?)",[c_name])
		cid= (cur.fetchone())
		con.commit()
	con.close()	
	print (cid)
	return render_template("question_display.html",problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])

