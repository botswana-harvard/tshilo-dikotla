from django.contrib import admin

from ..admin_site import td_maternal_admin
from ..forms import MaternalRandoForm
from ..models import MaternalRando

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalRando, site=td_maternal_admin)
class MartenalRandoAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalRandoForm

    fields = (
        'maternal_visit',
        'report_datetime',
        'dispensed', 'comment', 'subject_identifier', 'initials', 'rx',
        'site', 'randomization_datetime', 'delivery_clinic', 'delivery_clinic_other')
    list_display = ('sid', 'subject_identifier', 'initials', 'site', 'randomization_datetime', 'user_modified',
                    'dispensed')
    search_fields = ('sid', 'subject_identifier', 'dispensed', 'initials')
    list_filter = ('randomization_datetime', 'site')
    readonly_fields = (
        'sid',
        'subject_identifier',
        'initials',
        'rx',
        'site',
        'randomization_datetime')
    radio_fields = {"delivery_clinic": admin.VERTICAL, }
