from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Summary
from .serializers import BillSerializer


# SAVE DATA
@api_view(['POST'])
def save_bill(request):
    serializer = BillSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Saved"})
    
    print(serializer.errors)
    return Response(serializer.errors, status=400)
    
    
    
    
# GET BY DATE
@api_view(['GET'])
def get_bill(request):
    try:
        bill = Summary.objects.get(session_id=request.session_id)
        serializer = BillSerializer(bill)
        return Response(serializer.data)
    except Summary.DoesNotExist:
        return Response({"error": "Not found"})