import os

from django.utils import timezone

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings

from edc_appointment.apps import AppConfig as EdcAppointmentAppConfigParent
from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_consent.apps import AppConfig as EdcConsentAppConfigParent
from edc_consent.consent_config import ConsentConfig
from edc_label.apps import AppConfig as EdcLabelConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent
from edc_registration.apps import AppConfig as EdcRegistrationAppConfigParent
from edc_sync.apps import AppConfig as EdcSyncAppConfigParent
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_timepoint.timepoint import Timepoint
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent

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
    enrollment_caps = {'td_maternal.antenatalenrollment': ('maternal', -1),
                       'td_infant.infant_birth': ('infant', -1)}
#     max_subjects = {'maternal': 3000, 'infant': 3000}


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    institution = 'Botswana Harvard AIDS Institute Partnership'
    project_name = 'Tshilo Dikotla'


class EdcConsentAppConfig(EdcConsentAppConfigParent):
    consent_configs = [
        ConsentConfig(
            'td_maternal.maternalconsent',
            start=timezone.datetime(2016, 4, 1, 0, 0, 0),
            end=timezone.datetime(2018, 12, 1, 0, 0, 0),
            version='1',
            age_is_adult=18,
            age_max=64,
            gender=['F']),
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


class EdcAppointmentAppConfig(EdcAppointmentAppConfigParent):
    app_label = 'td_appointment'


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    visit_models = {'td_maternal': ('maternal_visit', 'td_maternal.maternalvisit'),
                    'td_infant': ('infant_visit', 'td_infant.infantvisit')}
