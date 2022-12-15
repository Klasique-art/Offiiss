import secrets as ss
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import timedelta as td
from .models import Profile, Code
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import datetime
import pytz


# specifying the time delta for the time interval

DELTA = td(hours=1)

def generate_code():
    gen = ss.SystemRandom()
    code = gen.randint(1*1000, 5000)
    return code

@api_view(["POST"])
def generate(request):
    email = request.data.get("email")
    user =  User.objects.filter(email=email)
    if user:
        try:
            code = Code()
            code.user = user[0]
            code.unique_code = str(generate_code())
            code.expiring_date = DELTA + code.date_generated
            code.save()

            send_mail("EMAIL ACCOUNT VERIFICATION CONFIRMATION CODE", f'Use the below code to verify your email address \n\r {code.unique_code} \r This code will expire in an hour time.', 'accountverification@offiiss.com', [email], fail_silently=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"status": "ok"})
    return Response({"status": "error"}, status=status.HTTP_404_NOT_FOUND)
@api_view(["POST"])
def validate_code(request):
    code_number = request.data.get("code")
    code = Code.objects.filter(unique_code=code_number)
    if code:
        if datetime.now(tz=pytz.utc) < code.expiring_date:
            user = Profile.objects.filter(user_id=code.user_id)[0]
 
            user.is_validated=True
            user.save()
            send_mail('Offiss Welcome message', 'Hello {user.user.first_name}, Your offiiss account has been validated', 'offiissapp@offiiss.com',  [], fail_silently=True)
            return Response({"status": "ok"})
        return Response({"status": "Code expired"}, status=status.HTTP_423_LOCKED)
    return Response({"status": "Invalid code"}	, status=status.HTTP_417_EXPECTATION_FAILED)

@api_view(["POST"])
def reset(request):
    try:
        code_number = request.data.get("code")
        code = Code.objects.filter(unique_code=code_number)
        if code:
            code = code[0]
            if  datetime.now(tz=pytz.utc) < code.expiring_date:
                return Response({"status": "ok"})
            return Response({"status": "Code expired"}, status=status.HTTP_423_LOCKED)
        return Response({"status": "Invalid code"}	, status=status.HTTP_417_EXPECTATION_FAILED)
    except Exception as e:
        return Response({"error": str(e)})

