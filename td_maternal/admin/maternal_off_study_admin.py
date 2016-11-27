from django.contrib import admin

from ..models import MaternalOffstudy
from ..forms import MaternalOffstudyForm
from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalOffstudy)
class MaternalOffstudyAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalOffstudyForm

    fields = (
        'maternal_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'reason_other',
        'comment')
