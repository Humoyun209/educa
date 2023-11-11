from django.http import HttpRequest, HttpResponse
from django.apps import apps
from django.forms import modelform_factory
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from courses.models import Content, Course, Module, Subject
from courses.forms import ModuleFormSet
from students.forms import CourseEnrollForm


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerEditMixin, OwnerCourseMixin):
    template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = "courses/manage/course/list.html"
    permission_required = "course.view_course"


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = "course.create_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = "course.change_course"


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
    permission_required = "course.delete_course"


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(data=data, instance=self.course)

    def dispatch(self, request: HttpRequest, pk: int) -> HttpResponse:
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_course_list")
        return self.render_to_response({"formset": formset, "course": self.course})

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({"formset": formset, "course": self.course})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context


class CourseList(TemplateResponseMixin, View):
    template_name = 'courses/course/list.html'

    def get(self, request):
        subjects = Subject.objects.prefetch_related('courses')
        return  self.render_to_response({'subjects': subjects})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = "courses/manage/content/form.html"

    def get_model(self, model_name):
        if model_name in ["text", "video", "file", "image"]:
            return apps.get_model(app_label="courses", model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model=self.model, exclude=["owner", "created", "updated", "order"]
        )
        return Form(*args, **kwargs)

    def dispatch(
        self, request: HttpRequest, module_id, model_name, id=None
    ) -> HttpResponse:
        self.model = self.get_model(model_name)
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)

        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            model=self.model, instance=self.obj, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect("module_content_list", self.module.id)
        return self.render_to_response({"form": form, "object": self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect("module_content_list", module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = "courses/manage/module/content_list.html"

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({"module": module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'ok'})
    

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                                   module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'ok'})