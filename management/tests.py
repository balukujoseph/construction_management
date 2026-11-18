from datetime import date

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import Client as TestClient
from django.test import TestCase, override_settings
from django.urls import reverse

from management.forms import ClientForm, EmployeeForm
from management.models import (
    Activity,
    Client,
    Employee,
    Equipment,
    Material,
    Project,
    Task,
)


@override_settings(ALLOWED_HOSTS=['testserver'])
class RecordActionTests(TestCase):
    def setUp(self):
        self.client_record = Client.objects.create(
            first_name='Ava',
            last_name='Stone',
            email='ava@example.com',
            phone='555-0101',
            address='Main Street',
            gender='F',
        )
        self.project = Project.objects.create(
            name='Office Build',
            description='Office construction',
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            client=self.client_record,
        )
        self.task = Task.objects.create(
            name='Foundation',
            description='Prepare the site',
            start_date=date(2025, 1, 2),
            end_date=date(2025, 2, 1),
            project=self.project,
        )
        self.employee = Employee.objects.create(
            first_name='Noah',
            last_name='Reed',
            email='noah@example.com',
            phone='555-0102',
            department='Construction',
            address='Second Street',
            gender='M',
        )
        self.material = Material.objects.create(
            name='Lumber',
            quantity=10,
            unit_price='12.50',
        )
        self.equipment = Equipment.objects.create(
            name='Mixer',
            quantity=2,
            unit_price='100.00',
        )
        self.activity = Activity.objects.create(
            name='Site preparation',
            description='Prepare the construction site',
            start_date=date(2025, 1, 3),
            end_date=date(2025, 1, 10),
            project=self.project,
        )

    def test_all_tables_link_to_edit_and_delete_pages(self):
        table_records = (
            ('client', self.client_record, 'add_client_page'),
            ('project', self.project, 'add_project_page'),
            ('task', self.task, 'add_task_page'),
            ('employee', self.employee, 'add_employee_page'),
            ('material', self.material, 'add_material_page'),
            ('equipment', self.equipment, 'add_equipment_page'),
            ('activity', self.activity, 'add_activity_page'),
        )

        for record_type, record, list_url in table_records:
            with self.subTest(record_type=record_type):
                response = self.client.get(reverse(list_url))
                self.assertContains(response, 'Navbar')
                self.assertContains(
                    response,
                    reverse('edit_record', args=(record_type, record.pk)),
                )
                self.assertContains(
                    response,
                    reverse('delete_record', args=(record_type, record.pk)),
                )

    def test_client_and_employee_address_boxes_match_input_height(self):
        for form_class in (ClientForm, EmployeeForm):
            with self.subTest(form=form_class.__name__):
                self.assertEqual(form_class().fields['address'].widget.attrs['rows'], 1)

    def test_edit_updates_record_and_returns_to_its_table(self):
        edit_url = reverse('edit_record', args=('material', self.material.pk))
        edit_page = self.client.get(edit_url)
        self.assertContains(edit_page, 'class="menu-sidebar"')
        self.assertContains(edit_page, '/static/css/app.css')
        self.assertContains(edit_page, '/static/js/main-vanilla.js')

        response = self.client.post(
            edit_url,
            {
                'name': 'Updated Lumber',
                'quantity': '25',
                'unit_price': '15.75',
            },
        )

        self.assertRedirects(response, reverse('add_material_page'))
        self.material.refresh_from_db()
        self.assertEqual(self.material.name, 'Updated Lumber')
        self.assertEqual(self.material.quantity, 25)

    def test_home_page_has_project_list_nav_link(self):
        response = self.client.get(reverse('home_page'))

        self.assertContains(
            response,
            f'<a class="nav-link" href="{reverse("project_list_page")}">Project List</a>',
        )
        self.assertContains(response, 'Navbar')

    def test_contact_button_links_to_message_dialog(self):
        response = self.client.get(reverse('home_page'))

        self.assertContains(
            response,
            f'<a id="contactNavLink" class="btn btn-primary" href="{reverse("home_page")}#contactDialog">Contact Us</a>',
        )
        self.assertContains(response, '<dialog id="contactDialog">')
        self.assertContains(response, 'name="message"')
        self.assertContains(response, 'window.location.hash === "#contactDialog"')

    def test_contact_form_shows_success_message(self):
        response = self.client.post(
            reverse('home_page'),
            {
                'name': 'Ava Stone',
                'email': 'ava@example.com',
                'message': 'Please contact me about my project.',
            },
        )

        self.assertContains(response, 'Message sent successfully.')

    def test_login_page_renders_with_base_template(self):
        response = self.client.get(reverse('index_page'))

        self.assertContains(response, '<title>Login - Construction Management</title>')
        self.assertNotContains(response, 'Navbar')
        self.assertContains(response, 'Sign in to continue')
        self.assertContains(response, 'New here? Create an account below.')

    def test_login_authenticates_user(self):
        user = get_user_model().objects.create_user(
            username='existing-user',
            password='SecurePassword123!',
        )

        response = self.client.post(
            reverse('index_page'),
            {'username': 'existing-user', 'password': 'SecurePassword123!'},
        )

        self.assertRedirects(response, reverse('home_page'))
        self.assertEqual(self.client.session['_auth_user_id'], str(user.pk))

    def test_logout_requires_post_and_ends_session(self):
        user = get_user_model().objects.create_user(
            username='signed-in-user',
            password='SecurePassword123!',
        )
        self.client.force_login(user)
        logout_url = reverse('logout_page')

        self.assertEqual(self.client.get(logout_url).status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post(logout_url)

        self.assertRedirects(response, reverse('index_page'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_staff_admin_link_and_management_model_registration(self):
        models = (Activity, Client, Employee, Equipment, Material, Project, Task)
        for model in models:
            with self.subTest(model=model.__name__):
                self.assertTrue(admin.site.is_registered(model))

        admin_user = get_user_model().objects.create_superuser(
            username='admin-user',
            email='admin@example.com',
            password='SecurePassword123!',
        )
        self.client.force_login(admin_user)
        response = self.client.get(reverse('home_page'))

        self.assertContains(
            response,
            f'<a class="nav-link" href="{reverse("admin_dashboard")}">Admin Dashboard</a>',
        )

    def test_admin_dashboard_is_staff_only_and_shows_record_counts(self):
        dashboard_url = reverse('admin_dashboard')
        anonymous_response = self.client.get(dashboard_url)
        self.assertRedirects(
            anonymous_response,
            f'{reverse("index_page")}?next={dashboard_url}',
            fetch_redirect_response=False,
        )

        admin_user = get_user_model().objects.create_superuser(
            username='dashboard-admin',
            email='dashboard-admin@example.com',
            password='SecurePassword123!',
        )
        self.client.force_login(admin_user)
        response = self.client.get(dashboard_url)

        self.assertContains(response, 'Admin Dashboard')
        self.assertContains(response, '<body class="app">')
        self.assertContains(response, '/static/css/theme.css')
        self.assertContains(response, reverse('admin:management_client_changelist'))
        self.assertContains(response, str(Client.objects.count()))

    def test_base_template_loads_local_static_assets(self):
        response = self.client.get(reverse('home_page'))

        self.assertContains(response, '/static/css/bootstrap.min.css')
        self.assertContains(response, '/static/css/page-layout.css')
        self.assertContains(response, '/static/js/bootstrap.bundle.min.js')

    def test_signup_creates_user_and_logs_them_in(self):
        signup_page = self.client.get(reverse('sign_up_page'))
        self.assertContains(signup_page, 'Create an Account')

        response = self.client.post(
            reverse('sign_up_page'),
            {
                'username': 'new-user',
                'password1': 'SecurePassword123!',
                'password2': 'SecurePassword123!',
            },
        )

        user = get_user_model().objects.get(username='new-user')
        self.assertRedirects(response, reverse('home_page'))
        self.assertEqual(self.client.session['_auth_user_id'], str(user.pk))

    def test_base_navbar_has_login_and_project_list(self):
        response = self.client.get(reverse('home_page'))
        navbar = response.content.decode().split('</nav>', 1)[0]
        login_button = f'<a class="btn btn-primary mr-2" href="{reverse("index_page")}">Login</a>'
        self.assertIn(login_button, navbar)
        self.assertLess(navbar.index(login_button), navbar.index('<a class="navbar-brand"'))
        self.assertIn(
            f'<a class="nav-link" href="{reverse("project_list_page")}">Project List</a>',
            navbar,
        )
        self.assertIn(
            f'<a class="nav-link" href="{reverse("home_page")}">Home',
            navbar,
        )
        self.assertNotIn('Dropdown link', navbar)
        contact_button = f'<a id="contactNavLink" class="btn btn-primary" href="{reverse("home_page")}#contactDialog">Contact Us</a>'
        self.assertIn(contact_button, navbar)
        self.assertLess(navbar.index('Project List'), navbar.index('Contact Us'))

    def test_project_list_page_shows_registered_projects_without_add_form(self):
        response = self.client.get(reverse('project_list_page'))

        self.assertContains(response, self.project.name)
        self.assertContains(
            response,
            reverse('edit_record', args=('project', self.project.pk)),
        )
        self.assertContains(response, 'Navbar')
        self.assertNotContains(response, 'ADD PROJECT')

    def test_delete_requires_confirmation_and_warns_about_cascades(self):
        delete_url = reverse('delete_record', args=('project', self.project.pk))
        csrf_client = TestClient(enforce_csrf_checks=True)

        confirmation = csrf_client.get(delete_url)

        self.assertContains(confirmation, 'Confirm Delete')
        self.assertContains(confirmation, 'tasks and activities')
        self.assertContains(confirmation, 'Navbar')
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
        csrf_token = confirmation.cookies['csrftoken'].value
        response = csrf_client.post(delete_url, HTTP_X_CSRFTOKEN=csrf_token)

        self.assertRedirects(response, reverse('add_project_page'))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertFalse(Activity.objects.filter(pk=self.activity.pk).exists())
