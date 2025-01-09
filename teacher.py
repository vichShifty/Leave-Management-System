from flask import *
from database import *

teacher = Blueprint('teacher',__name__)

@teacher.route('/')
def home():
	return render_template('home.html')

@teacher.route('/teacherHome')
def teacherHome():
	current_page = 'teacherHome'
	sel = "SELECT firstName FROM teachers WHERE loginID='%s'"%(session['loginID'])
	name = select(sel)

	sel1 = "SELECT receipt FROM leaverequest WHERE loginID='%s' AND status='Accepted' ORDER BY leaveRequestID DESC LIMIT 1"%(session['loginID'])
	data= select(sel1)
	if data:
		receipt = data[0]['receipt']
	else:
		receipt = None
	return render_template('teacherHome.html',name=name,receipt=receipt,current_page=current_page)

@teacher.route('/contact_teacher')
def contact():
	user='teacher'
	return render_template('contact.html',user=user)

@teacher.route('/manageStudents_teacher',methods=['get','post'])
def manageStudents():
	data = {}
	sel1 = "SELECT departmentID FROM teachers WHERE loginID='%s'"%(session['loginID'])
	dept = select(sel1)

	sel2 = "SELECT * FROM students WHERE departmentID='%s'"%(dept[0]['departmentID'])
	data['students'] = select(sel2)

	if 'addStudent' in request.form:
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		address = request.form['address']
		phoneNumber = request.form['phoneNumber']
		email = request.form['email']

		uname = request.form['uname']
		pword = request.form['pword']

		ins1 = "INSERT INTO login VALUES(null,'%s','%s','Student',12)"%(uname,pword)
		insert(ins1)

		qry = "SELECT loginID from login WHERE username='%s'"%(uname)
		logID = select(qry)

		ins2 = "INSERT INTO teachers VALUES(null,'%s','%s','%s','%s','%s','%s','%s')"%(logID[0]['loginID'],dept[0]['departmentID'],firstName,lastName,address,phoneNumber,email)
		insert(ins2)
		return redirect(url_for('teacher.manageStudents'))

	if 'action' in request.args:
		action = request.args['action']
		studentId = request.args['studentId']
	else:
		action = None

	if action == 'delete':
		d = "DELETE FROM students WHERE studentID='%s'"%(studentId)
		delete(d)
		return redirect(url_for('teacher.manageStudents'))

	if action == 'update':
		s = "SELECT * FROM students WHERE studentID='%s'"%(studentId)
		data['upd'] = select(s)

		if 'updStudent' in request.form:
			departmentID = request.form['departmentID']
			firstName = request.form['firstName']
			lastName = request.form['lastName']
			address = request.form['address']
			phoneNumber = request.form['phoneNumber']
			email = request.form['email']

			upd = "UPDATE students SET departmentID='%s',firstName='%s',lastName='%s',address='%s',phoneNumber='%s',email='%s' WHERE studentID='%s'"%(dept['departmentID'],firstName,lastName,address,phoneNumber,email,studentId)
			update(upd)
			return redirect(url_for('teacher.manageStudents'))

	return render_template('manageStudents.html',data=data)

@teacher.route('/sendLR_teacher',methods=['get','post'])
def sendLR():

	data = {}

	sel = "SELECT leaveCount from login WHERE loginID = '%s'"%(session['loginID'])
	data['lc'] = select(sel)

	if 'sendReq' in request.form:
		dateOfLeave = request.form['dateOfLeave']
		leaveType = request.form['leaveType']

		ins = "INSERT INTO leaverequest VALUES(null,'%s','Teacher','%s','%s','Pending','unread')"%(session['loginID'],dateOfLeave,leaveType)
		insert(ins)

		return redirect(url_for('teacher.teacherHome'))

	return render_template('sendLR.html',data=data)

@teacher.route('/viewReqStatus_teacher',methods=['get','post'])
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

		return redirect(url_for('teacher.viewReqStatus'))

	return render_template('viewReqStatus.html',data=data)

@teacher.route('/viewSRL_teacher')
def viewSRL():
	data={}

	deptid = "SELECT departmentID from teachers WHERE loginID = '%s'"%(session['loginID'])
	dId = select(deptid)

	sel = "SELECT * FROM leaverequest r ,students s WHERE r.loginID = s.loginID AND requestedBy='Student' AND departmentID = '%s' AND status ='Pending' ORDER BY leaveRequestID DESC"%(dId[0]['departmentID'])
	data['StudentLR'] = select(sel)

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

		return redirect(url_for('teacher.viewSRL'))

	if action == 'reject':
		upd = "UPDATE leaverequest SET status='Rejected' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		return redirect(url_for('teacher.viewSRL'))
	return render_template('viewSRL.html',data=data)

@teacher.route('/sendComplaint_teacher',methods=['get','post'])
def sendComplaint():
	if 'sendComplaint' in request.form:
		complaint = request.form['complaint']

		ins = "INSERT INTO complaint VALUES(null,'%s','Teacher','%s','Pending',curdate())"%(session['loginID'],complaint)
		insert(ins)
		return redirect(url_for('teacher.teacherHome'))
	return render_template('sendComplaint.html')

@teacher.route('/viewNotifications_teacher',methods=['get','post'])
def viewNotifications():
	data = {}

	deptid = "SELECT departmentID from teachers WHERE loginID = '%s'"%(session['loginID'])
	dId = select(deptid)

	sel = "SELECT * FROM notification WHERE departmentID = '%s'"%(dId[0]['departmentID'])
	data['notification'] = select(sel)
	return render_template('viewNotifications.html',data=data)

@teacher.route('/viewQueries_teacher',methods=['get','post'])
def viewQueries():
	data = {}

	sel = "SELECT * FROM queries q,students s WHERE q.senderID = s.loginID AND q.recieverID = '%s'"%(session['loginID'])
	data['queries'] = select(sel)
	
	return render_template('viewQueries.html',data=data)

@teacher.route('/queryReply',methods=['get','post'])
def queryReply():
	if 'submitReply' in request.form:
		reply = request.form['reply']
		queryId = request.args['queryId']

		res = "UPDATE queries SET reply='%s' WHERE queryID='%s'"%(reply,queryId)
		update(res)

		return redirect(url_for('teacher.viewQueries'))

	return render_template('queryReply.html')