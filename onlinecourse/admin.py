from django.contrib import admin

# TASK 2: Import đúng 7 lớp Model bắt buộc
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


# TASK 2: Định nghĩa ChoiceInline
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


# TASK 2: Định nghĩa QuestionInline
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2


# TASK 2: Định nghĩa QuestionAdmin tích hợp ChoiceInline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']


# TASK 2: Định nghĩa LessonAdmin tích hợp QuestionInline
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course']


class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['name', 'pub_date']


# Đăng ký các Model vào Trang Admin
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
