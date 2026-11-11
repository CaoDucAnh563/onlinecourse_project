from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Route xem chi tiết khóa học
    path('<int:course_id>/', views.course_details, name='course_details'),
    
    # Routes Đăng nhập & Đăng xuất (Khắc phục lỗi NoReverseMatch)
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    
    # Routes submit bài thi và xem kết quả (Task 6)
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]
