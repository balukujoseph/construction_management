"""
URL configuration for constructionmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from management.views import (
    admin_dashboard_view,
    add_activity_view,
    add_client_view,
    add_employee_view,
    add_equipment_view,
    add_material_view,
    add_project_view,
    add_task_view,
    delete_record_view,
    edit_record_view,
    home_view,
    index_view,
    logout_view,
    project_list_view,
    sign_up_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index_page'),
    path('logout/', logout_view, name='logout_page'),
    path('signup/', sign_up_view, name='sign_up_page'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('home/', home_view, name='home_page'),
    path('projects/', project_list_view, name='project_list_page'),
    path('add_client/', add_client_view, name='add_client_page'),
    path('add_material/', add_material_view, name='add_material_page'),
    path('add_equipment/', add_equipment_view, name='add_equipment_page'),
    path('add_project/', add_project_view, name='add_project_page'),
    path('add_employee/', add_employee_view, name='add_employee_page'),
    path('add_activity/', add_activity_view, name='add_activity_page'),
    path('add_task/', add_task_view, name='add_task_page'),
    path('records/<str:record_type>/<int:pk>/edit/', edit_record_view, name='edit_record'),
    path('records/<str:record_type>/<int:pk>/delete/', delete_record_view, name='delete_record'),
]
