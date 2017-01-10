"""
MB Payment
"""
import logging
from random import randint
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models

from plugs_core import mixins

from plugs_payments.settings import plugs_payments_settings as settings
from plugs_payments.managers import IfThenPaymentManager
from plugs_payments.signals import valid_ifthen_payment_received
from plugs_payments import fields

LOGGER = logging.getLogger(__name__)

class IfThenPayment(mixins.Timestampable, models.Model):
    """
    IfThenPay Payment model
    """
    is_paid = models.BooleanField(default=False)
    entity = fields.EntityField()
    reference = fields.ReferenceField()
    value = models.DecimalField(null=False, max_digits=20, decimal_places=2)
    payment_date = models.DateTimeField(null=True, blank=True)
    terminal = models.CharField(null=True, blank=True, max_length=40)
    objects = IfThenPaymentManager()

    def mark_as_paid(self, **data):
        """
        Mark payment as paid
        """
        self.is_paid = True
        # why is this a list?
        self.terminal = data.get('terminal')[0]
        self.payment_date = self._format_payment_date(data.get('datahorapag')[0])
        self.save()
        valid_ifthen_payment_received.send(sender=self)

    def generate_payment_details(self):
        self.bookkeeper = self._generate_bookkeeper()
        self.entity = settings['ENTITY']
        self.reference = self._generate_reference()
        
    def save(self, *args, **kwargs):
        """
        Overrides model save method
        """
        if not self.pk:
            counter = 0
            while(True):
                # entity, reference and value must be unique together
                # if a record exists with the same triad, loop and
                # generate new payment details
                # incremente and log counter, in the future
                # can be used to set the max number of retries before
                # giving up
                try:
                    self.generate_payment_details()
                    data = {
                        'entity': self.entity,
                        'reference': self.reference,
                        'value': self.value
                    }
                    self.__class__.objects.get(**data)
                    counter += 1
                except self.DoesNotExist:
                    # if the triad does not exist in the database
                    # proceed
                    break
                message = 'Retrying payments details generation {0}'
                LOGGER.warning(message.format(counter))
        super(IfThenPayment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.reference)

    def _format_payment_date(self, payment_date):
        try:
            # deal with payment_date
            from_format = "%d-%m-%Y %H:%M:%S"
            to_format = "%Y-%m-%d %H:%M:%S"
            payment_date = datetime.strptime(payment_date, from_format).strftime(to_format)
        except (TypeError, ValueError):
            message = 'Payment date invalid. Date {0}'
            LOGGER.warning(message.format(payment_date))
        return payment_date
    
    def _check_digits(self, integrity):
        """
        Integrity string is used to calculate
        the check digits using the provided algorithm

        Multiply each digit of the integrity string
        with a corresponding value in the lookup list

        Sum all the multiplications and subtract
        the modulus of summatory with 97 to the number 98
        """
        multipliers = [51, 73, 17, 89, 38, 62, 45, 53, 15, 50, 5, 49, 34, 81, 76, 27, 90, 9, 30, 3]
        # verify input len equal to multipliers
        if len(integrity) != len(multipliers):
            raise Http404
        summatory = 0
        for index, digit in enumerate(integrity):
            summatory += int(digit) * multipliers[index]
        result = 98 - (summatory % 97)
        return '{0:02d}'.format(result)
    
    def _format_value(self):
        """
        The value must use 8 digits, we need to
        multiply the decimal by 100 to shift the
        decimal places, convert to int and then
        padd the string with zeros if needed
        """
        try:
            inted_value = int(self.value * 100)
        except TypeError:
            raise
        return '{0:08d}'.format(inted_value)

    def _generate_bookkeeper(self):
        """
        Generate a random int to
        be used as a unique id when
        generating references
        """
        return randint(0, 9999)
    
    def _generate_integrity_string(self):
        """
        String that is gonna be used
        to compute check digits
        """
        return '{0}{1}{2}{3}'.format(
            settings['ENTITY'],
            settings['SUBENTITY'],
            '{0:04d}'.format(self.bookkeeper),
            self._format_value()
        )
    
    def _generate_reference(self):
        """
        Generate a reference using the ifthenpay 
        payment platform algorithm
        """
        integrity = self._generate_integrity_string()
        check_digits = self._check_digits(integrity)
        subentity = str(settings['SUBENTITY'])
        return '{0}{1}{2}'.format(subentity, '{0:04d}'.format(self.bookkeeper), check_digits)

    
    # pylint: disable=R0903
    class Meta:
        """
        Providing verbose names is recommended if
        we want to use i18n in admin site
        """
        unique_together = ('entity', 'reference', 'value')
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
