from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = '在线考试系统后台'
admin.site.site_title =  '在线考试系统'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'name',
		'sex',
		'dept',
		'major',
		'password',
		'email',
		'birth'
	)

	list_display_links = (
		'id',
		'name'
	)

	search_field = [
		'name',
		'dept',
		'major',
		'birth'
	]

	list_filter = [
		'name',
		'dept',
		'major',
		'birth'
	]

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'name',
		'sex',
		'dept',
		'password',
		'email',
		'birth'
	)

	list_display_links = (
		'id',
		'name'
	)

	search_field = [
		'name',
		'dept',
		'birth'
	]

	list_filter = [
		'name',
		'dept'
	]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'subject',
		'title',
		'optA',
		'optB',
		'optC',
		'optD',
		'answer',
		'level',
		'score'
	)

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
	list_display = (
		'tid',
		'major',
		'subject',
		'time',
	)

	list_display_links = (
		'major',
		'subject',
		'time',
	)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
	list_display = (
		'sid',
		'subject',
		'grade',
	)

	list_display_links = (
		'sid',
		'subject',
		'grade',
	)