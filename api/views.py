from rest_framework.decorators import api_view
from rest_framework.response import Response
from session.models import BillingSession
from .models import Summary
from .serializers import BillSerializer



    
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
def get_bill(request, session_id):   # 👈 take from URL, not query params

    all_sessions = BillingSession.objects.values_list(
        "session_id",
        flat=True
    )

    print("All sessions:", list(all_sessions))
    print(f"Requested session_id: {session_id}")
    try:
        print(f"Fetching bill for session_id: {session_id}")  # Debug log
        
        session = BillingSession.objects.get(session_id=session_id)
        print(session)  # Debug log to confirm session retrieval
        bill = Summary.objects.get(session=session)
        print(bill)  # Debug log to confirm bill retrieval

        serializer = BillSerializer(bill)
        print(serializer.data)  # Debug log to confirm serialization
        return Response(serializer.data)

    except BillingSession.DoesNotExist:
        print("Session not found")
        return Response({"error": "Session not found"}, status=404)

    except Summary.DoesNotExist:
        print("Bill not found")
        return Response({"error": "Bill not found"}, status=404)
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return Response({"error": "An unexpected error occurred"}, status=500)