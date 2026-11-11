from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

# --------------------------------------------------------------------------------------------
# View xem chi tiết khóa học và danh sách câu hỏi
# --------------------------------------------------------------------------------------------
def course_details(request, course_id):
    """
    Hiển thị thông tin chi tiết khóa học, các bài học và đề thi.
    """
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)


# --------------------------------------------------------------------------------------------
# TASK 5: submit & show_exam_result Views
# --------------------------------------------------------------------------------------------
def submit(request, course_id):
    """
    Xử lý việc nộp bài thi của học viên.
    """
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    # Dùng get_or_create để tự động tạo Enrollment nếu user chưa đăng ký
    enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)

    if request.method == 'POST':
        # 1. Tạo một bản ghi Submission mới
        submission = Submission.objects.create(enrollment=enrollment)

        # 2. Thu thập danh sách ID đáp án người dùng chọn từ request.POST
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_') or key == 'choice':
                if isinstance(value, list):
                    selected_choice_ids.extend(value)
                else:
                    selected_choice_ids.append(value)

        # 3. Gán các Choice đã chọn vào quan hệ Many-to-Many của Submission
        for choice_id in selected_choice_ids:
            choice = get_object_or_404(Choice, pk=int(choice_id))
            submission.choices.add(choice)

        submission.save()

        # 4. Chuyển hướng tới trang hiển thị kết quả
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

    return redirect('onlinecourse:course_details', course_id=course.id)


def show_exam_result(request, course_id, submission_id):
    """
    Tính điểm bài thi và hiển thị kết quả cho học viên.
    """
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Lấy danh sách ID các đáp án học viên đã tick
    selected_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    total_possible_score = 0

    # Lấy toàn bộ câu hỏi liên kết trực tiếp với Course hoặc thông qua Lesson
    questions = Question.objects.filter(course=course)
    if not questions.exists():
        questions = Question.objects.filter(lesson__course=course)

    # Tính tổng điểm đạt được
    for question in questions:
        total_possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade

    # Tính phần trăm điểm thu được
    score_percentage = 0
    if total_possible_score > 0:
        score_percentage = int((total_score / total_possible_score) * 100)

    # Điều kiện qua bài thi (đạt tối thiểu 70%)
    passed = score_percentage >= 70

    context['course'] = course
    context['submission'] = submission
    context['selected_ids'] = selected_ids
    context['total_score'] = total_score
    context['total_possible_score'] = total_possible_score
    context['score_percentage'] = score_percentage
    context['passed'] = passed

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
from django.contrib.auth import logout, login, authenticate

# Bổ sung hàm xử lý Đăng nhập
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect('onlinecourse:course_details', course_id=1)

# Bổ sung hàm xử lý Đăng xuất
def logout_request(request):
    logout(request)
    return redirect('onlinecourse:course_details', course_id=1)
