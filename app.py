from flask import Flask, render_template, request, redirect, jsonify
import random
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

ci=[]
pre=[]
bucket=[[]]
@app.route("/course/<variable>/preview-course", methods=["GET"])
def preview(variable):
	c_name=variable.replace('-',' ')
	ci.clear()
	print("coursname-->"+c_name)
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select problem_id from problem join course on course.course_id=problem.course_id where course_name= (?)",[c_name])
		for row in cur:
			for x in row:
				ci.append(x)
		con.commit()
	con.close()	
	cid=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT * FROM problem WHERE problem_id= (?)",[ci[0]])
		cid= (cur.fetchone())
		con.commit()
	con.close()	
	pre.clear()
	pre.append(ci[0])
	pre.append(0)
	ci.remove(ci[0])
	print(pre)
	print (ci)
	bucket.clear()
	bucket.append(ci)
	bucket.append([])
	bucket.append([])
	bucket.append([])
	return render_template("preview.html",name=variable,problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])

@app.route("/course/<variable>/preview-course", methods=["POST"])
def prev_pos(variable):
	c_name=variable.replace('-',' ')
	print("*********************************************")
	print (bucket)
	wrong=request.args.get('id')
	print(wrong)
	if(wrong==0):
		bucket[0].append(pre[1])
	else:
		bucket[pre[0]+1].append(pre[1])
	pre.clear()
	if(len(bucket[0])==0 and len(bucket[1])==0 and len(bucket[2])==0 and len(bucket[3])==0):
		return render_template("course_end.html",x="Congratulations! Course Ended.")
	ra=random.randint(0,3)
	while(len(bucket[ra])==0):
		ra=(ra+1)%4
	pre.append(ra);
	ra1=random.randint(0,len(bucket[ra])-1)
	pre.append(bucket[ra][ra1])
	

	cid=[]
	el=pre[1]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT * FROM problem WHERE problem_id= (?)",[el])
		cid= (cur.fetchone())
		con.commit()
	con.close()	
	bucket[ra].remove(el)
	return render_template("preview.html",name=variable,problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])


@app.route("/course/set-dependencies/<variable>", methods=["GET"])
def dependency(variable):
	s={}
	c_name=variable.replace('-',' ')
	print("kuch bhi"+c_name)
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
	return render_template("dependencies.html", msg=s)
