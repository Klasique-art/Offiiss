from random import choices
from django.db import models
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.class AgentType(models.Model):
class AgentType(models.Model):
    slug = models.SlugField(max_length = 205,null =
     True,blank = True)
    type = models.CharField(max_length=200)
    type_image = models.ImageField(upload_to='type_images', null=True, blank=True)

    def __str__(self):
        return self.type
class Profile(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telephone_number = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='profile', null=True, blank=True,default = '/profile/profile1.jpeg')
    is_agent = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
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
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client',null = True,blank=True)
    date = models.DateTimeField(default=now)
    content = models.TextField(max_length = 250,null = True,blank = True)
    rating = models.DecimalField(max_digits = 2,decimal_places = 1,null = True,blank = True)
    def __str__(self):
        return str(self.date)

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
    def __str__(self):
        # there is no such field as client_name or user in this model please take note
        return self.client.first_name + ' working with ' + self.agent.username + ' as an agent'


class Code(models.Model):
    email = models.CharField(max_length=150,null=True,blank=True)
    date_generated = models.DateTimeField(default=now)
    expiring_date = models.DateTimeField()
    unique_code = models.CharField(max_length=20)
    def __str__(self):
        return self.unique_code


class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=100)
    agent_phone = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    AGENT_CATEGORY_CHOICES = (
        (1, 'seaport'),
        (2, 'airport'),
        (3, 'both'),
    )
    
    category = models.PositiveSmallIntegerField(choices=AGENT_CATEGORY_CHOICES)
    description = models.CharField(max_length=300)
    license = models.ImageField(upload_to='license', null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile', null=True, blank=True,default = '/profile/profile1.jpeg')

    def __str__(self):
        return self.agent_name
class Transporter(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=100)
    driver_license_number = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=50)
    trailer_axle = models.CharField(max_length=50,blank=True,null=True)
    triiler_type = models.CharField(max_length=50,blank=True,null=True)
    triiler_length = models.CharField(max_length=50,blank=True,null=True)
    trucks_plate_number = models.CharField(max_length=50,blank=True,null=True)
    license_number = models.CharField(max_length=50,blank=True,null=True)
    trailer_license_plate = models.CharField(max_length=50,blank=True,null=True)
    description = models.CharField(max_length=300)
    profile_image = models.ImageField(upload_to='profile', null=True, blank=True,default = '/profile/profile1.jpeg')


    def __str__(self):
        return self.driver_name