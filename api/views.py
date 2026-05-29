from rest_framework.decorators import api_view
from rest_framework.response import Response

from session.models import BillingSession
from .models import Summary
from .serializers import BillSerializer


# # SAVE DATA
# @api_view(['POST'])
# def save_bill(request):
#     serializer = BillSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Saved"})
    
#     print(serializer.errors)
#     return Response(serializer.errors, status=400)
    
    
@api_view(['POST'])
def save_bill(request):
    # session_id = request.data.get("session_id")

    # session = BillingSession.objects.get(session_id=session_id)

    session = BillingSession.objects.get(session_id=request.data.get("session_id"))

    obj, created = Summary.objects.update_or_create(
        session=session,
        defaults={
            "opening_balance": request.data["opening_balance"],
            "cash_sales": request.data["cash_sales"],
            "pos": request.data["pos"],
            "fonepay": request.data["fonepay"],
            "credit": request.data["credit"],
            "total_sales": request.data["total_sales"],
            "excess_less": request.data["excess_less"],
            "expenses": request.data["expenses"],
            "deposited_bank": request.data["deposited_bank"],
            "given_other": request.data["given_other"],
            "closing_balance": request.data["closing_balance"],
        }
    )

    return Response({"message": "Saved", "created": created})


# GET BY DATE
@api_view(['GET'])
def get_bill(request):
    session_id = request.query_params.get("session_id")

    try:
        session = BillingSession.objects.get(session_id=session_id)
        bill = Summary.objects.get(session=session)

        serializer = BillSerializer(bill)
        return Response(serializer.data)

    except Summary.DoesNotExist:
        return Response({"error": "Not found"}, status=404)