from django.contrib import admin
from .models import Profile, Review, AgentType
from django.db.models import Avg

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    model  = Profile
    list_display = ["user", 'name', 'agent_type', 'telephone_number', 'image', 'company', 'company_location', 'company_description', 'city', 'region', 'user_type', 'average_rating']
    list_filter = ['user', 'company', 'telephone_number', 'agent_type']
    search_fields = ("user__username", "name", "company", "city", "region", "telephone_number")
    def average_rating(self, obj):
        avg_rate = obj.user.reviews.aggregate(Avg('rating'))
        return avg_rate["rating__avg"]

admin.site.register(Profile, ProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
    model  = Review
    list_display = ['agent', 'date', 'content', 'client']

admin.site.register(Review, ReviewAdmin)

admin.site.site_title = "Offiis"
admin.site.site_header = "Offiis admin"

class AgentTypeAdmin(admin.ModelAdmin):
    model = AgentType
    list_display = ['type', 'type_image']
admin.site.register(AgentType, AgentTypeAdmin)
