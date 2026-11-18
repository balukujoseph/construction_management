
from django.contrib import admin
from .models import Activity, Equipment, Client, Project, Task, Employee, Material


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'address')
    search_fields = ('first_name', 'last_name', 'email', 'phone')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'client')
    search_fields = ('name', 'description', 'client__first_name', 'client__last_name')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'project')
    search_fields = ('name', 'description', 'project__name')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'department', 'address')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'department')

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit_price')
    search_fields = ('name',)

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit_price')
    search_fields = ('name',)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'project')
    search_fields = ('name', 'description', 'project__name')

admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin) 
admin.site.register(Task, TaskAdmin)  
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Activity, ActivityAdmin)
