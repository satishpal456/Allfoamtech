from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
import pyrebase
import os.path
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials , firestore
import random , string
import qrcode
import datetime

tmpFilePath = os.path.abspath(os.path.join('firebase/serviceAccountKey.json', os.pardir)) + '\serviceAccountKey.json'
if (not len(firebase_admin._apps)):
	cred = credentials.Certificate(tmpFilePath)
	firebase_admin.initialize_app(cred)
firebase_admin.get_app()

db = firestore.client()

config = {
    "apiKey": "AIzaSyCC6uEdeE_3L6KKgBePW8n77sPNir5c4Bw",
    "authDomain": "sprayer-loyalty-a3d4a.firebaseapp.com",
    "databaseURL": "https://sprayer-loyalty-a3d4a.firebaseio.com",
    "projectId": "sprayer-loyalty-a3d4a",
    "storageBucket": "sprayer-loyalty-a3d4a.appspot.com",
    "messagingSenderId": "624993131038",
    "appId": "1:624993131038:web:5e7292485eb5d29b"
  };

dburl = "https://sprayer-loyalty-a3d4a.firebaseio.com"
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()

def signin_error(request,e):
	pass

def login_page(request):
	print('login_page')
	try:
		print('ttttttrrrrrrryyyyyyyyy')
		idtoken = request.session['uid']
		a = authe.get_account_info(idtoken)
		b = a['users']
		c = b[0]
		d = c['localId']

		user_ref = db.collection('users').document(d)
		data = user_ref.get()
		datas = data.to_dict()

		if d:
			return redirect('dashboard')
	except Exception as ex:
		print(ex)
		return redirect('log_in')


def merchant_login_page(request):
	print('merchant_login_page')
	try:
		print('ttttttrrrrrrryyyyyyyyy')
		idtoken = request.session['uid']
		a = authe.get_account_info(idtoken)
		b = a['users']
		c = b[0]
		d = c['localId']

		user_ref = db.collection('users').document(d)
		data = user_ref.get()
		datas = data.to_dict()

		if d:
			return redirect('product_list')
	except Exception as ex:
		print(ex)
		return render(request, "login-page.html")	

def dashboard(request):
	is_admin = False
	is_merchant = False
	try:

		idtoken = request.session['uid']
		a = authe.get_account_info(idtoken)
		b = a['users']
		c = b[0]
		d = c['localId']
		if d == 'oTEyh3p8BshhB6k25FzAQGCKl2D2': 
			is_admin = True
		else:
			is_merchant = True
		return render(request, "Dashboard.html",{"is_admin":is_admin,'is_merchant':is_merchant})
	except Exception as ex:
		print(ex)
		return render(request, "login-page.html")	


def log_in(request):
	print("login")
	login_error = False
	is_merchant = False
	is_admin = True
	base = 'base.html'

	email = request.POST.get('email')
	password = request.POST.get('password')
	try:
		user = authe.sign_in_with_email_and_password(email,password)
		
		if user:
			merchant_ref = db.collection('merchant').get()
			for m_ref in merchant_ref:
				m_ref_doc = m_ref.to_dict()
				for m_ref1 in m_ref_doc:
					if m_ref1 == 'Email':
						if email == m_ref_doc[m_ref1]:
							print('merchant---------')
							is_merchant = True
							base = 'base_merchant.html'
							is_admin = False
						
			session_id = user['idToken']
			request.session['uid'] = str(session_id)
			request.session['email'] = email
			uid = request.session['uid']

			return render(request, "Dashboard.html",{'e':email,'base':base,'is_admin':is_admin,'is_merchant':is_merchant})
	except Exception as ex:
		print(ex)
		login_error = True
		return render(request, "login-page.html",{'login_error':login_error})	

def logout(request):
	print('logout')
	try:
		del request.session['uid']
	except:
		pass
	return render(request, "login-page.html")	


def user_list(request):
	document_id = []
	is_admin = True
	is_merchant = False
	documents = list(db.collection('users').get())
	for doc in documents:
		document_id.append(doc.id)
	name = []
	email = []
	companyName = []
	number = []
	points = []
	users_ref = db.collection(u'users')
	print('----------------userssss---------',users_ref)
	data = users_ref.get()
	print('----------------userssss---------',data)

	for el in data:
		dic = el.to_dict()
		for d in dic:
			if d == "name":
				name.append(dic[d])
			elif d == "email":
				email.append(dic[d])	
			elif d == "companyName":
				companyName.append(dic[d])
			elif d == "number":
				number.append(dic[d])
			elif d == "points":
				points.append(dic[d])
		comb_list = sorted(zip(name,email,companyName,number,points,document_id))
	print('cccccccc',comb_list)
	return render(request , "user-list.html" , {'comb_list':comb_list,'is_admin':is_admin,'is_merchant':is_merchant})
	
def view_list(request,id):
	d_id = id
	is_admin = True
	is_merchant = False
	companyName = []
	referralFrnd = []
	number = []
	city = []
	name = []
	zip_code = []
	points = []
	state = []
	address = []
	referralUser = []
	email = []
	status = []
	users_ref = db.collection('users').document(d_id)
	print('----->>>>>>>>>+++++++++++',users_ref)
	data = users_ref.get()
	print('-----data-------',data.to_dict())
	dic = data.to_dict()
	for d in dic:
		print('-----k-----',d,'------v------',dic[d])
		if d == "companyName":
			companyName = dic[d]
		elif d == "referralFrnd":
			referralFrnd = dic[d]
		elif d == "number":
			number = dic[d]
		elif d == "city":
			city = dic[d]
		elif d == "name":
			name = dic[d]
		elif d == "zip":
			zip_code = dic[d]
		elif d == "points":
			points = dic[d]
		elif d == "state":
			state = dic[d]
		elif d == "address":
			address = dic[d]
		elif d == "referralUser":
			referralUser = dic[d]
		elif d == "email":
			print('----------999999999',dic['email'])
			email = dic[d]	
		elif d == 'status':
			status = dic[d]
	print('zzzzzzzzzz',zip_code)
	context = {
		'referralUser' : referralUser,
		'address' : address,
		'state': state,
		'points': points,
		'zip_code':zip_code,
		'name':name,
		'number':number,
		'referralFrnd':referralFrnd,
		'companyName':companyName,
		'email' : email,
		'city':city,
		'd_id': d_id,
		'status':status,
		'is_admin':is_admin,
		'is_merchant':is_merchant
	}
	return render(request , 'view_list.html',context)



def qr_code(request):
	try:
		return render(request,'qr.html')
	except KeyError:
		msg = 'Ooops! user log out please signIn  again'
		return redirect('signin_error',e=msg)			

def post_generate_qr(request):
	print('--ajax--call--post_generate_qr-->>>>')
	product_name = request.GET.get('product_name')
	print('----ppppppp------->>>>',product_name)
	points = request.GET.get('points')
	print('----points------->>>>',points)

	manufacturer = request.GET.get('manufacturer')
	print('----manufacturer------->>>>',manufacturer)

	guidelines = request.GET.get('guidelines')
	print('----guidelines------->>>>',guidelines)

	img_url = request.GET.get('img_url')
	print('----img_url------->>>>',img_url)

	try:
		abc =''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
		barrels = {
			'manufacturer':manufacturer,
			'product_name':product_name,
			'points':points,
		}
		barrel_insulation_data = {
			'url':img_url,
			'points':points,
			'Title':manufacturer,
			'guidelines':guidelines,
		}
		barrel_insulation_data_ref = db.collection('barrel_insulation_data').document(abc)
		barrel_insulation_data_ref.set(barrel_insulation_data)
		barrels_ref = db.collection('barrels').document(abc)
		barrels_ref.set(barrels)
		return redirect('qr_code_list')
	except:
		login_error = True
		return render(request, "login-page.html",{'login_error':login_error})	

def qr_code_list(request):
	is_admin = False
	is_merchant = False
	print('qr_code_list')
	points = []
	manufacturer=[]
	product_name=[]
	gallery = []
	guidelines = []
	qr_img_list = []
	try:
		print('trytry---------')
		idtoken = request.session['uid']
		a = authe.get_account_info(idtoken)
		b = a['users']
		c = b[0]
		d = c['localId']
		if d == 'oTEyh3p8BshhB6k25FzAQGCKl2D2': 
			is_admin = True
		else:
			is_merchant = True
		abc =''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
		barrels_ref = db.collection('barrels')
		barrel_insulation_data_ref = db.collection('barrel_insulation_data')
		data = barrels_ref.get()
		data1 = barrel_insulation_data_ref.get()
		
		barrels_ref = db.collection('product')
		data3 = barrels_ref.get()
		for d3 in data3:
			dic3 = d3.to_dict()
			print('----dic3------',dic3)
			for di3 in dic3:
				if di3 == "url":
					gallery.append(dic3[di3])
				elif di3 == "name":
					product_name.append(dic3[di3])
				elif di3 == "initial_point":
					points.append(dic3[di3])
				
		comb_list_1 = zip(product_name,points,gallery)

		
		return render(request, 'qr_code_list.html', {'data':comb_list_1,"is_admin":is_admin,"is_merchant":is_merchant})
	except KeyError:
		msg = 'Ooops! user log out please signIn  again'
		return redirect('signin_error',e=msg)

def ublock(request,d_id):
	dd_id = d_id
	db.collection('users').document(dd_id).update({'status' : 'false'})
	return redirect('view_list',id=dd_id)

def u_unblock(request,d_id):
	dd_id = d_id
	db.collection('users').document(dd_id).update({'status' : 'true'})
	return redirect('view_list',id=dd_id)



def video_details_home(request):
	is_admin = True
	is_merchant = False
	video_id = []
	v_url = []
	video_data = list(db.collection('Youtube_data').get())
	for data in video_data:
		video_id.append(data.id)
	thumbnails = []
	title = []

	video_ref = db.collection('Youtube_data')
	video_data = video_ref.get()
		video = vd.to_dict()
		for vid in video:
			if vid == "thumbnails":
				thumbnails.append(video[vid])

			elif vid == "title":
				title.append(video[vid])
	for thumbnails_key in thumbnails:
		print("default=============thumbnails_key===========>>>>",thumbnails_key)
		for da in thumbnails_key:
			print('-----k-----',da,'------v------',thumbnails_key[da])
			if da == "default":
				print('------ddddddddddd---',thumbnails_key[da])
				# print(default[da]['url'])
				v_url.append(thumbnails_key[da]['url'])
			

		comb_list = zip(v_url,title,video_id)
		print('-----------v_url-------',v_url,'\n--------title------',title,'\n--------video_id',video_id)
		print("comb_list===>",comb_list)
						

	return render(request,"video_details.html",{"comb_list":comb_list,"is_admin":is_admin,"is_merchant":is_merchant})

def quiz_list(request,id):
	iid = id
	is_admin = True
	is_merchant = False
	context = {'iid': iid,'admin':is_admin,'merchant':is_merchant}
	return render(request,"quiz_list.html",context)
		
def add_ques(request):
	# print('add_ques')
	if request.method == 'POST':
		print('POST')
		d_id = request.POST.get('id')
		print('d_id',d_id)
		points = request.POST.get('points')
		print('points',points)
		question1 = request.POST.get('question_1')

		option1 = request.POST.get('q_1_a')
		option2 = request.POST.get('q_1_b')
		option3 = request.POST.get('q_1_c')
		option4 = request.POST.get('q_1_d')
		answer1 = request.POST.get('q_1_ans')

		question2 = request.POST.get('question_2')
		option11 = request.POST.get('q_2_a')
		option22 = request.POST.get('q_2_b')
		option33 = request.POST.get('q_2_c')
		option44 = request.POST.get('q_2_d')
		answer11 = request.POST.get('q_2_ans')

		try:
			quiz_data = {
				'points' : points,
				'question1' : question1,
				'option1' : option1,
				'option2' : option2,
				'option3' : option3,
				'option4' : option4,
				'answer1' : answer1,
				'question2' : question2,
				'option11' : option11,
				'option22' : option22,
				'option33' : option33,
				'option44' : option44,
				'answer11' : answer11,

			}

			quiz_data_ref = db.collection('Quiz_db').document(d_id).set(quiz_data)
			return render(request, 'quiz_list.html')

		except Exception as ex:	
			print(ex)
			return HttpResponse('qqqqqqqq')

def merchant_list(request):
	merchant_id = []
	is_admin = True
	is_merchant = False
	print('ertyuiop',merchant_id)
	merchants = list(db.collection('merchant').get())
	for datas in merchants:
		merchant_id.append(datas.id)
	name = []
	Email = []
	Phone = []
	Address = []
	merchant_ref = db.collection('merchant')
	data = merchant_ref.get()
	for el in data:
		m_dic = el.to_dict()
		for data in m_dic:
			if data == "name":
				name.append(m_dic[data])
			elif data == "Email":
				Email.append(m_dic[data])	
			elif data == "Phone":
				Phone.append(m_dic[data])
			elif data == "Address":
				Address.append(m_dic[data])

	comb_list = zip(name,Email,Phone,Address,merchant_id)
	print('cccccccc',comb_list)
	return render(request , "merchant_list.html" , {'comb_list':comb_list,'is_admin':is_admin,'is_merchant':is_merchant})

def merchant_details(request,id):
	m_id = id
	is_admin = True
	is_merchant = False
	name = []
	Email = []
	Phone = []
	Address = []
	status = []

	
	points = []
	merchant_ref = db.collection('merchant').document(m_id)
	details = merchant_ref.get()
	dic = details.to_dict()
	for d in dic:
		print('-----k-----',d,'------v------',dic[d])
		if d == "status":
			print(dic['status'])
			status = dic[d]
		elif d == "name":
			print(dic['name'])
			name = dic[d]
		elif d == "Email":
			print(dic['name'])
			Email = dic[d]
		elif d == "Phone":
			print(dic['name'])
			Phone = dic[d]
		elif d == "Address":
			print(dic[d])
			Address = dic[d]

	barrels_ref = db.collection('product')
	data3 = barrels_ref.get()
	for d3 in data3:
		print('d3_id----',d3.id)
		if d3.id == 'biXyu0pQxRRbIGMzbKGa':
			p_id = []
			gallery = []
			product_name_new = []
			print('----match')
			dic3 = d3.to_dict()
			for di3 in dic3:
				p_id.append(di3)
				for di3_data in dic3[di3]:
					if di3_data == "url":
						gallery.append(dic3[di3][di3_data])
					elif di3_data == "name":
						product_name_new.append(dic3[di3][di3_data])
					elif di3_data == "initial_point":
						points.append(dic3[di3][di3_data])
		
			print('---p_id---',p_id)
			print('---product_name_new---',product_name_new)
			print('---gallery---',gallery)
	comb_list = zip(p_id,product_name_new,gallery)

	context = {
		'name' : name,
		'Email' : Email,
		'Phone': Phone,
		'Address': Address,
		'm_id':m_id,
		'is_admin' : is_admin,
		'is_merchant' : is_merchant,
		'status' : status,
		'comb_list':comb_list,
	}			


	return render(request,'merchant_details.html',context)	

def mblock(request,m_id):
	mm_id = m_id
	# print("ddddddddd",dd_id)
	db.collection('merchant').document(mm_id).update({'status' : 'False'})
	return redirect('merchant_details',id=mm_id)

def m_unblock(request,m_id):
	mm_id = m_id
	# print("ddddddddd",dd_id)
	db.collection('merchant').document(mm_id).update({'status' : 'True'})
	return redirect('merchant_details',id=mm_id)	

def add_merchant(request):
	
	is_admin = True
	is_merchant = False
	try:
		if request.method == 'POST':
			name = request.POST.get('name')
			print("--------name      ",name)
			Email = request.POST.get('Email')
			Phone = request.POST.get('Phone')
			Address = request.POST.get('Address')
			password = request.POST.get('password')
			status = request.POST.get('status')
			print('--------status',status)
			m_id =''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
			merchant_data = {
				'name' : name,
				'Email' : Email,
				'Phone' : Phone,
				'Address' : Address,
				'password' : password,
				'status' : status,
			}
			authe.create_user_with_email_and_password(Email,password)
			merchant_data_ref = db.collection('merchant').document(m_id).set(merchant_data)
			return redirect('merchant_list')

		return render(request,'add_merchant.html',{'is_admin':is_admin,'is_merchant':is_merchant})	
	except Exception as ex:
		print(ex)
		return HttpResponse('wwwwwwww')

def product_list(request):
	print('product_list')
	is_admin = False
	is_merchant = False
	try:
		print('trytry---------')
		idtoken = request.session['uid']
		a = authe.get_account_info(idtoken)
		b = a['users']
		c = b[0]
		# print('cccc',c)
		d = c['email']
		if d == 'fSL9ceMhSQXZI9SeDF6udab28233': 
			is_admin = True
		else:
			is_merchant = True
		document_id = []
		documents = list(db.collection('barrel_insulation_data').get())
		for doc in documents:
			document_id.append(doc.id)
		manufacture_name = []
		product_name = []
		points = []
		gallery = []
		quantity = []
		product_name_new = []
		p_id = []
		barrel_insulation_data_ref = db.collection('barrel_insulation_data')
		data = barrel_insulation_data_ref.get()
		
		barrels_ref = db.collection('product')
		data3 = barrels_ref.get()
		for d3 in data3:
			m_id = d3.id
			print('m_id----',m_id)

			if m_id == 'biXyu0pQxRRbIGMzbKGa':
				print('----match')
				dic3 = d3.to_dict()
				# print('dic3----',dic3)
				for di3 in dic3:
					# print('di3----',dic3[di3])
					p_id.append(di3)
					for di3_data in dic3[di3]:
						# print('=====',dic3[di3][di3_data])
						if di3_data == "url":
							# print('urlurl----',dic3[di3][di3_data])
							gallery.append(dic3[di3][di3_data])
						elif di3_data == "name":
							product_name_new.append(dic3[di3][di3_data])
						elif di3_data == "initial_point":
							points.append(dic3[di3][di3_data])


		print('---p_id---',p_id)
		print('---product_name_new---',product_name_new)
		print('---gallery---',gallery)

		comb_list = zip(p_id,product_name_new,gallery,document_id)
		# print('cccccccc',comb_list)
		return render(request=request,template_name='product_list.html',context={'comb_list':comb_list,'is_admin':is_admin,'is_merchant':is_merchant})
	except Exception as ex:
		print('except', ex)
		return redirect('login_page')
def add_product(request):
	is_admin = False
	is_merchant = False
	print('add_product')
	try:
		print('trytry---------')
		idtoken = request.session['uid']
		a = authe.get_account_info(idtoken)
		b = a['users']
		c = b[0]
		# print('cccc',c)
		d = c['email']
		# print('--------dddd----',d)
		if d == 'fSL9ceMhSQXZI9SeDF6udab28233': 
			is_admin = True
		else:
			is_merchant = True
		return render(request,'add_product.html',{'is_admin':is_admin,'is_merchant':is_merchant})
	except Exception as ex:
		print('except', ex)
		# msg = 'Ooops! user log out please signIn  again'
		return redirect('login_page')	

def post_product(request):
	qr_img_list = []

	print('--ajax--call--post_product-->>>>')
	product_name = request.GET.get('product_name')
	print('----ppppppp------->>>>',product_name)
	points = request.GET.get('points')
	print('----points------->>>>',points)
	manufacturer = request.GET.get('manufacturer')
	print('----manufacturer------->>>>',manufacturer)
	quantity = request.GET.get('quantity')

	print('----quantity------->>>>',quantity, '\nTYpe of quantity', type(quantity))

	img_url = request.GET.get('img_url')
	print('----img_url123------->>>>',img_url)

	try:
		print('trytry---------')
		abc =''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
		print('abc---',abc)
		barrels = {
			'name':product_name,
			# 'manufacturer':manufacturer,
			'initial_point':points,
			'url':img_url,
			'quantity':quantity,
		}
		print('barrels------->',barrels)
		product_ref = db.collection('product').document(abc)
		product_ref.set(barrels)

		product_ref = db.collection('product').get()
		for p in product_ref:
			print('---p--->>',p.id)

			p_dic = p.to_dict()
			print('====================+++++ppp',p_dic)
			for p1 in p_dic:
				print('p1p1p1p1==============',p_dic[p1])
				for p2 in p_dic[p1]:
					if p2 == 'name':
						pn = p_dic[p1][p2]
						print('pnpnpnpn',pn)
					if p2 == 'initial_point':
						ip = p_dic[p1][p2]
						print('initial point----',ip)
				
						i = 0
						qu1 = int(quantity)
						print('=====qu1===',qu1)
						for q1 in range(1,qu1+1):
							print(i)
							i = i + 1
							qr = qrcode.QRCode(
							    version = 1,
							    error_correction = qrcode.constants.ERROR_CORRECT_H,
							    box_size = 10,
							    border = 4,
							)
							print('---qr-1--',qr)
							qr_data = "MERCHANT ID : " + "biXyu0pQxRRbIGMzbKGa" + "\nPRODUCT ID : " + p1 + "\nYOU GOT "+ str(ip) +" REWARD POINTS"
									# print('----qr_data----',qr_data, '\nquality : ',quantity, '\n type of quantity', type(quantity))
								
							qr.add_data(qr_data)
							print('---qr-2--',qr)

							qr.make(fit=True)
							print('---qr-3--',qr)

							img = qr.make_image()
							print('---qr-4--',img)
							img.save("./fire/static/img/qr_images/"+pn+"_"+p1+"_"+str(i)+".png")
							print('---qr-5--',img)

							img_name = "qr_"+str(abc)+"_"+str(i)+".png"
							print('---qr-6--',img_name)

							qr_img_list.append(img_name)
							print('qr_img_list-7---',qr_img_list)
		return render(request,'products.html')

		# return redirect('product_list')
	except Exception as ex:
		print('except=====', ex)
		# login_error = True
		# return render(request, "login-page.html",{'login_error':login_error})	
		return redirect('merchant_login_page')					

def batch(request):
	print('batch_list')
	is_admin = False
	is_merchant = False
	try:
		print('trytry---------')
		idtoken = request.session['uid']
		a = authe.get_account_info(idtoken)
		b = a['users']
		c = b[0]
		# print('cccc',c)
		d = c['email']
		# print('--------dddd----',d)
		if d == 'fSL9ceMhSQXZI9SeDF6udab28233': 
			is_admin = True
		else:
			is_merchant = True

		batch_id = []
		p_id = []
		quantity = []

		batch_ref = db.collection('batch')
		batches = batch_ref.get()
		for batch in batches:
			print('batch----',batch.id)
			if batch.id == 'biXyu0pQxRRbIGMzbKGa':
				print('----match')
				dic3 = batch.to_dict()
				# print('dic3----',dic3)
				for di3 in dic3:
					# print('di3---->>>>>>>',dic3[di3])
					batch_id.append(di3)
					for di4 in dic3[di3]:
						p_id.append(di4)
					for di3_data in dic3[di3]:
						# print('=====',dic3[di3][di3_data])
						# print('--di3_data--',di3_data)
						# print('urlurl----',dic3[di3][di3_data])
						for q in dic3[di3][di3_data]:
							# print('qqqqq',q)
							if q == "quantity":
								# print('quantity----',dic3[di3][di3_data][q])
								quantity.append(dic3[di3][di3_data][q])
						
		# print('p_id---',p_id)
		# print('quantity---',quantity)
		# print('batch_id---',batch_id)

		comb_list = zip(batch_id,p_id,quantity)

		return render(request, 'batch_list.html',{'is_merchant':is_merchant,'is_admin':is_admin,'comb_list':comb_list})
	except Exception as ex:
		print(ex)
		return redirect('login_page')

def batch_view(request,b_id):
	b_id = b_id
	# print(b_id)
	print('batch_view')
	is_admin = False
	is_merchant = False
	p_id = []
	quantity = []
	try:
		print('trytry---------')
		idtoken = request.session['uid']
		a = authe.get_account_info(idtoken)
		b = a['users']
		c = b[0]
		# print('cccc',c)
		d = c['email']
		# print('--------dddd----',d)
		if d == 'fSL9ceMhSQXZI9SeDF6udab28233': 
			is_admin = True
		else:
			is_merchant = True

		p_id = []
		quantity = []

		batch_ref = db.collection('batch')
		batches = batch_ref.get()
		for batch in batches:
			print('batch----',batch.id)
			if batch.id == 'biXyu0pQxRRbIGMzbKGa':
				print('----match')
				dic3 = batch.to_dict()
				# print('dic3----',dic3)
				for di3 in dic3:
					# print('di3---->>>>>>>',di3)
					# batch_id.append(di3)
					if di3 == b_id: 
						print('match')
						for di4 in dic3[di3]:
							p_id.append(di4)
						for di3_data in dic3[di3]:
							# print('=====',dic3[di3][di3_data])
							# print('--di3_data--',di3_data)
							# print('urlurl----',dic3[di3][di3_data])
							for q in dic3[di3][di3_data]:
								# print('qqqqq',q)
								if q == "quantity":
									# print('quantity----',dic3[di3][di3_data][q])
									quantity.append(dic3[di3][di3_data][q])
		print('p_id---',p_id)
		print('quantity---',quantity)

		comb_list_1 = zip(p_id,quantity)
		return render(request, 'batch_view.html',{'is_merchant':is_merchant,'is_admin':is_admin,'comb_list_1':comb_list_1})
	except Exception as ex:
		print(ex)
		return redirect('login_page')		