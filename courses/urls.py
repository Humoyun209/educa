from django.urls import path
from courses import views


urlpatterns = [
    path("mine/", views.ManageCourseListView.as_view(), name="manage_course_list"),
    path("create/", views.CourseCreateView.as_view(), name="course_create"),
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course_edit"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("list/", views.CourseList.as_view(), name="course_list"),
    path(
        "<int:pk>/module/",
        views.CourseModuleUpdateView.as_view(),
        name="course_module_update",
    ),
    path(
        "module/<int:module_id>/content/<str:model_name>/create/",
        views.ContentCreateUpdateView.as_view(),
        name="module_content_create",
    ),
    path(
        "module/<int:module_id>/content/<str:model_name>/<int:id>/",
        views.ContentCreateUpdateView.as_view(),
        name="module_content_update",
    ),
    path(
        "content/delete/<int:id>/",
        views.ContentDeleteView.as_view(),
        name="module_content_delete",
    ),
    path(
        "module/<int:module_id>/",
         views.ModuleContentListView.as_view(),
         name='module_content_list'
    ),
    path(
        'module/order/',
         views.ModuleOrderView.as_view(),
         name='module_order'
    ),
    path('content/order/',
         views.ContentOrderView.as_view(),
         name='content_order'
    )
]
