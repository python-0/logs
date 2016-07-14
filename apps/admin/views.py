from flask import flash, redirect, url_for, request
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField
from flask_admin.form import rules
from wtforms.validators import DataRequired, Email, IPAddress


class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


class UserAdminView(ModelView):
    column_display_pk = True
    column_list = ['id', 'name', 'email', 'confirmd', 'admin']
    column_searchable_list = ['name']
    column_sortable_list = ['name']
    column_exclude_list = ['password_hash']

    form_edit_rules = (
        rules.FieldSet(('name', 'email', 'confirmd', 'admin'), 'Personal'),
        rules.Header('Reset Password'),
        'password', 'confirm'
    )

    form_create_rules = (
        'name', 'email', 'admin', 'password', 'confirm'
    )

    form_args = {
         'email': {
             'validators': [Email()]
         }
    }

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        form_class.confirm = PasswordField('Confirm Password')
        return form_class

    def create_model(self, form):
        model = self.model(
             form.email.data, form.name.data, form.password.data,
             form.admin.data, form.confirmd.data
        )
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

    def update_model(self, form, model):
        form.populate_obj(model)
        if form.password.data:
            if form.password.data != form.confirm.data:
                flash('Password must match')
                return
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()


class HostsAdminView(ModelView):
    column_display_pk = True
    create_modal = True
    column_editable_list = ['hostname', 'ipaddress', 'az']
    column_searchable_list = ['hostname', 'ipaddress']
    column_sortable_list = ['hostname', 'az']

    form_create_rules = (
        'hostname', 'ipaddress', 'az'
    )

    def create_model(self, form):
        model = self.model(
            form.hostname.data, form.ipaddress.data,
            form.az.data
        )
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()


class ProjectsAdminView(ModelView):
    column_display_pk = True
    column_list = ['id', 'project_name', 'host', 'log_path']
    column_searchable_list = ['project_name']
    column_sortable_list = ['project_name']

    form_edit_rules = (
        'project_name', 'host', 'log_path'
    )

    form_create_rules = (
        'project_name', 'host', 'log_path'
    )

    # form_ajax_refs = {
    #     'host': {
    #         'fields': ['hostname', ],
    #         'page_size': 10
    #     }
    # }

    def create_model(self, form):
        model = self.model(
            form.project_name.data, form.host.data,
            form.log_path.data
        )
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

    def update_model(self, form, model):
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()


