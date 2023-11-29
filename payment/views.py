import base64
from datetime import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django_daraja.mpesa.core import MpesaClient
from requests.auth import HTTPBasicAuth
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User

from KiLib.settings import MPESA_SHORTCODE, MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, MPESA_PASSKEY
from payment.models import LNMOnline
from payment.serializer import LNMOnlineSerializer
from store.models import Product

from basket.basket import Basket

from django.urls import reverse

# callback_url = request.build_absolute_url(reverse('callback'))
# callback_url = reverse('callback')
unformatted_time = datetime.now()
formatted_time = unformatted_time.strftime("%Y%m%d%H%M%S")

data_to_encode = MPESA_SHORTCODE + MPESA_PASSKEY + formatted_time
encoded_string_p = base64.b64encode(data_to_encode.encode())
decoded_password = encoded_string_p.decode('utf-8')

consumer_key = MPESA_CONSUMER_KEY
consumer_secret = MPESA_CONSUMER_SECRET
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
json_response = r.json()
my_access_token = json_response['access_token']


@login_required
def pay(request, id):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = int(total)
    product = get_object_or_404(Product, id=id)
    phone_number = 254743113141

    access_token = my_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": decoded_password,
        "Timestamp": formatted_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": total,
        "PartyA": phone_number,
        "PartyB": MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "http://127.0.0.1:8000/pay/lnm",
        "AccountReference": "12345678",
        "TransactionDesc": "Buy books",
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse(response)
    # return render(request, 'payment/pay.html', {'product': product})


class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer

    def create(self, request, *args, **kwargs):
        merchant_request_id = request.data['Body']['stkCallback']['MerchantRequestID']
        checkout_request_id = request.data['Body']['stkCallback']['CheckoutRequestID']
        result_code = request.data['Body']['stkCallback']['ResultCode']
        result_description = request.data['Body']['stkCallback']['ResultDesc']
        amount = request.data['Body']['stkCallback']['CallbackMetadata']['item'][0]['value']
        mpesa_receipt_number = request.data['Body']['stkCallback']['CallbackMetadata']['item'][1]['value']
        transaction_date = request.data['Body']['stkCallback']['CallbackMetadata']['item'][3]['value']
        phone_number = request.data['Body']['stkCallback']['CallbackMetadata']['item'][4]['value']

        from datetime import datetime
        str_transaction_date = str(transaction_date)
        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")

        from models import LNMOnline

        model = LNMOnline.objects.create(CheckoutRequestID=checkout_request_id, MerchantRequestID=merchant_request_id,
                                         ResultCode=result_code, ResultDesc=result_description, Amount=amount,
                                         MpesaReceiptNumber=mpesa_receipt_number, TransactionDate=transaction_datetime,
                                         PhoneNumber=phone_number
                                         )
        model.save()