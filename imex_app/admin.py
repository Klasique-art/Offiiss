from django.contrib import admin
from .models import Profile, Review, AgentType,Order,Code,Agent,Transporter
from django.db.models import Avg

# Register your models here.
admin.site.register(Agent)
admin.site.register(Transporter)
class ProfileAdmin(admin.ModelAdmin):
    model  = Profile
    list_display = ["id","user", 'name',  'telephone_number', 'image', ]
    list_filter = ['user', 'telephone_number', ]
    search_fields = ("user__username", "name", "telephone_number")
    def average_rating(self, obj):
        avg_rate = obj.user.reviews.aggregate(Avg('rating'))
        return avg_rate["rating__avg"]

admin.site.register(Profile, ProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
    model  = Review
    list_display = ['agent','rating', 'date', 'content', 'client']

admin.site.register(Review, ReviewAdmin)

admin.site.site_title = "Offiis"
admin.site.site_header = "Offiis admin"

class AgentTypeAdmin(admin.ModelAdmin):
    model = AgentType
    list_display = ['id','type', 'type_image']
admin.site.register(AgentType, AgentTypeAdmin)

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id','agent_id','client_id','code','is_done','code_active']
admin.site.register(Order,OrderAdmin)


class CodeAdmin(admin.ModelAdmin):
    model = Code
    list_display = ['email','unique_code','date_generated','expiring_date']
admin.site.register(Code,CodeAdmin)
