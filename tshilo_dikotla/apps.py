import os

from django.utils import timezone

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings

from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_consent.apps import AppConfig as EdcConsentAppConfigParent
from edc_label.apps import AppConfig as EdcLabelConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent
from edc_registration.apps import AppConfig as EdcRegistrationAppConfigParent
from edc_sync.apps import AppConfig as EdcSyncAppConfigParent
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_timepoint.timepoint import Timepoint

from edc_sync.constants import SERVER


class AppConfig(DjangoAppConfig):
    name = 'tshilo_dikotla'
    verbose_name = 'Tshilo Dikotla'

    def ready(self):
        pass


class EdcRegistrationAppConfig(EdcRegistrationAppConfigParent):
    app_label = 'td_registration'


class EdcProtocolAppConfig(EdcProtocolAppConfigParent):
    protocol = 'BHP085'
    protocol_number = '085'
    protocol_name = 'Tshilo Dikotla'
    protocol_title = ''
    study_start_datetime = timezone.datetime(2016, 4, 1, 0, 0, 0)
    study_end_datetime = timezone.datetime(2018, 12, 1, 0, 0, 0)
    subject_types = ['maternal', 'infant']
    enrollment_caps = {'td_maternal.antenatalenrollment': ('maternal', -1)}
#     max_subjects = {'maternal': 3000, 'infant': 3000}


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    institution = 'Botswana Harvard AIDS Institute Partnership'
    project_name = 'Tshilo Dikotla'


class EdcConsentAppConfig(EdcConsentAppConfigParent):
    consent_type_setup = [
        {'app_label': 'td_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': timezone.datetime(2016, 4, 1, 0, 0, 0),
         'end_datetime': timezone.datetime(2016, 12, 1, 0, 0, 0),
         'version': '1'}
    ]


class EdcTimepointAppConfig(EdcTimepointAppConfigParent):
    timepoints = [
        Timepoint(
            model='td_appointment.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='CLOSED'
        )
    ]


class EdcLabelAppConfig(EdcLabelConfigParent):
    default_cups_server_ip = '10.113.201.114'
    default_printer_label = 'leslie_testing'
    default_template_file = os.path.join(settings.STATIC_ROOT, 'tshilo_dikotla', 'label_templates', 'aliquot.lbl')
    default_label_identifier_name = ''


class EdcSyncAppConfig(EdcSyncAppConfigParent):
    edc_sync_files_using = True
    role = SERVER
