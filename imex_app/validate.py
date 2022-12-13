import secrets as ss
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import timedelta as td
from .models import Profile, Code
from django.contrib.auth.models import User
from django.core.mail import send_mail

DELTA = td(hours=+4)

def generate_code():
    gen = ss.SystemRandom()
    code = gen.randint(1*1000, 5000)
    return code

@api_view(["POST"])
def generate(request):
    email = request.data.get("email")
    user =  User.objects.filter(email=email)
    if user:
        code = Code()
        code.user = user
        code.unique_code = str(generate_code())
        code.expiring_date = DELTA + code.date_generated
        code.save()
        send_mail("EMAIL ACCOUNT VERIFICATION CODE CONFIRMATION", f'Use the below code to verify your email address \n\r {code.unique_code}', fail_silently=True)
        return Response({"status": "ok"})
    return Response({"status": "error"}, status=status.HTTP_404_NOT_FOUND)
@api_view(["POST"])
def validate_code(request):
    code_number = request.data.get("code")
    code = Code.objects.filter(unique_code=code_number)
    if code:
        if code.date_generated < code.expiring_date:
            user = Profile.objects.filter(user_id=code.user_id)
            user.is_validated=True
            user.save()
            return Response({"status": "ok"})
        return Response({"status": "Code expired"}, status=status.HTTP_423_LOCKED)
    return Response({"status": "Invalid code"}	, status=status.HTTP_417_EXPECTATION_FAILED)

@api_view(["POST"])
def reset(request):
    code_number = request.data.get("code")
    code = Code.objects.filter(unique_code=code_number)
    if code:
        if code.date_generated < code.expiring_date:
            return Response({"status": "ok"})
        return Response({"status": "Code expired"}, status=status.HTTP_423_LOCKED)
    return Response({"status": "Invalid code"}	, status=status.HTTP_417_EXPECTATION_FAILED)

