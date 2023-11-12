from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView

from courses.models import Course
from students.forms import CourseEnrollForm


class StudentRegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')
    template_name = 'students/student/registration.html'
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return super().form_valid(form)


class StudentEnrollCourse(LoginRequiredMixin, FormView):
    form_class = CourseEnrollForm
    course = None

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=(self.course.pk, ))


class StudentCourseListView(LoginRequiredMixin, ListView):
    queryset = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.objects.filter(students__in=[self.request.user])
    


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        module_id = self.kwargs.get('module_id')
        if module_id is None:
            context['module'] = course.modules.all()[0]
        else:
            context['module'] = course.modules.get(id=module_id)
        return context


