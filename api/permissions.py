from typing import Any

from django.http import HttpRequest
from rest_framework.permissions import BasePermission

from courses.models import Course


class IsEnrolled(BasePermission):
    def has_object_permission(self, request: HttpRequest, view: Any, obj: Course) -> bool:
        return obj.students.filter(id=request.user.id).exists()