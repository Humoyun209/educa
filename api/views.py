from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import (
    BaseAuthentication,
    TokenAuthentication,
    BasicAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from courses.models import Course
from api.serializers import CourseSerializer
from api.permissions import IsEnrolled


class CourseViewset(ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[BasicAuthentication],
    )
    def enroll(self, request):
        course = self.get_object()
        course.students.add(request.user)
        return Response({"Enrolled": True})

    @action(
        methods=['get'],
        detail=True,
        serializer_class=CourseSerializer,
        permission_classes=[IsAuthenticated, IsEnrolled],
        authentication_classes=[BasicAuthentication]
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class CourseEnrollView(APIView):
    authentication_classes = [BaseAuthentication]
    permission_classes = [IsAuthenticated]
