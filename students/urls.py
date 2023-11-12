from django.urls import path
from students import views


urlpatterns = [
    path('register/', views.StudentRegisterView.as_view(), name='student_registration'),
    path('enroll/', views.StudentEnrollCourse.as_view(), name='student_enroll_course'),
    path('my/courses/', views.StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<int:pk>/', views.StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<int:pk>/<int:module_id>/', views.StudentCourseDetailView.as_view(), name='student_course_detail_module'),
]