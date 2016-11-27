from django.core import serializers
from django.test.testcases import TestCase
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_registration.models import RegisteredSubject
from edc_sync.models import OutgoingTransaction

from td_maternal.models import SpecimenConsent


class TestMaternalSerializers(TestCase):

    def test_maternaleligibility_serializer(self):
        """ Creating maternaleligibility should creates outgoingtransaction """
        mommy.make_recipe('td_maternal.maternaleligibility')
        self.assertEqual(OutgoingTransaction.objects.filter(tx_name='td_maternal.maternaleligibility').count(), 1)

    def test_maternaleligibility_deserialize(self):
        """ Serialized maternaleligibility record should be able deserialized. """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        outgoing_transaction = OutgoingTransaction.objects.get(tx_name='td_maternal.maternaleligibility')
        deserialised_obj = self.deserialised_obj(maternal_eligibility, outgoing_transaction)
        self.assertEqual(maternal_eligibility.pk, deserialised_obj.object.pk)

    def create_specimen_consent(self, registered_subject):
        specimen_consent = mommy.make(
            SpecimenConsent,
            registered_subject=registered_subject,
            consent_datetime=get_utcnow(),
            may_store_samples=YES,
            is_literate=YES
        )
        return specimen_consent

    def deserialised_obj(self, model_obj, outgoing_tx):
        for deserialised_obj in serializers.deserialize(
                "json", outgoing_tx.aes_decrypt(outgoing_tx.tx), use_natural_foreign_keys=True, use_natural_primary_keys=True):
            return deserialised_obj

    def test_maternalconsent_serialize(self):
        """ Creating maternalconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        self.assertEqual(OutgoingTransaction.objects.filter(tx_name='td_maternal.maternalconsent').count(), 1)

    def test_maternalconsent_deserialize(self):
        """ Serialized maternalconsent record should be able deserialized. """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        outgoing_tx = OutgoingTransaction.objects.get(tx_name='td_maternal.maternalconsent')
        deserialised_obj = self.deserialised_obj(maternal_consent, outgoing_tx)
        self.assertEqual(maternal_consent.pk, deserialised_obj.object.pk)

    def test_specimen_consent_serialize(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        registered_subject = RegisteredSubject.objects.get(
            identity=maternal_consent.identity
        )
        self.create_specimen_consent(registered_subject)
        self.assertEqual(OutgoingTransaction.objects.filter(tx_name='td_maternal.specimenconsent').count(), 1)

    def test_speciman_consent_deserialize(self):
        """ Serialized specimenconsent record should be able deserialized. """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        registered_subject = RegisteredSubject.objects.get(
            identity=maternal_consent.identity
        )
        specimen_consent = self.create_specimen_consent(registered_subject)
        outgoing_tx = OutgoingTransaction.objects.get(tx_name='td_maternal.specimenconsent')
        deserialised_obj = self.deserialised_obj(specimen_consent, outgoing_tx)
        self.assertEqual(specimen_consent.pk, deserialised_obj.object.pk)

    def test_antenatal_enrollment(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=maternal_consent.subject_identifier)
        outgoing_tx = OutgoingTransaction.objects.filter(tx_name='td_maternal.antenatalenrollment')
        self.assertTrue(outgoing_tx)
        print(antenatal_enrollment.__dict__)
        deserialised_obj = self.deserialised_obj(antenatal_enrollment, outgoing_tx.first())
        self.assertEqual(antenatal_enrollment.pk, deserialised_obj.object.pk)
