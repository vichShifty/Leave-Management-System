from flask import *
from database import *

principal = Blueprint('principal',__name__)

@principal.route('/')
def home():
	return render_template('home.html')

@principal.route('/principalheader')
def principalheader():

	sel = "SELECT firstName FROM principal WHERE loginID='%s'"%(session['loginID'])
	name = select(sel)

	sel1 = "SELECT receipt FROM leaverequest WHERE loginID='%s' AND status='Accepted' ORDER BY leaveRequestID DESC LIMIT 1"%(session['loginID'])
	data= select(sel1)
	if data:
		receipt = data[0]['receipt']
	else:
		receipt = None

	return render_template('principalheader.html',name=name,receipt=receipt)

@principal.route('/principalHome')
def principalHome():
	current_page='principalHome'

	sel1 = "SELECT receipt FROM leaverequest WHERE loginID='%s' AND status='Accepted' ORDER BY leaveRequestID DESC LIMIT 1"%(session['loginID'])
	data= select(sel1)
	if data:
		receipt = data[0]['receipt']
	else:
		receipt = None


	sel2 = "SELECT * FROM leaverequest lr,login l where lr.loginID=l.loginID AND date=(select curdate())"
	data={}
	data['lr'] = select(sel2)
	
	return render_template('principalHome.html',current_page=current_page,receipt=receipt,data=data)

@principal.route('/contact_principal')
def contact():
	user='principal'
	return render_template('contact.html',user=user)

@principal.route('/sendLR_principal',methods=['get','post'])
def sendLR():

	data = {}

	sel = "SELECT leaveCount from login WHERE loginID = '%s'"%(session['loginID'])
	data['lc'] = select(sel)

	if 'sendReq' in request.form:
		dateOfLeave = request.form['dateOfLeave']
		leaveType = request.form['leaveType']

		ins = "INSERT INTO leaverequest VALUES(null,'%s','Principal','%s','%s','Pending','unread')"%(session['loginID'],dateOfLeave,leaveType)
		insert(ins)

		return redirect(url_for('principal.principalHome'))
	return render_template('sendLR.html',data=data)

@principal.route('/viewReqStatus_principal')
def viewReqStatus():
	data = {}
	sel = "SELECT * FROM leaverequest r ,login l WHERE r.loginID = l.loginID AND r.loginID='%s' AND receipt NOT LIKE 'read'"%(session['loginID'])
	data['reqStatus'] = select(sel)

	if 'action' in request.args:
		action = request.args['action']
		leaveReqId = request.args['leaveReqId']
	else:
		action = None

	if action == 'markAsRead':
		upd = "UPDATE leaverequest SET receipt='read' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		return redirect(url_for('principal.viewReqStatus'))

	return render_template('viewReqStatus.html',data=data)

@principal.route('/manageHOD_principal',methods=['get','post'])
def manageHOD():
	data={}
	sel = "SELECT * FROM hod"
	data['HOD'] = select(sel)

	dept = "SELECT * from department"
	data['deptID'] = select(dept)

	if 'addHOD' in request.form:
		departmentID = request.form['departmentID']
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		address = request.form['address']
		phoneNumber = request.form['phoneNumber']
		email = request.form['email']

		uname = request.form['uname']
		pword = request.form['pword']

		ins1 = "INSERT INTO login VALUES(null,'%s','%s','HOD',12)"%(uname,pword)
		insert(ins1)

		qry = "SELECT loginID from login WHERE username='%s'"%(uname)
		logID = select(qry)

		ins2 = "INSERT INTO hod VALUES(null,'%s','%s','%s','%s','%s','%s','%s')"%(logID[0]['loginID'],departmentID,firstName,lastName,address,phoneNumber,email)
		insert(ins2)
		return redirect(url_for('principal.manageHOD'))

	if 'action' in request.args:
		action = request.args['action']
		hodId = request.args['hodId']
	else:
		action = None

	if action == 'delete':
		d = "DELETE FROM hod WHERE hodID='%s'"%(hodId)
		delete(d)
		return redirect(url_for('principal.manageHOD'))

	if action == 'update':
		s = "SELECT * FROM hod WHERE hodID='%s'"%(hodId)
		data['upd'] = select(s)

		if 'updHOD' in request.form:
			departmentID = request.form['departmentID']
			firstName = request.form['firstName']
			lastName = request.form['lastName']
			address = request.form['address']
			phoneNumber = request.form['phoneNumber']
			email = request.form['email']

			upd = "UPDATE hod SET departmentID='%s',firstName='%s',lastName='%s',address='%s',phoneNumber='%s',email='%s' WHERE hodID='%s'"%(departmentID,firstName,lastName,address,phoneNumber,email,hodId)
			update(upd)
			return redirect(url_for('principal.manageHOD'))
	return render_template('manageHOD.html',data=data)

@principal.route('/manageTeachers_principal',methods=['get','post'])
def manageTeachers():
	data={}

	sel = "SELECT * FROM teachers"
	data['teachers'] = select(sel)

	dept = "SELECT * from department"
	data['deptID'] = select(dept)

	if 'addTeacher' in request.form:
		departmentID = request.form['departmentID']
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		address = request.form['address']
		phoneNumber = request.form['phoneNumber']
		email = request.form['email']

		uname = request.form['uname']
		pword = request.form['pword']

		ins1 = "INSERT INTO login VALUES(null,'%s','%s','Teacher',12)"%(uname,pword)
		insert(ins1)

		qry = "SELECT loginID from login WHERE username='%s'"%(uname)
		logID = select(qry)

		ins2 = "INSERT INTO teachers VALUES(null,'%s','%s','%s','%s','%s','%s','%s')"%(logID[0]['loginID'],departmentID,firstName,lastName,address,phoneNumber,email)
		insert(ins2)
		return redirect(url_for('principal.manageTeachers'))

	if 'action' in request.args:
		action = request.args['action']
		teacherId = request.args['teacherId']
	else:
		action = None

	if action == 'delete':
		d = "DELETE FROM teachers WHERE teachersID='%s'"%(teacherId)
		delete(d)
		return redirect(url_for('principal.manageTeachers'))

	if action == 'update':
		s = "SELECT * FROM teachers WHERE teachersID='%s'"%(teacherId)
		data['upd'] = select(s)

		if 'updTeacher' in request.form:
			departmentID = request.form['departmentID']
			firstName = request.form['firstName']
			lastName = request.form['lastName']
			address = request.form['address']
			phoneNumber = request.form['phoneNumber']
			email = request.form['email']

			upd = "UPDATE teachers SET departmentID='%s',firstName='%s',lastName='%s',address='%s',phoneNumber='%s',email='%s' WHERE teachersID='%s'"%(departmentID,firstName,lastName,address,phoneNumber,email,teacherId)
			update(upd)
			return redirect(url_for('principal.manageTeachers'))
	return render_template('manageTeachers.html',data=data)

@principal.route('/viewStudents_principal')
def viewStudents():
	data={}
	sel = "SELECT * FROM students"
	data['student'] = select(sel)

	return render_template('viewStudents.html',data=data)

@principal.route('/viewStaffLR_principal',methods=['get','post'])
def viewStaffLR():
	data = {}
	sel = "SELECT * FROM leaverequest r ,staff s WHERE r.loginID = s.loginID AND requestedBy='Staff' AND status ='Pending' ORDER BY leaveRequestID DESC"
	data['staffLR'] = select(sel)

	if 'action' in request.args:
		action = request.args['action']
		leaveReqId = request.args['leaveReqId']
	else:
		action = None

	if action == 'accept':
		upd = "UPDATE leaverequest SET status='Accepted' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		leave_type = select("SELECT type FROM leaverequest WHERE leaveRequestID='%s'" % leaveReqId)
		if leave_type[0]['type'] == 'Half Day':
			upd2 = "UPDATE login SET leaveCount = leaveCount-0.5 WHERE loginID = (SELECT loginID FROM leaverequest WHERE leaveRequestID = '%s')"%(leaveReqId)
			update(upd2)

		elif leave_type[0]['type'] == 'Full Day': 
			upd2 = "UPDATE login SET leaveCount = leaveCount-1 WHERE loginID = (SELECT loginID FROM leaverequest WHERE leaveRequestID = '%s')"%(leaveReqId)
			update(upd2)

		return redirect(url_for('principal.viewStaffLR'))

	if action == 'reject':
		upd = "UPDATE leaverequest SET status='Rejected' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		return redirect(url_for('principal.viewStaffLR'))

	return render_template('viewStaffLR.html',data=data)

@principal.route('/addNotification_principal',methods=['get','post'])
def addNotification():
	data={}
	sel = "SELECT * FROM department"
	data['dept'] = select(sel)

	if 'addNotification' in request.form:
		deptID = request.form['dept']
		notification = request.form['notification']

		ins = "INSERT INTO notification VALUES (null,'%s','%s',curdate(),curtime(),'principal')"%(deptID,notification)
		insert(ins)
		return redirect(url_for('principal.principalHome'))

	return render_template('addNotification.html',data=data)

@principal.route('/sendMessage_principal',methods=['get','post'])
def sendMessage():
	if 'sendMessage' in request.form:
		message = request.form['message']

		ins = "INSERT INTO message VALUES (null,'%s','%s','pending',curdate())"%(session['loginID'],message)
		insert(ins)
		return redirect(url_for('principal.principalHome'))
	return render_template('sendMessage.html')