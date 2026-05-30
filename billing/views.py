from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item,Bill,BillItem,Payment
from .serializers import ItemSerializer
from datetime import datetime
import nepali_datetime
from django.db import transaction
from customers.models import Customer
from .models import BillSequence
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bill_no(request):
    
    bill_type = request.GET.get("type", "SI")
    
    with transaction.atomic():
        seq, created = BillSequence.objects.select_for_update().get_or_create(
            user=request.user,
            bill_type=bill_type,
            defaults={"last_no": 0}
        )
        
        seq.last_no += 1
        seq.save()
        bill_no = f"{bill_type}-{seq.last_no:06d}"
        # last_bill = (
        #     Bill.objects.select_for_update().filter(
        #         bill_no__startswith=bill_type,
        #         user=request.user   # 🔥 ADD THIS
        # ).order_by('-id').first()
        # )

        # if last_bill:
        #     last_no = int(last_bill.bill_no.split('-')[-1])
        #     bill_no = f"{bill_type}-{last_no + 1:06d}"
        # else:
        #     bill_no = f"{bill_type}-000001"

    return Response({"bill_no": bill_no})


@api_view(['GET'])
def get_items(request):
    query = request.GET.get('search', '')

    items = Item.objects.filter(
        name__icontains=query
    ) | Item.objects.filter(
        code__icontains=query
    )

    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_bill(request):
    
    data = request.data
    
    bill_type = data.get("billType", "SI")
    customer_name = data.get("customer_name", "")
    customer_no = data.get("customer_no", "")
    customer_pan = data.get("customer_pan", "")
    customer_addr = data.get("customer_addr", "")
    print(data)
 
    with transaction.atomic():
        
        seq = BillSequence.objects.select_for_update().get(
            user=request.user,
            bill_type=bill_type
        )

        bill_no = f"{bill_type}-{seq.last_no:06d}"
        
    
    print("all good till here")
    
    total = 0

    for item in data.get("items", []):
        price = float(item.get("price", 0))
        qty = int(item.get("qty", 0))
        total += price * qty
    
    taxableAmount = total / 1.13
    Vat = total - taxableAmount
    tender = sum(float(p.get("amount", 0)) for p in data.get("payments", []))
    change = max(tender - total, 0)
    discount = float(data.get("discount", 0))
    netAmount = (taxableAmount - discount) + Vat
    
    print("calculation done")
    
    # ✅ Dates
    now = datetime.now()
    date_en = now.date()
    time = now.time()

    date_np = nepali_datetime.date.from_datetime_date(date_en)

    try:
    # ✅ Create Bill
        bill = Bill.objects.create(
            user=request.user,
            bill_no=bill_no,

            date_en=date_en,
            date_np=str(date_np),
            time=time,
            customer_name=customer_name,
            customer_no=customer_no,
            customer_pan=customer_pan,
            customer_addr=customer_addr,

            total_amount=total,   # ✅ map correctly
            discount=discount,
            vat=Vat,
            net_amount=netAmount,       # ✅ map correctly

            tender=tender,
            change=change,
        )
    except Exception as e:
        print("Error creating bill:", e)
        return Response({"error": "Failed to create bill"}, status=500)
    
        # ✅ Save Items
    print("bill created, now saving items and payments")
    
    for item in data.get("items", []):
        code = item.get("code", "")
        name = item.get("name", "")
        price = float(item.get("price", 0))
        qty = int(item.get("qty", 0))
        total = price * qty

        BillItem.objects.create(
            bill=bill,
            code=code,
            name=name,
            price=price,
            qty=qty,
            total=total
        )
    print("items saved, now saving payments")
    
    # ✅ Save Payments
    for p in data.get("payments", []):
        Payment.objects.create(
            bill=bill,
            method=p.get("method"),
            amount=p.get("amount", 0),
        )
    print("payments saved")

    return Response({
        "status": "success",
        "bill_no": bill.bill_no
    })
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_bills(request):
    bills = Bill.objects.filter(
        user=request.user
    ).order_by('-date_en', '-time')
    
    data = [
        {
            "bill_no": b.bill_no,
            "date": b.date_en,
            "time": b.time.strftime("%H:%M:%S"),
            "total": b.net_amount
        }
        for b in bills
    ]

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bill_details(request, bill_no):
    try:
        bill = Bill.objects.get(
            bill_no=bill_no,
            user=request.user   # 🔥 ADD THIS
        )

        items = BillItem.objects.filter(bill=bill)
        payments = Payment.objects.filter(bill=bill)

        items_data = [
            {
                "code": i.code,
                "name": i.name,
                "price": i.price,
                "qty": i.qty,
                "total": i.total
            }
            for i in items
        ]

        payments_data = [
            {
                "method": p.method,
                "amount": p.amount
            }
            for p in payments
        ]

        return Response({
            "bill_no": bill.bill_no,
            "date_en": bill.date_en,
            "date_np": bill.date_np,
            "time": bill.time,
            "customer_name": bill.customer_name,
            "customer_no": bill.customer_no,
            "customer_pan": bill.customer_pan,
            "customer_addr": bill.customer_addr,
            

            # ✅ totals (IMPORTANT)
            "total_amount": bill.total_amount,
            "discount": bill.discount,
            "vat": bill.vat,
            "net_amount": bill.net_amount,
            "tender": bill.tender,
            "change": bill.change,

            # ✅ cart
            "items": items_data,

            # ✅ payments
            "payments": payments_data
        })

    except Bill.DoesNotExist:
        return Response({"error": "Bill not found"}, status=404)