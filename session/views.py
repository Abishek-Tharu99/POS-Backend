from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import BillingSession
from decimal import Decimal
from datetime import datetime
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_session(request):
    
    #if request.user.is_anonymous:
     #   return Response({"error": "Unauthorized"}, status=401)

    active = BillingSession.objects.filter(
        user=request.user,
        is_active=True
    ).first()
    

    if active:
        return Response({
            "message": "Session already active",
            "session_id": active.session_id
        })

    session = BillingSession.objects.create(
        user=request.user
    )

    return Response({
        "message": "Session started",
        "session_id": session.session_id
    })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_session(request):

    session_id = request.data.get("session_id")
    
    if not session_id:
        return Response({"error": "session_id required"}, status=400)

    try:
        session = BillingSession.objects.get(
            session_id=session_id,
            user=request.user,
            is_active=True
        )
    except BillingSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)

    session.end_time = timezone.now()

    session.total_sales =  Decimal(str(request.data.get("total_sales", 0)))
    session.credit_sales =  Decimal(str(request.data.get("credit", 0)))
    session.card_sales =  Decimal(str(request.data.get("pos", 0)))
    session.fonepay_sales =  Decimal(str(request.data.get("fonepay", 0)))
    session.cash_sales = session.total_sales - (session.card_sales + session.fonepay_sales + session.credit_sales)

    session.is_active = False
    session.save()

    return Response({
        "message": "Session ended successfully",
        "session_id":session.session_id
    })

@api_view(['GET'])
def clear_sessions(request):

    BillingSession.objects.all().delete()

    return Response({
        "message": "All sessions deleted"
    })