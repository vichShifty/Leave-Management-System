from flask import *
from database import *

staff = Blueprint('staff',__name__)

@staff.route('/')
def home():
	return render_template('home.html')

@staff.route('/staffHome')
def staffHome():
	current_page = 'staffHome'
	sel = "SELECT firstName FROM staff WHERE loginID='%s'"%(session['loginID'])
	name = select(sel)

	sel1 = "SELECT receipt FROM leaverequest WHERE loginID='%s' AND status='Accepted' ORDER BY leaveRequestID DESC LIMIT 1"%(session['loginID'])
	data= select(sel1)
	if data:
		receipt = data[0]['receipt']
	else:
		receipt = None

	return render_template('staffHome.html',name=name,receipt=receipt,current_page=current_page)

@staff.route('/contact_staff')
def contact():
	user='staff'
	return render_template('contact.html',user=user)

@staff.route('/sendLR_staff',methods=['get','post'])
def sendLR():

	data = {}

	sel = "SELECT leaveCount from login WHERE loginID = '%s'"%(session['loginID'])
	data['lc'] = select(sel)

	if 'sendReq' in request.form:
		dateOfLeave = request.form['dateOfLeave']
		leaveType = request.form['leaveType']

		ins = "INSERT INTO leaverequest VALUES(null,'%s','Staff','%s','%s','Pending','unread')"%(session['loginID'],dateOfLeave,leaveType)
		insert(ins)

		return redirect(url_for('staff.staffHome'))
	return render_template('sendLR.html',data=data)

@staff.route('/viewReqStatus_staff')
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

		return redirect(url_for('staff.viewReqStatus'))

	return render_template('viewReqStatus.html',data=data)

@staff.route('/sendComplaint_staff',methods=['get','post'])
def sendComplaint():
	if 'sendComplaint' in request.form:
		complaint = request.form['complaint']

		ins = "INSERT INTO complaint VALUES(null,'%s','Staff','%s','Pending',curdate())"%(session['loginID'],complaint)
		insert(ins)
		return redirect(url_for('staff.staffHome'))
	return render_template('sendComplaint.html')