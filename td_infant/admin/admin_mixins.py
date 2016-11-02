from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin, DashboardRedirectUrlMixin

from ..models import InfantVisit


class InfantScheduleModelModelAdminMixin(EdcBaseModelAdminMixin, DashboardRedirectUrlMixin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(
                    visit_code=request.GET.get('visit_code'), appointment_id=request.GET.get('appointment_pk'))
        return super(InfantScheduleModelModelAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)
