from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course-list'),
    path('<int:course_id>/', views.course_detail, name='course-detail'),
    path('delete/<int:course_id>/', views.course_delete, name='course-delete'),
    path('update/<int:course_id>/', views.course_update, name='course-update'),
    path('create/', views.course_create, name='course-create'),
]
