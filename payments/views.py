from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.contrib.auth.models import User
from products.models import Order
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime

@login_required
def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'payments/pay.html')

    cart = Order.objects.filter(user = request.user).get(placed = "False")
    transaction = Transaction.objects.create(made_by=request.user, amount=cart.amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = {
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(request.user.id)),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('TXN_AMOUNT', str(transaction.amount)),
        # ('EMAIL', request.user.email),
        #('MOBILE_NO', '8696011111'),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/payments/callback/'),
        #('PAYMENT_MODE_ONLY', 'NO'),
    }

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params)
    #return HttpResponse(checksum)
    #return render(request, 'payments/pay.html')
    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payments/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        received_data = dict(request.POST)
        
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            #print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            #print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        if is_valid_checksum and received_data['RESPCODE'][0] == "01":
            txn = Transaction.objects.get(order_id = received_data["ORDERID"][0])
            txn.txn_id = received_data["TXNID"]
            user = txn.made_by
            cart = Order.objects.filter(user = user).get(placed = "False")
            cart.placed = "True"
            cart.order_time = datetime.now()
            txn.save()
            cart.transaction = txn
            cart.save()
            NewCart = Order.objects.create(user = user)
            NewCart.save()
            messages.success(request, f'Order Confirmed')
            return redirect('product-home')
        
        else:
            messages.warning(request, f'Payment Not Succesful. Order not placed.')
            return redirect('product-home')

        return JsonResponse(received_data)



