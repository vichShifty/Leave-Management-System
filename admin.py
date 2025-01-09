from flask import *
from database import *

admin = Blueprint('admin',__name__)

@admin.route('/')
def home():
	return render_template('home.html')

@admin.route('/adminheader')
def adminheader():
	data = {}
	sel = "SELECT COUNT(*) FROM message where reply='pending'"
	data['messagecount'] = select(sel)
	return render_template('adminheader.html',data=data)

@admin.route('/adminHome')
def adminHome():
	current_page='adminHome'
	data = {}
	sel = "SELECT COUNT(*) FROM message where reply='pending'"
	data['messagecount'] = select(sel)
	return render_template('adminHome.html',data=data,current_page=current_page)

@admin.route('/contact_admin')
def contact():
	user='admin'
	return render_template('contact.html',user=user)

@admin.route('/manageDepartment_admin',methods=['get','post'])
def manageDepartment():
	data={}
	sel = "SELECT * FROM department"
	data['dept'] = select(sel)

	if 'addDepartment' in request.form:
		deptName = request.form['deptName']

		ins = "INSERT INTO department VALUES(null,'%s')"%(deptName)
		insert(ins)
		return redirect(url_for('admin.manageDepartment'))

	if 'action' in request.args:
		action = request.args['action']
		deptId = request.args['deptId']
	else:
		action = None

	if action == 'delete':
		d = "DELETE FROM department WHERE departmentID='%s'"%(deptId)
		delete(d)
		return redirect(url_for('admin.manageDepartment'))

	if action == 'update':
		s = "SELECT * FROM department WHERE departmentID='%s'"%(deptId)
		data['upd'] = select(s)

		if 'updDepartment' in request.form:
			department = request.form['deptName']

			upd = "UPDATE department SET department='%s' WHERE departmentID='%s'"%(department,deptId)
			update(upd)
			return redirect(url_for('admin.manageDepartment'))

	return render_template('manageDepartment.html',data=data)

@admin.route('/manageHOD_admin',methods=['get','post'])
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
		return redirect(url_for('admin.manageHOD'))

	if 'action' in request.args:
		action = request.args['action']
		hodId = request.args['hodId']
	else:
		action = None

	if action == 'delete':
		d = "DELETE FROM hod WHERE hodID='%s'"%(hodId)
		delete(d)
		return redirect(url_for('admin.manageHOD'))

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
			return redirect(url_for('admin.manageHOD'))

	return render_template('manageHOD.html',data=data)

@admin.route('/manageStaff_admin',methods=['get','post'])
def manageStaff():
	data={}
	sel = "SELECT * FROM staff"
	data['staff'] = select(sel)

	if 'addStaff' in request.form:
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		address = request.form['address']
		phoneNumber = request.form['phoneNumber']
		email = request.form['email']

		uname = request.form['uname']
		pword = request.form['pword']

		ins1 = "INSERT INTO login VALUES(null,'%s','%s','Staff',12)"%(uname,pword)
		insert(ins1)

		qry = "SELECT loginID from login WHERE username='%s'"%(uname)
		logID = select(qry)

		ins2 = "INSERT INTO staff VALUES(null,'%s','%s','%s','%s','%s','%s')"%(logID[0]['loginID'],firstName,lastName,address,phoneNumber,email)
		insert(ins2)
		return redirect(url_for('admin.manageStaff'))

	if 'action' in request.args:
		action = request.args['action']
		staffId = request.args['staffId']
	else:
		action = None

	if action == 'delete':
		d = "DELETE FROM staff where staffID='%s'"%(staffId)
		delete(d)
		return redirect(url_for('admin.manageStaff'))

	if action == 'update':
		s = "SELECT * FROM staff WHERE staffID='%s'"%(staffId)
		data['upd'] = select(s)

		if 'updStaff' in request.form:
			firstName = request.form['firstName']
			lastName = request.form['lastName']
			address = request.form['address']
			phoneNumber = request.form['phoneNumber']
			email = request.form['email']

			upd = "UPDATE staff SET firstName='%s',lastName='%s',address='%s',phoneNumber='%s',email='%s' WHERE staffID='%s'"%(firstName,lastName,address,phoneNumber,email,staffId)
			update(upd)
			return redirect(url_for('admin.manageStaff'))

	return render_template('manageStaff.html',data=data)

@admin.route('/viewTeachers_admin')
def viewTeachers():
	data={}
	sel = "SELECT * FROM teachers"
	data['teachers'] = select(sel)

	return render_template('viewTeachers.html',data=data)

@admin.route('/viewStudents_admin')
def viewStudents():
	data={}
	sel = "SELECT * FROM students"
	data['student'] = select(sel)

	return	render_template('viewStudents.html',data=data)

@admin.route('/viewPrincipalLR_admin')
def viewPrincipalLR():
	data={}
	sel = "SELECT * FROM leaverequest r ,principal p WHERE r.loginID = p.loginID AND requestedBy='Principal' AND status='Pending'"
	data['principalLR'] = select(sel)

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


		return redirect(url_for('admin.viewPrincipalLR'))

	if action == 'reject':
		upd = "UPDATE leaverequest SET status='Rejected' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		return redirect(url_for('admin.viewPrincipalLR'))

	return render_template('viewPrincipalLR.html',data=data)

@admin.route('/viewHODLR_admin')
def viewHODLR():
	data={}
	sel = "SELECT * FROM leaverequest r ,hod h WHERE r.loginID = h.loginID AND requestedBy='HOD' AND status ='Pending' ORDER BY leaveRequestID DESC"
	data['HODLR'] = select(sel)

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


		return redirect(url_for('admin.viewHODLR'))

	if action == 'reject':
		upd = "UPDATE leaverequest SET status='Rejected' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		return redirect(url_for('admin.viewHODLR'))

	return render_template('viewHODLR.html',data=data)

@admin.route('/viewStaffLR_admin')
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


		return redirect(url_for('admin.viewStaffLR'))

	if action == 'reject':
		upd = "UPDATE leaverequest SET status='Rejected' WHERE leaveRequestID='%s'"%(leaveReqId)
		update(upd)

		return redirect(url_for('admin.viewStaffLR'))

	return render_template('viewStaffLR.html',data=data)

@admin.route('/addNotification_admin',methods=['get','post'])
def addNotification():
	data={}
	sel = "SELECT * FROM department"
	data['dept'] = select(sel)

	if 'addNotification' in request.form:
		deptID = request.form['dept']
		notification = request.form['notification']

		ins = "INSERT INTO notification VALUES (null,'%s','%s',curdate(),curtime(),'admin')"%(deptID,notification)
		insert(ins)
		return redirect(url_for('admin.adminHome'))

	return render_template('addNotification.html',data=data)

@admin.route('/viewMessage_admin')
def viewMessage():
	data = {}
	sel = "SELECT * FROM message m , principal p WHERE m.senderID = p.loginID"
	data['message'] = select(sel)

	return render_template('viewMessage.html',data=data)

@admin.route('/messageResponse',methods=['get','post'])
def messageResponse():
	if 'submitResponse' in request.form:
		response = request.form['response']
		messageId = request.args['messageId']

		res = "UPDATE message SET reply='%s' WHERE messageID='%s'"%(response,messageId)
		update(res)

		return redirect(url_for('admin.viewMessage'))

	return render_template('messageResponse.html')

@admin.route('/viewComplaint_admin')
def viewComplaint():
	data = {}
	sel = "SELECT * FROM COMPLAINT c, Login l WHERE c.loginID = l.loginID"
	data['complaint'] = select(sel)

	return render_template('viewComplaint.html',data=data)

@admin.route('/complaintResponse',methods=['get','post'])
def complaintResponse():
	if 'submitResponse' in request.form:
		response = request.form['response']
		complaintId = request.args['complaintId']

		res = "UPDATE complaint SET reply='%s' WHERE complaintID='%s'"%(response,complaintId)
		update(res)

		return redirect(url_for('admin.viewComplaint'))

	return render_template('complaintResponse.html')