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
    return Response(serializer.errors, status=400)
    print(serializer.errors)
    
    
    
# GET BY DATE
@api_view(['GET'])
def get_bill(request, date):
    try:
        bill = Summary.objects.get(date=date)
        serializer = BillSerializer(bill)
        return Response(serializer.data)
    except Summary.DoesNotExist:
        return Response({"error": "Not found"})