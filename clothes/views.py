from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
# from django_daraja.mpesa.core import MpesaClient
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

# Create your views here.

def getAccessToken(request):
    consumer_key = 'TpCIJnUaLQLs1XLhMySKCEfgtPSWkZNU'
    consumer_secret = '1booBmyCQ3NHxT3Y'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)    

def lipa_na_mpesa_online(request):
    order = Client.objects.get(paid=False)
    # remove "+" from customer's phone number
    mobile = order.phone_number
    phone = str(order.phone_number).translate({ord('+'): None})

    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline", #CustomerBuyGoodsOnline
        "Amount": int(order.amount), 
        "PartyA": int(phone),  # replace with your phone number to get stk push...convert phone number to integer
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": int(phone),  # replace with your phone number to get stk push .translate({ord('+'): None})
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Laundry services",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    order = Client.objects.get(phone_number=mobile)
    order.paid=True
    order.save()
    
    return redirect('home') 




def home(request):

    clients_list = Client.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(clients_list, 10)

    try:
        clothes = paginator.page(page)
    except PageNotAnInteger:
        clothes = paginator.page(1)
    except EmptyPage:
        clothes = paginator.page(paginator.num_pages)



    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form':form,
        'clothes':clothes

    }  
    return render(request, 'home.html', context)      

def clients(request):
    # clothes = Client.objects.all().order_by('-id')
    clients_list = Client.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(clients_list, 10)

    try:
        clothes = paginator.page(page)
    except PageNotAnInteger:
        clothes = paginator.page(1)
    except EmptyPage:
        clothes = paginator.page(paginator.num_pages)

    context = {
        'clothes':clothes
    }
    return render(request, 'clienst.html', context)      

def editClient(request, id):
    client = get_object_or_404(Client, id=id)

    form = ClientUpdateForm(instance=client)
    if request.method == 'POST':
        form = ClientUpdateForm(request.POST,instance=client)
        if form.is_valid():
            form.save()
            return redirect('lipa_na_mpesa')

    context = {
        'form':form,
        'client':client

    }       

    return render(request, 'update.html', context)      

def clientDelete(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return redirect('home')



# from django.http import HttpResponse, JsonResponse
# import requests
# from requests.auth import HTTPBasicAuth
# import json
# from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
# from django.views.decorators.csrf import csrf_exempt
# # from .models import MpesaPayment
# # def getAccessToken(request):
# #     consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
# #     consumer_secret = '2nHEyWSD4VjpNh2g'
# #     api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
# #     r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
# #     mpesa_access_token = json.loads(r.text)
# #     validated_mpesa_access_token = mpesa_access_token['access_token']
# #     return HttpResponse(validated_mpesa_access_token)
# # def lipa_na_mpesa_online(request):
# #     access_token = MpesaAccessToken.validated_mpesa_access_token
# #     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
# #     headers = {"Authorization": "Bearer %s" % access_token}
# #     request = {
# #         "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
# #         "Password": LipanaMpesaPpassword.decode_password,
# #         "Timestamp": LipanaMpesaPpassword.lipa_time,
# #         "TransactionType": "CustomerPayBillOnline",
# #         "Amount": 1,
# #         "PartyA": 254728851119,  # replace with your phone number to get stk push
# #         "PartyB": LipanaMpesaPpassword.Business_short_code,
# #         "PhoneNumber": 254728851119,  # replace with your phone number to get stk push
# #         "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
# #         "AccountReference": "Henry",
# #         "TransactionDesc": "Testing stk push"
# #     }
# #     response = requests.post(api_url, json=request, headers=headers)
# #     return HttpResponse('success')

# @csrf_exempt
# def register_urls(request):
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
#                "ResponseType": "Completed",
#                "ConfirmationURL": "http://127.0.0.1:8000/payment/confirmation",
#                "ValidationURL": "http://127.0.0.1:8000/payment/validation"}
#     response = requests.post(api_url, json=options, headers=headers)
#     return HttpResponse(response.text)


# @csrf_exempt
# def call_back(request):
#     pass

# @csrf_exempt
# def validation(request):
#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }
#     return JsonResponse(dict(context))

# @csrf_exempt
# def confirmation(request):
#     mpesa_body =request.body.decode('utf-8')
#     mpesa_payment = json.loads(mpesa_body)
#     payment = MpesaPayment(
#         first_name=mpesa_payment['FirstName'],
#         last_name=mpesa_payment['LastName'],
#         middle_name=mpesa_payment['MiddleName'],
#         description=mpesa_payment['TransID'],
#         phone_number=mpesa_payment['MSISDN'],
#         amount=mpesa_payment['TransAmount'],
#         reference=mpesa_payment['BillRefNumber'],
#         organization_balance=mpesa_payment['OrgAccountBalance'],
#         type=mpesa_payment['TransactionType'],
#     )
#     payment.save()
#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }
#     return JsonResponse(dict(context))                