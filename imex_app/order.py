from django.shortcuts import render, get_object_or_404
from .models import Order
from django.contrib.auth.models import User
import secrets as ss
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.decorators import api_view

def generate(x, y):
    gen = ss.SystemRandom()
    code = gen.randint(1*1000, 100*6990594598454)
    final = code*892289873473938
    return x+str(final)+y
@api_view(['POST'])
def order(request):
    if request.method == 'POST':
        client_id = request.data.get("client_id")
        agent_id = request.data.get('agent_id')
        client = get_object_or_404(User, pk=client_id)
        agent = get_object_or_404(User, pk=agent_id)
        order_name = client.username + ' ' + agent.username
        if Order.objects.filter(order_name=order_name).exists():
            return Response({"status": "Already exists"}, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
        Order.objects.create(order_name=order_name, client_id=client_id, agent_id=agent_id)
        return Response({'status': 'ordered'})

@api_view(['POST'])
def check_code(request):
    # Again instead of sending both code and order_id, we are sending only the code
    # the code is going to be used to query the order to ensure simplicity
    code = request.data.get("code")
    order = get_object_or_404(Order, code=code)
    print(code)
    print(order.code_active)
    # We may not need this check if we are already able to query the order using the code
    # There is no such field in the order model as is_active we only have code_active
    if Order.objects.filter(code=code).exists():
        if order.is_done and order.code_active:
            return Response({"status": "can review"}, status=status.HTTP_100_CONTINUE)
        return Response({"status": "cannot review"},status=status.HTTP_103_EARLY_HINTS)
    return Response({"status": "The code does not exist"}, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

@api_view(['POST'])
def done(request):
    if request.method == 'POST':
        # Instead of sending client name from frontend, we will send only order id
        # with the order id we can get client and agent(all details about the order)
        # This ensures simplisity and avoids redundancy
        #Also notice that there is no name field in user table
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        order.code=generate(order.agent.username, order.client.username)
        order.save()
    #this is where request will be sent by mail or sms
        send_mail('Offiis review request', f'Please use the below code to review {order.agent.username}. \r' + str(order.code), [order.client.email], fail_silently=True)
        order.is_done=True;order.code_active=True
        order.save()
    return Response({"status": "Request sent"})

