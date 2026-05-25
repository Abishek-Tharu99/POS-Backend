from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer
from .Serializers import CustomerSerializer

# Add customer
@api_view(['POST'])
def add_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
       
        return Response(serializer.errors, status=400)

# Get + filter customers
@api_view(['GET'])
def get_customers(request):
    customer = request.GET.get('customer','')  
    
    if customer:
        customers = Customer.objects.filter(name__icontains=customer)
    else:
        customers = Customer.objects.all()

    
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)