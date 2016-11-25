from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords, UrlMixin
from edc_base.model.validators import date_not_future
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import NO, YES
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_protocol.validators import date_not_before_study_start
from edc_visit_schedule.model_mixins import EnrollmentModelMixin

from .antenatal_enrollment_mixin import AntenatalEnrollmentMixin


class AntenatalEnrollment(AntenatalEnrollmentMixin, EnrollmentModelMixin, OffstudyMixin, CreateAppointmentsMixin,
                          RequiresConsentMixin, ExportTrackingFieldsMixin, UrlMixin, BaseUuidModel):

    weeks_base_field = 'ga_lmp_enrollment_wks'

    knows_lmp = models.CharField(
        verbose_name="Does the mother know the approximate date of the first day her last menstrual period?",
        choices=YES_NO,
        help_text='LMP',
        max_length=3)

    last_period_date = models.DateField(
        verbose_name="What is the approximate date of the first day of the mother's last menstrual period",
        validators=[
            date_not_before_study_start,
            date_not_future, ],
        null=True,
        blank=True,
        help_text='LMP')

    ga_lmp_enrollment_wks = models.IntegerField(
        verbose_name="GA by LMP at enrollment.",
        help_text=" (weeks of gestation at enrollment, LPM). Eligible if >16 and <36 weeks GA",
        null=True,
        blank=True,)

    ga_lmp_anc_wks = models.IntegerField(
        verbose_name="What is the mother's gestational age according to ANC records?",
        null=True,
        blank=True,
        help_text=" (weeks of gestation at enrollment, ANC)",)

    edd_by_lmp = models.DateField(
        verbose_name="Estimated date of delivery by lmp",
        validators=[
            date_not_before_study_start],
        null=True,
        blank=True,
        help_text="")

    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier, )

    def unenrolled_error_messages(self):
        """Returns a tuple (True, None) if mother is eligible otherwise
        (False, unenrolled_error_message) where error message is the reason enrollment failed."""
        unenrolled_error_message = []
        chronic_message = self.chronic_unenrolled_error_messages()
        unenrolled_error_message.append(chronic_message) if chronic_message else None
        if self.will_breastfeed == NO:
            unenrolled_error_message.append('will not breastfeed')
        if self.will_remain_onstudy == NO:
            unenrolled_error_message.append('won\'t remain in study')
        if self.will_get_arvs == NO:
            unenrolled_error_message.append('Will not get ARVs on this pregnancy.')
        if self.rapid_test_done == NO:
            unenrolled_error_message.append('rapid test not done')
        if self.ga_lmp_enrollment_wks and (self.ga_lmp_enrollment_wks < 16 or self.ga_lmp_enrollment_wks > 36):
            unenrolled_error_message.append('gestation not 16 to 36wks')
        if self.delivery and not self.delivery.keep_on_study:
            unenrolled_error_message.append('Hiv+ and not on ART for atleast 4 weeks.')
        if self.ultrasound and not self.ultrasound.pass_antenatal_enrollment:
            unenrolled_error_message.append('Pregnancy is not a singleton.')
        return unenrolled_error_message

    def chronic_unenrolled_error_messages(self):
        unenrolled_error_message = None
        if self.is_diabetic == YES:
            unenrolled_error_message = 'Diabetic'
        return unenrolled_error_message

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule.maternal_enrollment_step1'
