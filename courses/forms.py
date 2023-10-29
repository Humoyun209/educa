from django import forms
from django.forms.models import inlineformset_factory
from courses.models import Course, Module


ModuleFormSet = inlineformset_factory(parent_model=Course,
                                      model=Module,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)