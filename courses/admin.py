from django.contrib import admin
from courses.models import Subject, Course, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields= {'slug': ['title']}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ['title']}
    inlines = [ModuleInline]
