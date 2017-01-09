"""
Solo Payments Manager
"""
import logging

from datetime import datetime

from django.db import models
from django.http import Http404

from rest_framework.exceptions import ValidationError

from plugs_payments.settings import plugs_payments_settings as settings
from plugs_payments import signals

LOGGER = logging.getLogger(__name__)

class IfThenPaymentManager(models.Manager):
    """
    IfThenPay Payment custom manager
    """

    def confirmation(self, data):
        """
        Payment confirmation callback
        http://www.yoursite.com/callback.php?chave=[CHAVE_ANTI_PHISHING]&entidad
        e=[ENTIDADE]&referencia=[REFERENCIA]&valor=[VALOR]&datahorapag=[DATA_HOR
        A_PAGAMENTO]&terminal=[TERMINAL]
        """
        self.data = data
        self._verify_phishing_key()
        mbpayment = self._get_mbpayment()
        mbpayment.mark_as_paid(**data)
        return {"message": "Payment Confirmation Received"}

    def _verify_phishing_key(self):
        """
        Uses key provided in the request to
        authenticate the payment platform
        """
        if settings['ANTI_PHISHING_KEY'] != self.data.get('chave'):
            message = 'Anti Phishing Key is Missing or Incorrect.'
            signals.suspicious_ifthen_payment_received.send(sender=self, data=self.data)
            raise ValidationError(message)

    def _get_mbpayment(self):
        """
        Get object or 404
        """
        entity = self.data.get('entidade')
        reference = self.data.get('referencia')
        value = self.data.get('valor')
        try:
            return self.model.objects.get(
                is_paid=False,
                entity=entity,
                reference=reference,
                value=value)
        except self.model.DoesNotExist:
            signals.invalid_ifthen_payment_received.send(sender=self, data=self.data)
            raise Http404
