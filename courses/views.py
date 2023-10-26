from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy

from courses.models import Course


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    

class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    

class OwnerCourseEditMixin(OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'
    

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    

class CourseCreateView(OwnerCourseEditMixin, UpdateView):
    pass


class CourseUpdateView(OwnerCourseEditMixin, CreateView):
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'