
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from management.forms import (
    ContactForm,
    ClientForm,
    ProjectForm,
    TaskForm,
    EmployeeForm,
    MaterialForm,
    EquipmentForm,
    ActivityForm
)

from management.models import (
    Activity,
    Client,
    Employee,
    Equipment,
    Material,
    Project,
    Task,
)

RECORD_CONFIG = {
    'client': {
        'model': Client,
        'form': ClientForm,
        'label': 'Client',
        'list_url': 'add_client_page',
        'delete_warning': 'Deleting this client will also delete its projects, tasks, and activities.',
    },
    'project': {
        'model': Project,
        'form': ProjectForm,
        'label': 'Project',
        'list_url': 'add_project_page',
        'delete_warning': 'Deleting this project will also delete its tasks and activities.',
    },
    'task': {
        'model': Task,
        'form': TaskForm,
        'label': 'Task',
        'list_url': 'add_task_page',
        'delete_warning': '',
    },
    'employee': {
        'model': Employee,
        'form': EmployeeForm,
        'label': 'Employee',
        'list_url': 'add_employee_page',
        'delete_warning': '',
    },
    'material': {
        'model': Material,
        'form': MaterialForm,
        'label': 'Material',
        'list_url': 'add_material_page',
        'delete_warning': '',
    },
    'equipment': {
        'model': Equipment,
        'form': EquipmentForm,
        'label': 'Equipment',
        'list_url': 'add_equipment_page',
        'delete_warning': '',
    },
    'activity': {
        'model': Activity,
        'form': ActivityForm,
        'label': 'Activity',
        'list_url': 'add_activity_page',
        'delete_warning': '',
    },
}


def index_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Login successful.')
            return redirect('home_page')
    else:
        form = AuthenticationForm(request)

    if not request.user.is_authenticated:
        messages.info(request, 'New here? Create an account below.')

    context = {
        'form': form,
        'msg': list(get_messages(request)),
    }
    return render(request, 'index.html', context)


def home_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            messages.success(request, 'Message sent successfully.')
            
    else:
        contact_form = ContactForm()
    context = {
        'contact_form': contact_form,
        'msg': list(get_messages(request)),
    }
    return render(request, 'home.html', context)


def project_list_view(request):
    context = {
        'projects': Project.objects.select_related('client').all(),
        'msg': list(get_messages(request)),
    }
    return render(request, 'project_list.html', context)


@staff_member_required(login_url='index_page')
def admin_dashboard_view(request):
    dashboard_items = (
        {
            'label': 'Clients',
            'count': Client.objects.count(),
            'url': reverse('admin:management_client_changelist'),
        },
        {
            'label': 'Projects',
            'count': Project.objects.count(),
            'url': reverse('admin:management_project_changelist'),
        },
        {
            'label': 'Tasks',
            'count': Task.objects.count(),
            'url': reverse('admin:management_task_changelist'),
        },
        {
            'label': 'Employees',
            'count': Employee.objects.count(),
            'url': reverse('admin:management_employee_changelist'),
        },
        {
            'label': 'Materials',
            'count': Material.objects.count(),
            'url': reverse('admin:management_material_changelist'),
        },
        {
            'label': 'Equipment',
            'count': Equipment.objects.count(),
            'url': reverse('admin:management_equipment_changelist'),
        },
        {
            'label': 'Activities',
            'count': Activity.objects.count(),
            'url': reverse('admin:management_activity_changelist'),
        },
    )
    context = {
        'dashboard_items': dashboard_items,
        'msg': list(get_messages(request)),
    }
    return render(request, 'dashboard.html', context)


def add_client_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client added successfully.')
            
    else:
        form = ClientForm()

    clients = Client.objects.all()
    context = {
        'form': form,
        'clients': clients,
        'msg': list(get_messages(request)),
    }
    return render(request, 'add_client.html', context)


def add_material_view(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material added successfully.')
           
    else:
        form = MaterialForm()

    materials = Material.objects.all()
    context = {
        'form': form,
        'materials': materials,
        'msg': list(get_messages(request)),
    }
    return render(request, 'add_material.html', context)


def add_equipment_view(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment added successfully.')
            
    else:
        form = EquipmentForm()

    equipment_list = Equipment.objects.all()
    context = {
        'form': form,
        'equipment_list': equipment_list,
        'msg': list(get_messages(request)),
    }
    return render(request, 'add_equipment.html', context)


def add_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project added successfully.')
            
    else:
        form = ProjectForm()

    projects = Project.objects.all()
    context = {
        'form': form,
        'projects': projects,
        'msg': list(get_messages(request)),
    }
    return render(request, 'add_project.html', context)


def add_employee_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully.')
            
    else:
        form = EmployeeForm()

    employees = Employee.objects.all()
    context = {
        'form': form,
        'employees': employees,
        'msg': list(get_messages(request)),
    }
    return render(request, 'add_employee.html', context)


def add_activity_view(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity added successfully.')
            
    else:
        form = ActivityForm()

    activities = Activity.objects.select_related('project').all()
    context = {
        'form': form,
        'activities': activities,
        'msg': list(get_messages(request)),
    }
    return render(request, 'add_activity.html', context)


def add_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully.')
           
    else:
        form = TaskForm()

    tasks = Task.objects.select_related('project').all()
    context = {
        'form': form,
        'tasks': tasks,
        'msg': list(get_messages(request)),
    }
    return render(request, 'add_task.html', context)



@require_http_methods(['GET', 'POST'])
def edit_record_view(request, record_type, pk):
    config = RECORD_CONFIG.get(record_type)
    if config is None:
        raise Http404('Unknown record type.')

    record = get_object_or_404(config['model'], pk=pk)
    form_class = config['form']
    if request.method == 'POST':
        form = form_class(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, f"{config['label']} updated successfully.")
            return redirect(config['list_url'])
        messages.error(request, 'Please correct the errors and try again.')
    else:
        form = form_class(instance=record)

    context = {
        'form': form,
        'record': record,
        'record_label': config['label'],
        'list_url': config['list_url'],
        'msg': list(get_messages(request)),
    }
    return render(request, 'edit_record.html', context)


@require_http_methods(['GET', 'POST'])
def delete_record_view(request, record_type, pk):
    config = RECORD_CONFIG.get(record_type)
    if config is None:
        raise Http404('Unknown record type.')

    record = get_object_or_404(config['model'], pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, f"{config['label']} deleted successfully.")
        return redirect(config['list_url'])

    context = {
        'record': record,
        'record_label': config['label'],
        'delete_warning': config['delete_warning'],
        'list_url': config['list_url'],
        'msg': list(get_messages(request)),
    }
    return render(request, 'delete_record.html', context)

@require_http_methods(['GET', 'POST'])
def sign_up_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('home_page')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'msg': list(get_messages(request)),
    }
    return render(request, 'regesitration/sign_up.html', context)


@require_POST
def logout_view(request):
    logout(request)
    return redirect('index_page')
