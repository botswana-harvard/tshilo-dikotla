from collections import OrderedDict

from django.contrib import admin

from td_registration.models import RegisteredSubject
from edc_export.actions import export_as_csv_action

from td_maternal.models import MaternalLabourDel
from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin

from ..forms import InfantBirthForm
from ..models import InfantBirth


@admin.register(InfantBirth)
class InfantBirthAdmin(EdcBaseModelAdminMixin, admin.ModelAdmin):

    form = InfantBirthForm

    list_display = (
        'registered_subject',
        'maternal_labour_del',
        'report_datetime',
        'first_name',
        'initials',
        'dob',
        'gender',
    )

    list_display = ('report_datetime', 'first_name', 'maternal_labour_del')
    list_filter = ('gender',)
    radio_fields = {'gender': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('subject_identifier'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    subject_identifier=request.GET.get('subject_identifier', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('registered_subject')
                except ValueError:
                    self.readonly_fields.append('registered_subject')
        if db_field.name == "maternal_labour_del":
            if request.GET.get('subject_identifier'):
                maternal_subject_identifier = RegisteredSubject.objects.get(
                    subject_identifier=request.GET.get('subject_identifier')).relative_identifier
                kwargs["queryset"] = MaternalLabourDel.objects.filter(
                    registered_subject__subject_identifier=maternal_subject_identifier)
        return super(InfantBirthAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
