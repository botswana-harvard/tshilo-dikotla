from django.contrib import admin

from edc_lab.receive.admin_mixins import ReceiveModelAdminMixin
# from tshilo_dikotla.admin_mixins import MembershipBaseModelAdmin
from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin
from ..models import Receive


@admin.register(Receive)
class ReceiveAdmin(ReceiveModelAdminMixin, EdcBaseModelAdminMixin):

    date_hierarchy = 'receive_datetime'

    list_display = ("receive_identifier", "requisition", "receive_datetime", "drawn_datetime",
                    'registered_subject', 'created', 'modified', 'import_datetime')

    search_fields = ('registered_subject__subject_identifier',
                     "receive_identifier", "requisition_identifier",)

    list_filter = ('created', "receive_datetime", "drawn_datetime", 'modified', 'import_datetime', )

    list_per_page = 15

    def get_readonly_fields(self, request, obj):
        return (['receive_identifier', 'requisition_model_name', 'clinician_initials'] +
                [field.name for field in obj._meta.fields if field.editable])
