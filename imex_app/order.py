from django.shortcuts import render, get_object_or_404
from .models import Order
from django.contrib.auth.models import User
import secrets as ss
from rest_framework.response import Response
from rest_framework import status

def generate(x, y):
    gen = ss.SystemRandom()
    code = gen.randint(1*1000, 100*6990594598454)
    final = code*892289873473938
    return x+str(final)+y
@api_view(['POST'])
def order(request):
    if request.method == 'POST':
        client_name = request.data.get()
        agent_id = request.data.get('agent_id')
        Order.objects.create(client_name=client_name, agent_id=agent_id)
        return Response({'status': 'ordered'})

@api_view(['POST'])
def check_code(request):
    pass

@api_view(['POST'])
    def done(request):
    if request.method == 'POST':
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        client_number = request.data.get('client_number')
        agent_id = request.data.get('agent_id')
        agent = get_object_or_404(User, pk=agent_id)
        order.code=generate(agent.username, client_name)
        order.save()
#        this is where request will be sent by mail or sms
        Order.is_done=True;order.code_active=True
        order.save()
        return Response({"status": "Request sent")

