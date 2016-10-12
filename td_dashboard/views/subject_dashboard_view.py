from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

from edc_base.views import EdcBaseViewMixin
from edc_label.view_mixins import EdcLabelViewMixin
from ..classes import MarqueeViewMixin, AppointmentSubjectVisitCRFViewMixin, LocatorResultsActionsViewMixin
from td_maternal.models.maternal_consent import MaternalConsent
from td_maternal.models.requisition_meta_data import RequisitionMetadata
from edc_constants.constants import SUBJECT
from td_maternal.models.maternal_locator import MaternalLocator
from td_maternal.models.maternal_crf_meta_data import CrfMetadata


class SubjectDashboardView(
        MarqueeViewMixin,
        AppointmentSubjectVisitCRFViewMixin, LocatorResultsActionsViewMixin, EdcBaseViewMixin, EdcLabelViewMixin, TemplateView):

    def __init__(self, **kwargs):
        super(SubjectDashboardView, self).__init__(**kwargs)
        self.request = None
        self.context = {}
        self.show = None
        self.template_name = 'td_dashboard/subject_dashboard.html'

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            site_header=admin.site.site_header,
        )
        self.context.update({
            'markey_data': self.markey_data.items(),
            'markey_next_row': self.markey_next_row,
            'requistions_metadata': self.requistions_metadata,
            'scheduled_forms': self.scheduled_forms,
            'appointments': self.appointments,
            'subject_identifier': self.subject_identifier,
            'consents': [],
            'dashboard_type': SUBJECT,
            'locator': self.locator
        })
        return self.context

    def get(self, request, *args, **kwargs):
        self.request = request
        context = self.get_context_data(**kwargs)
        self.show = request.GET.get('show', None)
        context.update({'show': self.show})
        self.print_barcode_labels(request)
        return self.render_to_response(context)

    @property
    def locator(self):
        try:
            maternal_locator = MaternalLocator.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except MaternalLocator.DoesNotExist:
            maternal_locator = None
        return maternal_locator

    @property
    def scheduled_forms(self):
        scheduled_forms = CrfMetadata.objects.filter(
            subject_identifier=self.subject_identifier)
        return scheduled_forms

    @property
    def requistions_metadata(self):
        requistions_metadata = RequisitionMetadata.objects.filter(
            subject_identifier=self.subject_identifier, appointment=self.appointment)
        return requistions_metadata

    @property
    def consent(self):
        try:
            maternal_consent = MaternalConsent.objects.get(subject_identifier=self.subject_identifier)
        except MaternalConsent.DoesNotExist:
            maternal_consent = None
        return maternal_consent

    @property
    def show_forms(self):
        show = self.request.GET.get('show', None)
        return True if show == 'forms' else False

    @property
    def subject_identifier(self):
        return self.context.get('subject_identifier')
