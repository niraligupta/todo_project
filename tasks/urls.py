from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<int:task_id>/", views.edit_task_page, name="edit_task_page"),
    path("api/tasks/", views.tasks_list_create, name="api_tasks_list_create"),
    path("api/tasks/<int:task_id>/", views.tasks_detail, name="api_tasks_detail"),
]
