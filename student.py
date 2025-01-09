from flask import *
from database import *

student = Blueprint('student',__name__)

@student.route('/')
def home():
	return render_template('home.html')

@student.route('/studentHome')
def studentHome():
	current_page = 'studentHome'
	sel = "SELECT firstName FROM students WHERE loginID='%s'"%(session['loginID'])
	name = select(sel)

	sel1 = "SELECT receipt FROM leaverequest WHERE loginID='%s' AND status='Accepted' ORDER BY leaveRequestID DESC LIMIT 1"%(session['loginID'])
	data= select(sel1)
	if data:
		receipt = data[0]['receipt']
	else:
		receipt = None
	return render_template('studentHome.html',name=name,receipt=receipt,current_page=current_page)

@student.route('/contact_student')
def contact():
	user='student'
	return render_template('contact.html',user=user)

@student.route('/sendLR_student',methods=['get','post'])
def sendLR():

	data = {}

	sel = "SELECT leaveCount from login WHERE loginID = '%s'"%(session['loginID'])
	data['lc'] = select(sel)

	if 'sendReq' in request.form:
		dateOfLeave = request.form['dateOfLeave']
		leaveType = request.form['leaveType']

		ins = "INSERT INTO leaverequest VALUES(null,'%s','Student','%s','%s','Pending','unread')"%(session['loginID'],dateOfLeave,leaveType)
		insert(ins)

		return redirect(url_for('student.studentHome'))
	return render_template('sendLR.html',data=data)

@student.route('/viewReqStatus_student',methods=['get','post'])
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

		return redirect(url_for('student.viewReqStatus'))

	return render_template('viewReqStatus.html',data=data)

@student.route('/sendComplaint_student',methods=['get','post'])
def sendComplaint():
	if 'sendComplaint' in request.form:
		complaint = request.form['complaint']

		ins = "INSERT INTO complaint VALUES(null,'%s','Student','%s','Pending',curdate())"%(session['loginID'],complaint)
		insert(ins)
		return redirect(url_for('student.studentHome'))
	return render_template('sendComplaint.html')

@student.route('/viewNotifications_student',methods=['get','post'])
def viewNotifications():
	data = {}

	deptid = "SELECT departmentID from students WHERE loginID = '%s'"%(session['loginID'])
	dId = select(deptid)

	sel = "SELECT * FROM notification WHERE departmentID = '%s'"%(dId[0]['departmentID'])
	data['notification'] = select(sel)
	return render_template('viewNotifications.html',data=data)

@student.route('/sendQueries_student',methods=['get','post'])
def sendQueries():
	data = {}
	deptid = "SELECT departmentID from students WHERE loginID = '%s'"%(session['loginID'])
	dId = select(deptid)
	sel = "SELECT * FROM teachers WHERE departmentID = '%s'"%(dId[0]['departmentID'])

	data['teachers'] = select(sel)

	sel1 = "SELECT * FROM queries WHERE senderID = '%s'"%(session['loginID'])
	data['query'] = select(sel1)

	if 'sendQuery' in request.form:
		query = request.form['query']
		reciever = request.form['reciever']

		ins = "INSERT INTO queries VALUES (null,'%s','%s','%s','Pending',curdate())"%(session['loginID'],reciever,query)
		insert(ins)
		return redirect(url_for('student.studentHome'))
	return render_template('sendQueries.html',data=data)