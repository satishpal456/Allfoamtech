from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
import pyrebase
import os.path
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials , firestore
import random , string
import qrcode

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
# firebase.initializeApp(Config);
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
# database = firebase.database()  

# Create your views here.
def signin_error(request,e):
	pass
	# print('signin_error')
	# error = e
	# return render(request, "login-page.html",{'error':error})	

def login_page(request):
	print('login_page')
	is_merchant = False
	is_admin = True
	base = 'base.html'
	try:
		# session_error=False
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
			return render(request, "Dashboard.html",{'e':email,'base':base,'admin':is_admin,'merchant':is_merchant})

			# return redirect('dashboard')
	except:
		print('except')
		# session_error = True
		return render(request, "login-page.html")	


def dashboard(request):
	return render(request, "Dashboard.html")

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
			uid = request.session['uid']
			print('uiduiduiduid',uid)			

			return render(request, "Dashboard.html",{'e':email,'base':base,'admin':is_admin,'merchant':is_merchant})
	except Exception as ex:
		print(ex)
		login_error = True
		return render(request, "login-page.html",{'login_error':login_error})	

		# return redirect('signin_error',e=msg)

		# return render(request,"login-page.html",{"msg":message})

def logout(request):
	print('logout')
	# auth.logout(request)
	try:
		del request.session['uid']
	except:
		pass
	return render(request, "login-page.html")	

	# return redirect('login_page')	

def user_list(request):
	document_id = []
	documents = list(db.collection('users').get())
	for doc in documents:
		document_id.append(doc.id)
	name = []
	email = []
	companyName = []
	number = []
	points = []
	users_ref = db.collection('users').order_by("points")
	data = users_ref.get()
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
		comb_list = zip(name,email,companyName,number,points,document_id)
		print('cccccccc',comb_list)
	return render(request , "user-list.html" , {'comb_list':comb_list})
	
def view_list(request,id):
	d_id = id
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
			# print(dic['name'])
			companyName = dic[d]
		elif d == "referralFrnd":
			# print(dic['name'])
			referralFrnd = dic[d]
		elif d == "number":
			# print(dic['name'])
			number = dic[d]
		elif d == "city":
			print(dic[d])
			city = dic[d]
		elif d == "name":
			# print(dic['name'])
			name = dic[d]
		elif d == "zip":
			# print(dic['name'])
			zip_code = dic[d]
		elif d == "points":
			# print(dic['name'])
			points = dic[d]
		elif d == "state":
			# print(dic['name'])
			state = dic[d]
		elif d == "address":
			# print(dic['name'])
			address = dic[d]
		elif d == "referralUser":
			# print(dic['name'])
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
	print('qr_code_list')
	points = []
	manufacturer=[]
	product_name=[]
	gallery = []
	guidelines = []
	qr_img_list = []
	try:
		abc =''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
		barrels_ref = db.collection('barrels')
		barrel_insulation_data_ref = db.collection('barrel_insulation_data')
		data = barrels_ref.get()
		data1 = barrel_insulation_data_ref.get()
		for el in data:
			dic = el.to_dict()
			for d in dic:
				if d == 'points':
					points.append(dic[d])
				elif d == 'manufacturer':
					manufacturer.append(dic[d])
				elif d == 'product_name':
					product_name.append(dic[d])
		for i in data1:
			dic1 = i.to_dict()
			for d1 in dic1:
				if d1 == 'url':
					gallery.append(dic1[d1])
				elif d1 == 'guidelines':
					guidelines.append(dic1[d1])
		
		comb_list_1 = zip(manufacturer,product_name,points)

		i = 0
		for m,p_name,p in comb_list_1:
			i = i + 1
			p = str(p)
			print('---m---',m,'----p_name---',p_name,'----points---',p)
			data = "ID : " + str(i) +"\nManufactur Name : " + m + "\nProduct Name : " + p_name + "\nPoints : " + p 
			qr = qrcode.QRCode(
			    version = 1,
			    error_correction = qrcode.constants.ERROR_CORRECT_H,
			    box_size = 10,
			    border = 4,
			)
			qr.add_data(data)
			qr.make(fit=True)
			img = qr.make_image()
			img.save("./fire/static/img/qr_images/qr"+str(i)+".png")
			img_name = "qr"+str(i)+".png"
			qr_img_list.append(img_name)

		comb_list = zip(manufacturer,product_name,points,gallery,qr_img_list,guidelines)
		return render(request, 'qr_code_list.html', {'data':comb_list})
	except KeyError:
		msg = 'Ooops! user log out please signIn  again'
		return redirect('signin_error',e=msg)

def ublock(request,d_id):
	dd_id = d_id
	# print("ddddddddd",dd_id)
	db.collection('users').document(dd_id).update({'status' : 'false'})
	return redirect('view_list',id=dd_id)

def u_unblock(request,d_id):
	dd_id = d_id
	# print("ddddddddd",dd_id)
	db.collection('users').document(dd_id).update({'status' : 'true'})
	return redirect('view_list',id=dd_id)



def video_details_home(request):
	video_id = []
	v_url = []
	video_data = list(db.collection('Youtube_data').get())
	for data in video_data:
		video_id.append(data.id)
	thumbnails = []
	title = []
	# points = []
	# action = []
	video_ref = db.collection('Youtube_data')
	# print("video_ref===>",video_ref)
	video_data = video_ref.get()
	# print("video_data===>",video_data)
	for vd in video_data:
		video = vd.to_dict()
		# print("video===>",video)
		for vid in video:
			if vid == "thumbnails":
				# print("thumbnails===>",thumbnails)
				thumbnails.append(video[vid])
							# print('---------url========',v_url)
							# v_url.append(video[vid])
							# default[da]['url'].append(video[vid])
			elif vid == "title":
				# print("title===>",title)
				title.append(video[vid])
	for thumbnails_key in thumbnails:
					# print('-----k-----',da,'------v------',thumbnails_key[da])
		print("default=============thumbnails_key===========>>>>",thumbnails_key)
		for da in thumbnails_key:
			print('-----k-----',da,'------v------',thumbnails_key[da])
			if da == "default":
				print('------ddddddddddd---',thumbnails_key[da])
				# print(default[da]['url'])
				v_url.append(thumbnails_key[da]['url'])
			
			# if vid == "points":
			# 	print("vid===>",vid)
			# 	points.append(video[vid])
				
			# if vid == "action":
			# 	print("vid===>",vid)
			# 	action.append(video[vid])	

		comb_list = zip(v_url,title,video_id)
		print('-----------v_url-------',v_url,'\n--------title------',title,'\n--------video_id',video_id)
		print("comb_list===>",comb_list)
						
	# pass
	# data_ref = db.collection(u"Youtube_data").document()
	# video_data = data_ref.get()
	# videoss = video_data.to_dict()
	# print("dataa===>",video_data)
	# print("dataassss===>",videoss)

	return render(request,"video_details.html",{"comb_list":comb_list})

def quiz_list(request,id):
	iid = id
	context = {'iid': iid,}
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

		# print('question1',question1)
		option1 = request.POST.get('q_1_a')

		# print('option1',option1)
		option2 = request.POST.get('q_1_b')

		# print('option2',option2)
		option3 = request.POST.get('q_1_c')

		# print('option3',option3)
		option4 = request.POST.get('q_1_d')

		# print('option4',option4)
		answer1 = request.POST.get('q_1_ans')

		question2 = request.POST.get('question_2')
		option11 = request.POST.get('q_2_a')
		option22 = request.POST.get('q_2_b')
		option33 = request.POST.get('q_2_c')
		option44 = request.POST.get('q_2_d')
		answer11 = request.POST.get('q_2_ans')

		# print('answer',answer)

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
			# print('cfgvhbjnkml,;',quiz_data_ref)
			return render(request, 'quiz_list.html')

		except Exception as ex:	
			print(ex)
			return HttpResponse('qqqqqqqq')

# def merchant_list(request):

# 	return render(request,'merchant_list.html')	
def merchant_list(request):
	merchant_id = []
	print('ertyuiop',merchant_id)
	merchants = list(db.collection('merchant').get())
	for datas in merchants:
		merchant_id.append(datas.id)
	name = []
	Email = []
	Phone = []
	Address = []
	# password = []
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
			# elif data == "password":
			# 	password.append(m_dic[data])

	comb_list = zip(name,Email,Phone,Address,merchant_id)
	print('cccccccc',comb_list)
	return render(request , "merchant_list.html" , {'comb_list':comb_list})

def add_merchant(request):
	

		try:
			if request.method == 'POST':
				name = request.POST.get('name')
				print("--------name      ",name)
				Email = request.POST.get('Email')
				Phone = request.POST.get('Phone')
				Address = request.POST.get('Address')
				password = request.POST.get('password')
				m_id =''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
				merchant_data = {
					'name' : name,
					'Email' : Email,
					'Phone' : Phone,
					'Address' : Address,
					'password' : password,
				}
				authe.create_user_with_email_and_password(Email,password)
				merchant_data_ref = db.collection('merchant').document(m_id).set(merchant_data)
				return redirect('merchant_list')

			return render(request,'add_merchant.html')	
		except Exception as ex:
			print(ex)
			return HttpResponse('wwwwwwww')

# 	pass	




	# user_ref = db.collection('users').document(d)
	# data = user_ref.get()
	# datas = data.to_dict()
# def update_api_data(request,pk):
# 	api_id = pk
# 	print("api_id===>",api_id)
# 	asda = db.collection(u"Youtube_data").document(api_id)
# 	xx = asda.get()
# 	return render(request,'quiz.html')

# def quiz_Api_Data(request):
# 	if request.method == "POST":
# 		question = request.POST.get("question")
# 		option1 = request.POST.get("option1")
# 		option2 = request.POST.get("option2")
# 		option3 = request.POST.get("option3")
# 		option4 = request.POST.get("option4")
# 		answer = request.POST.get("answer")
# 		hidden_id = request.POST.get("hiddData")
# 		print("hidden_id==>",hidden_id)
# 		data={
# 		"Question":question,
# 		"Option1":option1,
# 		"Option2":option2,
# 		"Option3":option3,
# 		"Option4":option4,
# 		"Answer":answer
# 		}
# 		asda = db.collection(u"Youtube_data").document(hidden_id)
# 		xx = asda.update(data)
# 		print("xx===>",data)
# 		return HttpResponse("data updated")	

# def homeData(request):
# 	response = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=PL1WVjBsN-_NJ4urkLt7iVDocVu_ZQgVzF&key=AIzaSyAmKTIOpxv3H2Csf-Eabsax4s1qpOmnqXg')
# 	geodata = response.json()
# 	digit_value = 0
# 	for geodata_val in geodata:
# 		if digit_value <= len(geodata_val):
# 			youtube_api_values = geodata["items"][digit_value]["snippet"]
# 			remove_data = ('description','channelId','publishedAt','position')
# 			for data_loop_val in remove_data:
# 				youtube_api_values.pop(data_loop_val)
# 			doc_ref = db.collection(u"Youtube_data").document()
# 			doc_ref.set(youtube_api_values)
# 			digit_value+=1
# 	return JsonResponse(youtube_api_values, safe=False)

# def form_Quiz(request):
# 	return render(request,'quiz.html')		
	
	


