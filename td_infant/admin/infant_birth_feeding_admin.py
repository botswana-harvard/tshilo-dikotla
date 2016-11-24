from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin_mixins import TabularInlineMixin
from edc_export.actions import export_as_csv_action

from ..forms import InfantVaccinesForm, InfantBirthFeedinVaccineForm
from ..models import InfantBirthFeedingVaccine, InfantVaccines

from .admin_mixins import CrfModelAdminMixin


class InfantVaccinesInline(TabularInlineMixin, admin.TabularInline):

    model = InfantVaccines
    form = InfantVaccinesForm
    extra = 0


@admin.register(InfantBirthFeedingVaccine)
class InfantBirthFeedingVaccineAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantBirthFeedinVaccineForm

    list_display = ('feeding_after_delivery',)

    list_filter = ('feeding_after_delivery',)

    inlines = [InfantVaccinesInline]

    radio_fields = {'feeding_after_delivery': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth Feeding & Vaccination",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_visit__appointment__registered_subject__dob',
                 }),
        )]


@admin.register(InfantVaccines)
class InfantVaccinesAdmin(admin.ModelAdmin):
    form = InfantVaccinesForm
