from django.contrib import admin

from edc_base.modeladmin_mixins import TabularInlineMixin

from ..admin_site import td_maternal_admin
from ..forms import MaternalArvPregForm, MaternalArvForm
from ..models import MaternalArvPreg, MaternalArv

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalArvInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = MaternalArv
    form = MaternalArvForm
    extra = 1


@admin.register(MaternalArv, site=td_maternal_admin)
class MaternalArvAdmin(admin.ModelAdmin):
    form = MaternalArvForm


@admin.register(MaternalArvPreg, site=td_maternal_admin)
class MaternalArvPregAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):
    form = MaternalArvPregForm
    inlines = [MaternalArvInlineAdmin, ]
    list_display = ('maternal_visit', 'took_arv',)
    list_filter = ('took_arv',)
    radio_fields = {'took_arv': admin.VERTICAL,
                    'is_interrupt': admin.VERTICAL,
                    'interrupt': admin.VERTICAL
                    }
