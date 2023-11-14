from django.urls import include, path
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'course', views.CourseViewset)


app_name = 'course_api'


urlpatterns = [
    path("", include(router.urls)),
]