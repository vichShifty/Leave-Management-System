from flask import *
from database import *

hod = Blueprint('hod',__name__)

@hod.route('/')
def home():
	return render_template('home.html')

@hod.route('/hodHome')
def hodHome():
	current_page = 'hodHome'
	sel = "SELECT firstName FROM hod WHERE loginID='%s'"%(session['loginID'])
	name = select(sel)

	sel1 = "SELECT receipt FROM leaverequest WHERE loginID='%s' AND status='Accepted' ORDER BY leaveRequestID DESC LIMIT 1" % (session.get('loginID'))
	data = select(sel1)

	if data:
		receipt = data[0]['receipt']
	else:
		receipt = None
	return render_template('hodHome.html',name=name,receipt=receipt,current_page=current_page)

@hod.route('/contact_hod')
def contact():
	user='hod'
	return render_template('contact.html',user=user)

@hod.route('/manageTeachers_hod',methods=['get','post'])
def manageTeachers():
	data={}
	sel1 = "SELECT departmentID FROM hod WHERE loginID='%s'"%(session['loginID'])
	dept = select(sel1)

	sel = "SELECT * FROM teachers WHERE departmentID='%s'"%(dept[0]['departmentID'])
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
		return redirect(url_for('hod.manageTeachers'))

	if 'action' in request.args:
		action = request.args['action']
		teacherId = request.args['teacherId']
	else:
		action = None

	if action == 'delete':
		d = "DELETE FROM teachers WHERE teachersID='%s'"%(teacherId)
		delete(d)
		return redirect(url_for('hod.manageTeachers'))

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
			return redirect(url_for('hod.manageTeachers'))

	return render_template('manageTeachers.html',data=data)

@hod.route('/sendLR_hod',methods=['get','post'])
def sendLR():
	
	data = {}

	sel = "SELECT leaveCount from login WHERE loginID = '%s'"%(session['loginID'])
	data['lc'] = select(sel)

	if 'sendReq' in request.form:
		dateOfLeave = request.form['dateOfLeave']
		leaveType = request.form['leaveType']

		ins = "INSERT INTO leaverequest VALUES(null,'%s','HOD','%s','%s','Pending','unread')"%(session['loginID'],dateOfLeave,leaveType)
		insert(ins)

		return redirect(url_for('hod.hodHome'))

	return render_template('sendLR.html',data=data)

@hod.route('/viewReqStatus_hod')
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

		return redirect(url_for('hod.viewReqStatus'))

	return render_template('viewReqStatus.html',data=data)

@hod.route('/viewTRL_hod')
def viewTRL():
	data={}

	deptid = "SELECT departmentID from hod WHERE loginID = '%s'"%(session['loginID'])
	dId = select(deptid)

	sel = "SELECT * FROM leaverequest r ,teachers t WHERE r.loginID = t.loginID AND requestedBy='Teacher' AND departmentID = '%s' AND status ='Pending' ORDER BY leaveRequestID DESC "%(dId[0]['departmentID'])
	data['TeacherLR'] = select(sel)

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


		return redirect(url_for('hod.viewTRL'))

	if action == 'reject':
		upd = "UPDATE leaverequest SET status='Rejected' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		return redirect(url_for('hod.viewTRL'))
	return render_template('viewTRL.html',data=data)

@hod.route('/viewSRL_hod')
def viewSRL():
	data={}

	deptid = "SELECT departmentID from hod WHERE loginID = '%s'"%(session['loginID'])
	dId = select(deptid)

	sel = "SELECT * FROM leaverequest r ,students s WHERE r.loginID = s.loginID AND requestedBy='Student' AND departmentID = '%s' AND status ='Pending' ORDER BY leaveRequestID DESC "%(dId[0]['departmentID'])
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


		return redirect(url_for('hod.viewSRL'))

	if action == 'reject':
		upd = "UPDATE leaverequest SET status='Rejected' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		return redirect(url_for('hod.viewSRL'))
	return render_template('viewSRL.html',data=data)

@hod.route('/viewNotifications_hod')
def viewNotifications():
	data = {}

	deptid = "SELECT departmentID from hod WHERE loginID = '%s'"%(session['loginID'])
	dId = select(deptid)

	sel = "SELECT * FROM notification WHERE departmentID = '%s'"%(dId[0]['departmentID'])
	data['notification'] = select(sel)

	return render_template('viewNotifications.html',data=data)

@hod.route('/sendComplaint_hod',methods=['get','post'])
def sendComplaint():
	if 'sendComplaint' in request.form:
		complaint = request.form['complaint']

		ins = "INSERT INTO complaint VALUES(null,'%s','HOD','%s','Pending',curdate())"%(session['loginID'],complaint)
		insert(ins)
		return redirect(url_for('hod.hodHome'))
	return render_template('sendComplaint.html')


