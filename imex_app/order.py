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
        Order.objects.create(client_id=client_id, agent_id=agent_id)
        return Response({'status': 'ordered'})

@api_view(['POST'])
def check_code(request):
    order_id = request.data.get('order_id')
    code = request.data.get("code")
    order = get_object_or_404(Order, pk=order_id)
    if Order.objects.filter(code=code).exists():
        if order.is_done and order.is_active:
            return Response({"status": "can review"}, status=status.HTTP_100_CONTINUE)
        return Response({"status": "cannot review"}, status=status.HTTP_103_EARLY_HINTS)
    return Response({"status": "The code does not exist"}, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

@api_view(['POST'])
def done(request):
    if request.method == 'POST':
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        client_name = request.data.get('client_name')
        agent_id = request.data.get('agent_id')
        client = get_object_or_404(User, username=client_name)
        order.code=generate(agent.username, client_name)
        order.save()
    #        this is where request will be sent by mail or sms
        send_mail('Offiis review request', f'Please use the below code to review {agent.username}. \r' + str(order.code), [client.email], fail_silently=True)
        order.is_done=True;order.code_active=True
        order.save()
    return Response({"status": "Request sent"})

