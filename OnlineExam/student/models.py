from django.db import models

# Create your models here.

SEX = (
	('男', '男'),
	('女', '女'),
)

DEPT=(
	('计算机科学与技术学院', '计算机科学与技术学院'),
	('化学工程学院', '化学工程学院'),
	('经济管理学院', '经济管理学院'),
	('理学院', '理学院'),
)



class Student(models.Model):
	id = models.CharField('学号', max_length = 20, primary_key = True)
	name = models.CharField('姓名', max_length = 20)
	sex = models.CharField('性别', max_length = 4, choices = SEX, default = '男')
	dept = models.CharField('学院', max_length = 20, choices = DEPT, default = None)
	major = models.CharField('专业', max_length = 20, default = None)
	password = models.CharField('密码', max_length = 20, default = '111')
	email = models.EmailField('邮箱', default = None)
	birth = models.DateField('出生日期')

	class Meta:
		db_table = 'student'
		verbose_name = '学生'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.id

class Teacher(models.Model):
	id = models.CharField('教工号', max_length = 20, primary_key = True)
	name = models.CharField('姓名', max_length = 20)
	sex = models.CharField('性别', max_length = 4, choices = SEX, default = '男')
	dept = models.CharField('学院', max_length = 20, choices = DEPT, default = None)
	email = models.EmailField('邮箱', default = None)
	password = models.CharField('密码', max_length = 20, default = '000000')
	birth = models.DateField('出生日期')

	class Meta:
		db_table = 'teacher'
		verbose_name = '教师'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name

ANSWER = (
	('A', 'A'),
	('B', 'B'),
	('C', 'C'),
	('D', 'D'),
)

LEVEL = (
	('1', 'easy'),
	('2', 'normal'),
	('3', 'difficult'),
)

class Question(models.Model):
	id = models.AutoField(primary_key = True)
	subject = models.CharField('科目', max_length = 20)
	title = models.TextField('题目')
	optA = models.CharField('A选项', max_length = 30)
	optB = models.CharField('B选项', max_length = 30)
	optC = models.CharField('C选项', max_length = 30)
	optD = models.CharField('D选项', max_length = 30)
	answer = models.CharField('答案', max_length = 10, choices = ANSWER)
	level = models.CharField('难度', max_length = 10, choices = LEVEL)
	score = models.IntegerField('分数', default = 1)

	class Meta:
		db_table = 'question'
		verbose_name = '单项选择题库'
		verbose_name_plural = verbose_name

	def __str__(self):
		return '<%s:%s>' % (self.subject, self.title)

class Paper(models.Model):
	#pid:题号，与题库为多对多关系
	pid = models.ManyToManyField(Question)
	#外键
	tid = models.ForeignKey(Teacher, on_delete = models.CASCADE)
	subject = models.CharField('科目', max_length = 20, default = '')
	major = models.CharField('专业', max_length = 20)
	time = models.DateTimeField()

	class Meta:
		db_table = 'paper'
		verbose_name = '试卷'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.major

class Grade(models.Model):
	sid = models.ForeignKey(Student, on_delete = models.CASCADE, default = '')
	subject = models.CharField('科目', max_length = 20, default = '')
	grade = models.IntegerField()

	class Meta:
		db_table = 'grade'
		verbose_name = '成绩'
		verbose_name_plural = verbose_name

	def __str__(self):
		return '<%s:%s>' % (self.sid, self.grade)
