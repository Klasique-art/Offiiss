from django.contrib import admin
from .models import Agent, Review, AgentType

# Register your models here.

class AgentAdmin(admin.ModelAdmin):
    model  = Agent
    list_display = ['name', 'telephone_number', 'image', 'company', 'agent_type', 'company_location', 'company_description']

admin.site.register(Agent, AgentAdmin)

class ReviewAdmin(admin.ModelAdmin):
    model  = Review
    list_display = ['name', 'date', 'content','rating']

admin.site.register(Review, ReviewAdmin)
admin.site.site_title = "Imex"
admin.site.site_header = "Imex admin"

class AgentTypeAdmin(admin.ModelAdmin):
    model = AgentType
    list_display = ['type', 'type_image']
admin.site.register(AgentType, AgentTypeAdmin)
