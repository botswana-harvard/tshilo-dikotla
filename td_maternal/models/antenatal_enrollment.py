from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsOnEligibleMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords, UrlMixin
from edc_base.model.validators import date_not_future
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.choices import POS_NEG_UNTESTED_REFUSAL, YES_NO_NA, POS_NEG, YES_NO
from edc_constants.constants import NO
from edc_offstudy.model_mixins import OffstudyMixin
from edc_protocol.validators import date_not_before_study_start
from edc_visit_schedule.model_mixins import EnrollmentModelMixin

from ..enrollment_helper import EnrollmentHelper
from ..managers import EnrollmentManager

from dateutil.relativedelta import relativedelta
from td_maternal.models.maternal_visit import MaternalVisit
from django.core.exceptions import MultipleObjectsReturned
from td_maternal.enrollment_helper import EnrollmentError


class AntenatalEnrollment(EnrollmentModelMixin, OffstudyMixin, CreateAppointmentsOnEligibleMixin,
                          RequiresConsentMixin, UrlMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'td_maternal_admin'

    is_diabetic = models.CharField(
        verbose_name='Are you diabetic?',
        choices=YES_NO,
        help_text='INELIGIBLE if YES',
        max_length=3)

    will_breastfeed = models.CharField(
        verbose_name='Are you willing to breast-feed your child for 6 months?',
        choices=YES_NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    will_remain_onstudy = models.CharField(
        verbose_name="Are you willing to remain in the study for the child's first three year of life",
        choices=YES_NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    current_hiv_status = models.CharField(
        verbose_name="What is your current HIV status?",
        choices=POS_NEG_UNTESTED_REFUSAL,
        max_length=30,
        help_text=("if POS or NEG, ask for documentation."))

    evidence_hiv_status = models.CharField(
        verbose_name="(Interviewer) Have you seen evidence of the HIV result?",
        max_length=15,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        help_text=("evidence = clinic and/or IDCC records. check regimes/drugs. If NO, more criteria required."))

    week32_test = models.CharField(
        verbose_name="Have you tested for HIV before or during this pregnancy?",
        choices=YES_NO,
        default=NO,
        max_length=3)

    week32_test_date = models.DateField(
        verbose_name="Date of HIV Test",
        null=True,
        blank=True)

    week32_result = models.CharField(
        verbose_name="What was your result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

    evidence_32wk_hiv_status = models.CharField(
        verbose_name="(Interviewer) Have you seen evidence of the result from HIV test on or before this pregnancy?",
        max_length=15,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        help_text=("evidence = clinic and/or IDCC records. check regimes/drugs."))

    will_get_arvs = models.CharField(
        verbose_name="(Interviewer) If HIV+ve, do records show that participant is taking, is prescribed,"
                     "or will be prescribed ARVs (if newly diagnosed) during pregnancy?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        max_length=15,
        help_text=("If found POS by RAPID TEST. Then answer YES, can take them OFF STUDY at birth visit if there were"
                   " not on therapy for atleast 4 weeks."))

    rapid_test_done = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        max_length=15,
        help_text=(
            'Remember, rapid test is for NEG, UNTESTED, UNKNOWN and Don\'t want to answer.'))

    rapid_test_date = models.DateField(
        verbose_name="Date of rapid test",
        null=True,
        validators=[
            date_not_before_study_start,
            date_not_future],
        blank=True)

    rapid_test_result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

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

    enrollment_hiv_status = models.CharField(
        max_length=15,
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    date_at_32wks = models.DateField(
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    pending_ultrasound = models.BooleanField(
        editable=False,
        help_text='Auto-filled by enrollment helper')

    enrollment_ga = models.IntegerField(
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    enrollment_ga_method = models.CharField(
        max_length=15,
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    edd = models.DateField(
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    edd_method = models.CharField(
        max_length=15,
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    unenrolled = models.TextField(
        verbose_name="Reason not enrolled",
        max_length=350,
        null=True,
        editable=False)

    objects = EnrollmentManager()

    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    def save(self, *args, **kwargs):
        enrollment_helper = EnrollmentHelper(self)
        self.is_eligible = enrollment_helper.is_eligible
        try:
            self.date_at_32wks = (enrollment_helper.edd.edd - relativedelta(weeks=6)).date()
        except TypeError:
            self.date_at_32wks = None
        try:
            self.edd_by_lmp = enrollment_helper.lmp.edd.date()
        except AttributeError:
            self.edd_by_lmp = None
        self.enrollment_hiv_status = enrollment_helper.enrollment_result.result
        try:
            self.ga_lmp_enrollment_wks = enrollment_helper.lmp.ga.weeks
        except AttributeError:
            self.ga_lmp_enrollment_wks = None
        self.pending_ultrasound = enrollment_helper.ga_pending
        self.enrollment_ga = enrollment_helper.ga.weeks
        self.enrollment_ga_method = enrollment_helper.ga.method
        self.edd = enrollment_helper.edd.edd
        self.edd_method = enrollment_helper.edd.method
        self.unenrolled = enrollment_helper.messages.as_string()
        error_msg = (
            'Blocking attempt to change eligibility from \'eligible\' to \'not eligible\' for subject '
            'who has already attended scheduled visits.')
        if not self.is_eligible:
            try:
                MaternalVisit.objects.get(appointment__subject_identifier=self.subject_identifier)
                raise EnrollmentError(error_msg)
            except MultipleObjectsReturned:
                raise EnrollmentError(error_msg)
            except MaternalVisit.DoesNotExist:
                pass
        super(AntenatalEnrollment, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.subject_identifier, )

    @property
    def reasons_not_eligible(self):
        return self.unenrolled

    @property
    def ga_pending(self):
        return self.pending_ultrasound

    @property
    def ga_by_lmp(self):
        return self.ga_lmp_enrollment_wks

    @property
    def error_messages(self):
        return self.unenrolled

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule.maternal_enrollment_step1'
