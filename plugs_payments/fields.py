"""
Plugs Payments Fields
"""

from django.db import models

from plugs_core.validators import NumberOfDigitsValidator

class ReferenceField(models.PositiveIntegerField):
    """
    Custom model field that represent a payment reference
    """

    default_validators = [NumberOfDigitsValidator(9)]
    description = "A payment reference"

class EntityField(models.PositiveIntegerField):
    """
    Custom model field that represents an entity
    """

    default_validators = [NumberOfDigitsValidator(5)]
    description = "A payment entity"
