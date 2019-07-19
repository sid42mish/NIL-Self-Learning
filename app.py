
from flask import Flask, render_template, request, redirect, jsonify, make_response
import random
import queue
import sqlite3 as sql
app = Flask(__name__, static_folder="static_dir")

# # debug mode on
# if __name__ == "__main__":
# 	app.run(debug=True)

def resetdb():
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("delete from bucket1")
		cur.execute("delete from bucket2")
		cur.execute("delete from savedata")
		cur.execute("delete from bucket3")
		cur.execute("update user_rating set rating=1500")
		cur.execute("update problem set rating=1500")
		cur.execute("INSERT INTO bucket1 select problem_id, course_id from problem")
	con.close()
resetdb()

def tellpid(title,cid):
	z=1
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select problem_id from problem where title=(?) and course_id=(?)",[title,cid])
		z=cur.fetchone()[0]
		con.commit()
	con.close()
	return z

def set_dependency(cid):
	mp={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		x=list(cur.execute("select problem_id from problem where course_id=(?)",[cid]))
		for i in x:
			print(i[0])
			mp[i[0]]=[]
		vec=list(cur.execute("select distinct * from dependencies where course_id=(?)",[cid]))
		for i in vec:
			mp[tellpid(i[1],cid)].append(tellpid(i[0],cid))
		print("mmmmmmmmmmmpppppppppppppp->",mp)
		con.commit()
	con.close()
	return mp

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
		cur.execute("Select distinct course.course_id from course join problem on problem.course_id= course.course_id where course_name=(?)",[ss])
		cid=(cur.fetchone())
		cur.execute("DELETE From course where course_name=(?)",[ss])
		cur.execute("DELETE From problem where course_id=(?)",[cid])

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
	correct_opt=request.form["option"]
	explanation=request.form["explain"]
	print ("title--> "+title)
	c_name=variable.replace('-',' ')
	cid=1
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (cur.fetchone()[0])
		cur=con.cursor()
		cur.execute("INSERT INTO problem (title,problem,canswer,wanswer1,wanswer2,wanswer3,course_id,correct_opt,explanation) VALUES (?,?,?,?,?,?,?,?,?)",[title,problem,canswer,wanswer1,wanswer2,wanswer3,cid,correct_opt,explanation])
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
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT problem_id FROM problem WHERE title= (?)",[title])
		pid= (cur.fetchone()[0])
		cur.execute("insert into bucket1 VALUES (?,?)",(pid,cid))
		con.commit()
	con.close()
	return render_template("course.html",cn=variable, msg=s)

@app.route("/course/<variable>", methods=["DELETE"])
def cdelete(variable):
	c_name=variable.replace('-',' ')
	ss=request.args.get('id')
	print ("from DELETE-> "+ss+"  c_name->"+c_name)
	##DELETE A PROBLEM FROM DB
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("delete from bucket1 where bucket1.problem_id in (select problem_id from problem JOIN course ON problem.course_id=course.course_id where course_name=(?) and title=(?))",(c_name,ss))
		cur.execute("delete from bucket2 where bucket2.problem_id in (select problem_id from problem JOIN course ON problem.course_id=course.course_id where course_name=(?) and title=(?))",(c_name,ss))
		cur.execute("delete from bucket3 where bucket3.problem_id in (select problem_id from problem JOIN course ON problem.course_id=course.course_id where course_name=(?) and title=(?))",(c_name,ss))
		cur.execute("delete from problem where problem.problem_id in (select problem_id from problem JOIN course ON problem.course_id=course.course_id where course_name=(?) and title=(?))",(c_name,ss))
		con.commit()
	con.close()
	j=1
	s={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select distinct title from problem where title=(?)",[c_name])
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
	return render_template("question_display.html",title=cid[1],problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])

ci=[]
pre=[]
bucket=[[]]



@app.route("/course/<variable>/preview-course", methods=["GET"])
def preview(variable):
	c_name=variable.replace('-',' ')
	ci.clear()
	print("coursname-->"+c_name)
	bucket.clear()

	resetdb()
	cid=1;
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid=cur.fetchone()[0]
		cur.execute("select distinct problem_id from bucket1 join course on course.course_id=bucket1.course_id where course_name= (?)",[c_name])
		t=cur.fetchall()
		l=[]
		for i in t:
			l+=i
		bucket.append(l)
		
		cur.execute("select distinct problem_id from bucket2 join course on course.course_id=bucket2.course_id where course_name= (?)",[c_name])
		t=cur.fetchall()
		l=[]
		for i in t:
			l+=i
		bucket.append(l)
		
		cur.execute("select distinct problem_id from bucket3 join course on course.course_id=bucket3.course_id where course_name= (?)",[c_name])
		t=cur.fetchall()
		l=[]
		for i in t:
			l+=i
		bucket.append(l)
		
	con.close()
	bucket.append([])
	print (bucket)
	pre.clear()
	f=0

	if (len(bucket[0])!=0):
		pre.append(bucket[0][0])
		pre.append(0)
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("delete from bucket1 where problem_id=(?)",[bucket[0][0]])
			con.commit()
		con.close()
		f=1
	elif (len(bucket[1])!=0):
		pre.append(bucket[1][0])
		pre.append(1)
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("delete from bucket2 where problem_id=(?)",[bucket[1][0]])
			con.commit()
		con.close()
		f=1
	elif (len(bucket[0])!=0):
		pre.append(bucket[2][0])
		pre.append(2)
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("delete from bucket3 where problem_id=(?)",[bucket[2][0]])
			con.commit()
		con.close()
		f=1
	
	if (f==0):
		return render_template("course_end.html",x="Congratulations! Course Ended.")

	cid=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select * from problem where problem_id=(?)",[pre[0]])
		cid=list(cur.fetchone())
		ra=pre[1]
		el=pre[0]
		cur.execute("DELETE FROM savedata")
		cur.execute("INSERT into savedata VALUES (?,?)",(ra,el))	
		con.commit()
	con.close()		
	print (bucket)

	return render_template("preview.html",name=variable,title=cid[1],problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])


@app.route("/course/<variable>/preview-course", methods=["POST"])
def prev_pos(variable):
	c_name=variable.replace('-',' ')
	c_id=0;
	with sql.connect("hack.db") as con:			#finding the course
		cur=con.cursor()
		cur.execute("select course_id from course where course_name=(?)",[c_name])
		c_id=(cur.fetchone()[0])
		con.commit()
	con.close()
	
	print (bucket)
	submi=str(request.form['select'])
	tit=str(request.form['title'])
	if submi is not None and tit is not None:
		print("you are in the check portion")
		with sql.connect("hack.db") as con:		
			cur=con.cursor()
			cur.execute("select problem_id from problem where title=(?) and course_id=(?)",[tit,c_id])
			pid=(cur.fetchone()[0])
			cur.execute("select correct_opt from problem where problem_id=(?)",[pid])
			right=(cur.fetchone()[0])
			cur.execute("select * from problem where problem_id=(?)",[pid])
			cid=(cur.fetchone())		
			con.commit()
		con.close()
		print("fdmjlaksdjflkasdjflkd",submi==right)
		if (right==submi):
			print ("right answer")
		return jsonify({'right':right, 'submi':submi})
			

	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select * from savedata")
		fu=list(cur.fetchone())
		ra=fu[0]
		el=fu[1]
		print (fu)
		bucket[ra].remove(el)
		con.commit()
	con.close()
	wrong = request.form['mcq']
	if wrong!='ca':    #for rating update
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("SELECT rating from problem where  problem_id=(?)",[pre[0]]	)
			rat=cur.fetchone()[0]
			rat=rat+int(10*rat/1500)
			cur.execute("update problem set rating=(?) where problem_id=(?)",(rat,pre[0]))
			cur.execute("SELECT rating from user_rating where user_id=1")
			rat=cur.fetchone()[0]
			rat=rat-int(50*rat/1500)
			cur.execute("update user_rating set rating=(?) where user_id=1",[rat])
			con.commit()
		con.close()
	else:
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("SELECT rating from problem where  problem_id=(?)",[pre[0]])
			rat=cur.fetchone()[0]
			rat=rat-int(50*rat/1500)
			cur.execute("update problem set rating=(?) where problem_id=(?)",(rat,pre[0]))
			cur.execute("SELECT rating from user_rating where user_id=1")
			rat=cur.fetchone()[0]
			rat=rat+int(10*rat/1500)
			cur.execute("update user_rating set rating=(?) where user_id=1",[rat])
			con.commit()
		con.close()

	with sql.connect("hack.db") as con:
		cur=con.cursor()
		if (ra==0):
			cur.execute("DELETE FROM bucket1 WHERE problem_id=(?) and course_id=(?)",(el,c_id))
		if (ra==1):
			cur.execute("DELETE FROM bucket2 WHERE problem_id=(?) and course_id=(?)",(el,c_id))
		if (ra==2):
			cur.execute("DELETE FROM bucket3 WHERE problem_id=(?) and course_id=(?)",(el,c_id))
		con.commit()
	con.close()

	print("*********************************************")
	print (bucket)
	print(pre)
	if wrong!='ca':
		cid=c_id
		mp=set_dependency(cid)
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			L=queue.Queue(maxsize=1000000)
			print ("wrong")
			L.put(pre[0])
			while(not L.empty()):
				z=L.get()
				cur.execute("DELETE FROM bucket1 WHERE problem_id=(?) and course_id=(?)",(z,c_id))
				cur.execute("DELETE FROM bucket2 WHERE problem_id=(?) and course_id=(?)",(z,c_id))
				cur.execute("DELETE FROM bucket3 WHERE problem_id=(?) and course_id=(?)",(z,c_id))
		
				cur.execute("INSERT INTO bucket1 VALUES (?,?)",(z,c_id))
				if z not in bucket[0] and z not in bucket[3]:
					print ("YES")
					bucket[0].append(z)
				if z in bucket[1]:
					bucket[1].remove(z)
				if z in bucket[2]:
					bucket[2].remove(z)
				# print (z)	
				# print (z, mp[z])
				for i in mp[z]:
					L.put(i)
			con.commit()
		con.close()
	else:
		print ("correct")
		bucket[pre[1]+1].append(pre[0])
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			if (pre[1]==0):
				cur.execute("INSERT INTO bucket2 VALUES (?,?)",(pre[0],c_id))
			if (pre[1]==1):
				cur.execute("INSERT INTO bucket3 VALUES (?,?)",(pre[0],c_id))
			con.commit()
		con.close()
	pre.clear()
	print(bucket)
	if(len(bucket[0])==0 and len(bucket[1])==0 and len(bucket[2])==0 ):
		grade=''
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			rat=cur.execute("SELECT rating from user_rating where user_id=1").fetchone()[0]
			rat=int(rat)
			if(rat>2000):
				grade='A+'
			elif(rat>1700):
				grade='A'
			elif(rat>1300):
				grade='B+'
			elif(rat>1000):
				grade='B'
			else:
				grade='C'

			con.commit()
		con.close()
		return render_template("course_end.html",x="Congratulations! Course Ended.",grade=grade)
	ra=random.randint(0,2)
	
	while(len(bucket[ra])==0):
		ra=(ra+1)%3
	ra1=random.randint(0,len(bucket[ra])-1)
	pre.append(bucket[ra][ra1])
	pre.append(ra);
	
	cid=[]
	el=pre[0]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT * FROM problem WHERE problem_id= (?)",[el])
		cid= (cur.fetchone())
		cur.execute("DELETE FROM savedata")
		cur.execute("INSERT into savedata VALUES (?,?)",(ra,el))	
		con.commit()
	con.close()	
	
	print (bucket)
	
	return render_template("preview.html",name=variable,title=cid[1],problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])


@app.route("/course/set-dependencies/<variable>", methods=["GET"])
def dependency(variable):
	c_name=variable.replace('-',' ')
	cid=1
	with sql.connect("hack.db") as con:
		curr=con.cursor()
		curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (curr.fetchone()[0])
		con.commit()
	con.close()
	s=[]
	dep=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT title from problem where course_id=(?)",[cid])
		x=cur.fetchall()
		for i in x:
			s.append(i[0])
		cur.execute("SELECT  distinct x,y from dependencies where course_id=(?)",[cid])
		x=cur.fetchall()
		print (x)

		for i in x:
			l=[]
			l.append(i[0])
			l.append(i[1])
			dep.append(l)
	
	con.close()
	return render_template("dependencies.html", msg=s,x=dep,variable=variable)

@app.route("/course/set-dependencies/<variable>", methods=["POST"])
def dependency_post(variable):
	c_name=variable.replace('-',' ')
	option1=str(request.form.get('val1'))
	option2=str(request.form.get('val2'))
	print(option1,option2)
	print ("set dependencies post for-->" + c_name)
	cid=1
	with sql.connect("hack.db") as con:
		curr=con.cursor()
		curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid=curr.fetchone()[0]
		if((option1!="None" and option2!="None") and (option1!="none" and option2!="none")) :
			print ("--------------------here-----------------------")
			curr.execute("INSERT INTO dependencies VALUES (?,?,?)",(option1,option2,cid))
		con.commit()
	con.close()
	s=[]
	dep=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT title from problem where course_id=(?)",[cid])
		x=cur.fetchall()
		for i in x:
			s.append(i[0])
		cur.execute("SELECT distinct x,y from dependencies where course_id=(?)",[cid])
		x=cur.fetchall()
		print (x)

		for i in x:
			l=[]
			l.append(i[0])
			l.append(i[1])
			dep.append(l)
	
	con.close()
	return render_template("dependencies.html", msg=s,x=dep,variable=variable)


@app.route("/course/set-dependencies/<variable>", methods=["DELETE"])
def dependency_remove(variable):
	print ("WE ARE IN DELETE METHOD")
	c_name=variable.replace('-',' ')
	option1=str(request.form['i1'])
	option2=str(request.form['i2'])
	print(option1,option2)
	cid=1
	with sql.connect("hack.db") as con:
		curr=con.cursor()
		curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (curr.fetchone()[0])
		curr.execute("DELETE FROM dependencies where x=(?) and y=(?)",(option1,option2))
		con.commit()
	con.close()
	s=[]
	dep=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT title from problem where course_id=(?)",[cid])
		x=cur.fetchall()
		for i in x:
			s.append(i[0])
		cur.execute("SELECT distinct x,y from dependencies where course_id=(?)",[cid])
		x=cur.fetchall()
	
		for i in x:
			l=[]
			l.append(i[0])
			l.append(i[1])
			dep.append(l)
	
	con.close()
	print (dep)
	return render_template("dependencies.html", msg=s,x=dep,variable=variable)

