from flask import *
from database import *
from admin import *

public = Blueprint('public',__name__)

@public.route('/')
def home():
	data = {}
	notif = "SELECT * FROM notification WHERE departmentID=0 ORDER BY notificationID DESC LIMIT 5"
	data['notifications'] = select(notif)

	return render_template('home.html',data=data)

@public.route('/contact_public')
def contact():
	user='public'
	return render_template('contact.html',user=user)

@public.route('/login',methods=['get','post'])
def login():
	if 'login' in request.form:
		uname = request.form['uname']
		pword = request.form['pword']

		loginQry = "SELECT * FROM login WHERE username='%s' AND password='%s'"%(uname,pword)
		sel = select(loginQry)

		if sel:
			session['loginID']=sel[0]['loginID']
			if sel[0]['userType']=='admin':
				session['desig'] = 'Admin'
				return redirect(url_for('admin.adminHome'))
			elif sel[0]['userType']=='HOD':
				q="SELECT * FROM hod WHERE loginID = '%s'"%(session['loginID'])
				val=select(q)
				if val:
					session['hodId']=val[0]['hodID']
					session['desig']='HOD'
					res = "SELECT firstName FROM hod WHERE loginID='%s'"%(session['loginID'])
					name = select(res)
					session['name'] = name[0]['firstName']
					return redirect(url_for('hod.hodHome'))
			elif sel[0]['userType']=='Teacher':
				q="SELECT * FROM teachers WHERE loginID = '%s'"%(session['loginID'])
				val=select(q)
				if val:
					session['teachersID'] = val[0]['teachersID']
					session['desig'] = 'Teacher'
					res = "SELECT firstName FROM teachers WHERE loginID='%s'"%(session['loginID'])
					name = select(res)
					session['name'] = name[0]['firstName']
					return redirect(url_for('teacher.teacherHome'))
			elif sel[0]['userType']=='Student':
				q="SELECT * FROM students WHERE loginID = '%s'"%(session['loginID'])
				val=select(q)
				if val:
					session['studentID'] = val[0]['studentID']
					session['desig'] = 'Student'
					res = "SELECT firstName FROM students WHERE loginID='%s'"%(session['loginID'])
					name = select(res)
					session['name'] = name[0]['firstName']
					return redirect(url_for('student.studentHome'))
			elif sel[0]['userType']=='Staff':
				q="SELECT * FROM staff WHERE loginID = '%s'"%(session['loginID'])
				val=select(q)
				if val:
					session['staffID'] = val[0]['staffID']
					session['desig'] = 'Staff'
					res = "SELECT firstName FROM staff WHERE loginID='%s'"%(session['loginID'])
					name = select(res)
					session['name'] = name[0]['firstName']
					return redirect(url_for('staff.staffHome'))
			elif sel[0]['userType']=='Principal':
				session['desig'] = 'Principal'
				res = "SELECT firstName FROM principal WHERE loginID='%s'"%(session['loginID'])
				name = select(res)
				session['name'] = name[0]['firstName']
				return redirect(url_for('principal.principalHome'))

	return render_template('login.html')