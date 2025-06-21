from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course-list'),
    path('<int:course_id>/', views.course_detail, name='course-detail'),
    path('delete/<int:course_id>/', views.course_delete, name='course-delete'),
    path('update/<int:course_id>/', views.course_update, name='course-update'),
    path('create/', views.course_create, name='course-create'),

    path('api/', views.course_list_api, name='course-list-api'),
    path('api/<int:course_id>/', views.course_detail_api, name='course-detail-api'),
    path('api/delete/<int:course_id>/', views.course_delete_api, name='course-delete-api'),
    path('api/update/<int:course_id>/', views.course_update_api, name='course-update-api'),
    path('api/create/', views.course_create_api, name='course-create-api'),
]
