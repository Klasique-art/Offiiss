from random import choices
from django.db import models
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.class AgentType(models.Model):

class Profile(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telephone_number = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='profile', null=True, blank=True,default = '/profile/profile1.jpeg')
    is_agent = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    # user_type = models.PositiveSmallIntegerField(choices=((1, 'client'), (2, 'agent')), default=1)
    # license = models.ImageField(upload_to='license', null=True, blank=True)
    # agent_type = models.ForeignKey(AgentType, on_delete=models.CASCADE, related_name='agents', null=True, blank=True)
    # is_validated = models.BooleanField(default=True)
    # company = models.CharField(max_length=200,null=True,blank=True)
    # company_description = models.TextField(null=True,blank=True)
    # company_location = models.CharField(max_length=200,null=True,blank=True)
    # city = models.CharField(max_length=200,null = True,blank = True)
    # is_sea_port = models.BooleanField(default = False)
    # ghana_card = models.CharField(max_length=100)
    # is_air_port = models.BooleanField(default = False)
    # AGENT_STATUS_CHOICES = (
    #     (1, 'created'),
    #     (2, 'pending'),
    #     (3, 'verified'),
    # )
    # agent_status = models.PositiveSmallIntegerField(choices = AGENT_STATUS_CHOICES,default = 1)
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client',null = True,blank=True)
    date = models.DateTimeField(default=now)
    content = models.TextField(max_length = 250,null = True,blank = True)
    rating = models.DecimalField(max_digits = 2,decimal_places = 1,null = True,blank = True)
    # def __str__(self):
    #     return str(self.date)



class Order(models.Model):
    order_name = models.CharField(max_length=100)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_orders')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(default=now)
    code = models.CharField(max_length=20, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    code_active = models.BooleanField(default=False)
    class Meta:
        ordering = ['date']
    # def __str__(self):
    
    #     return str(self.date)


class Code(models.Model):
    email = models.CharField(max_length=150,null=True,blank=True)
    date_generated = models.DateTimeField(default=now)
    expiring_date = models.DateTimeField()
    unique_code = models.CharField(max_length=20)
    def __str__(self):
        return self.unique_code


class EmialCode(models.Model):
    email = models.CharField(max_length=150,null=True,blank=True)
    date_generated = models.DateTimeField(default=now)
    expiring_date = models.DateTimeField()
    unique_code = models.CharField(max_length=20)
    def __str__(self):
        return self.unique_code



class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='agent')
    agent_name = models.CharField(max_length=100,null=True, blank=True)
    agent_phone = models.CharField(max_length=50,null=True, blank=True)
    company_name = models.CharField(max_length=100,null=True, blank=True)
    location = models.CharField(max_length=150,null=True, blank=True)
    AGENT_CATEGORY_CHOICES = (
        (1, 'seaport'),
        (2, 'airport'),
        (3, 'both'),
    )
    
    category = models.PositiveSmallIntegerField(choices=AGENT_CATEGORY_CHOICES,default=1)

    AGENT_STATUS_CHOICES = (
        (1, 'pending'),
        (2, 'active'),
        
    )
    
    status = models.PositiveSmallIntegerField(choices=AGENT_STATUS_CHOICES,default=1)
    description = models.CharField(max_length=300,null=True, blank=True)
    license = models.ImageField(upload_to='license', null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile', null=True, blank=True,default = '/profile/profile1.jpeg')
    cover_image = models.ImageField(upload_to='cover', null=True, blank=True,default = '/cover/header.png')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent_name
class Transporter(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="transporter")
    driver_name = models.CharField(max_length=100,blank=True,null=True)
    driver_license_number = models.CharField(max_length=100,blank=True,null=True)
    driver_phone = models.CharField(max_length=50,blank=True,null=True)
    trailer_axle = models.CharField(max_length=50,blank=True,null=True)
    triiler_type = models.CharField(max_length=50,blank=True,null=True)
    triiler_length = models.CharField(max_length=50,blank=True,null=True)
    trucks_plate_number = models.CharField(max_length=50,blank=True,null=True)
    license_number = models.CharField(max_length=50,blank=True,null=True)
    trailer_license_plate = models.CharField(max_length=50,blank=True,null=True)
    description = models.CharField(max_length=300,blank=True,null=True)
    profile_image = models.ImageField(upload_to='profile', null=True, blank=True,default = '/profile/profile1.jpeg')
    vehicle_1 = models.ImageField(upload_to='vehicles', null=True, blank=True,default = '/cover/header.png')
    vehicle_2 = models.ImageField(upload_to='vehicles', null=True, blank=True,default = '/cover/header.png')
    vehicle_3 = models.ImageField(upload_to='vehicles', null=True, blank=True,default = '/cover/header.png')
    vehicle_4 = models.ImageField(upload_to='vehicles', null=True, blank=True,default = '/cover/header.png')
    TRANSPORTER_STATUS_CHOICES = (
        (1, 'pending'),
        (2, 'active'),
    )
    
    status = models.PositiveSmallIntegerField(choices=TRANSPORTER_STATUS_CHOICES,default=1)
    location = models.CharField(max_length=150,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.email


class AgentReview(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='agent_reviews')
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='agent_client',null = True,blank=True)
    date = models.DateTimeField(default=now)
    content = models.TextField(max_length = 250,null = True,blank = True)
    rating = models.DecimalField(max_digits = 2,decimal_places = 1,null = True,blank = True)
    def __str__(self):
         return str(self.date)

class TransporterReview(models.Model):
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE, related_name='transporter_reviews')
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transporter_client',null = True,blank=True)

    date = models.DateTimeField(default=now)
    content = models.TextField(max_length = 250,null = True,blank = True)
    rating = models.DecimalField(max_digits = 2,decimal_places = 1,null = True,blank = True)
    def __str__(self):
         return str(self.date)