from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_death_report.model_mixins import DeathReportModelMixin

from .maternal_visit import MaternalVisit
from edc_base.model.models.url_mixin import UrlMixin

from ..managers import MaternalDeathReportManager


class MaternalDeathReport(DeathReportModelMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user on the mother's death. """

    ADMIN_SITE_NAME = 'td_maternal_admin'

    maternal_visit = models.OneToOneField(MaternalVisit)

    objects = MaternalDeathReportManager()

    history = HistoricalRecords()

    def natural_key(self):
        return self.maternal_visit.natural_key()
    natural_key.dependencies = ['td_maternal.maternalvisit']

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Death Report"
