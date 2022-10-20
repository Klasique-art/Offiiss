from django.db import models
from tastypie.utils.timezone import now

# Create your models here.
class AgentType(models.Model):
    slug = models.SlugField(max_length = 205,null =
     True,blank = True)
    type = models.CharField(max_length=200)
    type_image = models.ImageField(upload_to='type_images', null=True, blank=True)

    def __str__(self):
        return self.type

class Agent(models.Model):
    name = models.CharField(max_length=200)
    telephone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='agent_profile_pic', null=True, blank=True)
    agent_type = models.ForeignKey(AgentType, on_delete=models.CASCADE)
    company = models.CharField(max_length=200,null=True,blank=True)
    company_description = models.TextField(null=True,blank=True)
    company_location = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null = True,blank = True,default = "Accra")
    region = models.CharField(max_length=200,null = True,blank = True,default = 'Greater Accra')
    def __str__(self):
        return self.name

class Review(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE,null = True,blank =True,related_name = 'reviews')
    name = models.CharField(max_length=200,null = True,blank = True)
    date = models.DateTimeField(default=now)
    content = models.TextField(max_length = 250,null = True,blank = True)
    rating = models.DecimalField(max_digits = 2,decimal_places = 1,null = True,blank = True)
    def __str__(self):
        return self.name
