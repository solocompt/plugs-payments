"""
Payments Views
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from plugs_payments import models

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def confirmation(request):
    """
    Callback to be used by the payments platform
    """
    reason = models.IfThenPayment.objects.confirmation(request.GET)
    return Response(data=reason)    
