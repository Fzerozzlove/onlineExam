
import sys
from django.shortcuts import render, redirect
from student import models
from django.http import HttpResponse
from django.contrib.auth import logout
from django.db import connection, transaction

# Create your views here.

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
    defaultencoding = sys.getdefaultencoding()

def index(request):
	return render(request, 'index.html')

def toIndex(request):
	return render(request, 'index.html')

def logout(request):
	return redirect('/toIndex')

def studentLogin(request):
	if request.method == 'POST':
		if 'log' in request.POST:
			stuid = request.POST.get('id')
			password = request.POST.get('password')
		elif 'reg' in request.POST:
			return render(request, 'studentRegister.html')

		student = models.Student.objects.get(id = stuid)
		print(student)
		if password == student.password:
			paper = models.Paper.objects.filter(major = student.major)
			grade = models.Grade.objects.filter(sid = student.id)
			return render(request, 'index.html', {
				'student': student,
				'paper': paper,
				'grade': grade
				})
		else: 
			return render(request, 'index.html', {
				'message': '密码不正确'
				})

def teacherLogin(request):
	if request.method == 'POST':
		if 'log' in request.POST:
			teaid = request.POST.get('id')
			password = request.POST.get('password')
		elif 'reg' in request.POST:
			return render(request, 'teacherRegister.html')

		teacher = models.Teacher.objects.get(id = teaid)
		print(teacher)

		if password == teacher.password:
			paper = models.Paper.objects.filter(tid = teacher.id)

			data1 = models.Grade.objects.filter(subject = '软件工程', grade__lt=60).count()
			data2 = models.Grade.objects.filter(subject = '软件工程', grade__gte=60, grade__lt=70).count()
			data3 = models.Grade.objects.filter(subject = '软件工程', grade__gte=70, grade__lt=80).count()
			data4 = models.Grade.objects.filter(subject = '软件工程', grade__gte=80, grade__lt=90).count()
			data5 = models.Grade.objects.filter(subject = '软件工程', grade__gte=90).count()

			data = {
				'data1': data1,
				'data2': data2,
				'data3': data3,
				'data4': data4,
				'data5': data5,
			}

			print(data)

			return render(request, 'teacher.html', {
				'teacher': teacher,
				'paper': paper,
				'data': data,
            	})

		else: 
			return render(request, 'index.html', {
				'message': '密码不正确'
			})

def startExam(request):
	sid = request.GET.get('sid')
	subject1 = request.GET.get('subject')
	student = models.Student.objects.get(id = sid)
	paper = models.Paper.objects.filter(subject = subject1)
	return render(request, 'exam.html', {
		'student': student,
		'paper': paper,
		'subject': subject1,
		})

def calGrade(request):
	if request.method == 'POST':
		sid = request.POST.get('sid')
		subject1 = request.POST.get('subject')
		student = models.Student.objects.get(id = sid)
		paper = models.Paper.objects.filter(major = student.major)
		grade = models.Grade.objects.filter(sid = student.id)
		question = models.Paper.objects.get(subject = subject1).pid.all().values('id', 'answer', 'score')

		print(question)

		mygrade = 0
		for p in question:
			qid = str(p['id'])
			my_ans = request.POST.get(qid)
			right_ans = p['answer']
			if my_ans == right_ans:
				mygrade += p['score']

		models.Grade.objects.create(sid_id = sid, subject = subject1, grade = mygrade)

		return render(request, 'index.html', {
			'student': student,
			'paper': paper,
			'grade': grade,
			})

def showGrade(request):
	subject1 = request.GET.get('subject')
	grade = models.Grade.objects.filter(subject = subject1)

	data1 = models.Grade.objects.filter(subject = subject1, grade__lt = 60).count()
	data2 = models.Grade.objects.filter(subject = subject1, grade__gte = 60, grade__lt = 70).count()
	data3 = models.Grade.objects.filter(subject = subject1, grade__gte = 70, grade__lt = 80).count()
	data4 = models.Grade.objects.filter(subject = subject1, grade__gte = 80, grade__lt = 90).count()
	data5 = models.Grade.objects.filter(subject = subject1, grade__gte = 90).count()

	data = {
		'data1': data1,
		'data2': data2,
		'data3': data3,
		'data4': data4,
		'data5': data5,
	}

	return render(request, 'showGrade.html', {
		'grade': grade,
		'data': data,
		'subject': subject1,
		})

def dictfetchall(cursor):
	desc = cursor.description
	return [
		dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
	]

def queryStudent(request):
	sid = request.GET.get('id')
	sex = request.GET.get('sex')
	subject1 = request.GET.get('subject')

	tid = request.GET.get('tid')
	teacher = models.Teacher.objects.get(id = tid)
	paper = models.Paper.objects.filter(tid = teacher.id)

	cursor = connection.cursor()
	sql="select * from grade,student where student.id=grade.sid_id " \
        "and student.id like %s and grade.subject like %s and student.sex like %s and '1'='1'"
	val=('%'+sid+'%', '%'+subject1+'%', '%'+sex+'%')
	cursor.execute(sql, val)
	result = dictfetchall(cursor)
	
	return render(request, 'teacher.html', {
		'teacher': teacher,
		'result': result,
		'paper': paper,
		'ifactive':1
    	})

def teacherRegister(request):
	if request.method == 'POST':
		try:
			name1 = request.POST.get('name')
			id1 = request.POST.get('id')
			password1 = request.POST.get('password')
			sex1 = request.POST.get('sex')
			dept1 = request.POST.get('dept')
			email1 = request.POST.get('email')
			birth1 = request.POST.get('birth')
		except:
			return render(request, 'teacherRegister.html', {
				message: '错误的格式！请参考方框内格式填写！',
			})
		else:
			models.Teacher.objects.create(
				name = name1,
				id = id1,
				password = password1,
				sex = sex1,
				dept = dept1,
				email = email1,
				birth = birth1
			)
			teacher = models.Teacher.objects.get(id = id1)

			print(teacher)

			return render(request, 'teacher.html', {
				'teacher': teacher,
				})

def studentRegister(request):
	if request.method == 'POST':
		try:
			name1 = request.POST.get('name')
			id1 = request.POST.get('id')
			password1 = request.POST.get('password')
			sex1 = request.POST.get('sex')
			dept1 = request.POST.get('dept')
			major1 = request.POST.get('major')
			email1 = request.POST.get('email')
			birth1 = request.POST.get('birth')
		except:
			return render(request, 'teacherRegister.html', {
				message: '错误的格式！请参考方框内格式填写！',
			})
		else:
			models.Student.objects.create(
				name = name1,
				id = id1,
				password = password1,
				sex = sex1,
				dept = dept1,
				major = major1,
				email = email1,
				birth = birth1
			)
			student = models.Student.objects.get(id = id1)
			paper = models.Paper.objects.filter(major = student.major)

			print(student)

			return render(request, 'index.html', {
				'student': student,
				'paper':paper,
				})

def addq(request):
	return render(request, 'addq.html')

def questionAddition(request):
	if request.method == 'POST':
		try:
			subject1 = request.POST.get('subject')
			title1 = request.POST.get('title')
			optA1 = request.POST.get('optA')
			optB1 = request.POST.get('optB')
			optC1 = request.POST.get('optC')
			optD1 = request.POST.get('optD')
			answer1 = request.POST.get('answer')
			level1 = request.POST.get('level')
			score1 = request.POST.get('score')
		except:
			return render(request, 'teacherRegister.html', {
				message: '错误的格式！请参考方框内格式填写！',
			})
		else:
			models.Question.objects.create(
				subject = subject1,
				title = title1,
				optA = optA1,
				optB = optB1,
				optC = optC1,
				optD = optD1,
				answer = answer1,
				level = level1,
				score = score1,
			)
			return render(request, 'teacher.html')
