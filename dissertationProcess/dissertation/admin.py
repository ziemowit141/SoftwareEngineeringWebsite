from django.contrib import admin
from .models import Profile, Thesis, Message

class ProfileAdmin(admin.ModelAdmin):
    # list_display = ('user__first_name', 'user__last_name', 'user__email')
    filter_horizontal = ('thesisList',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Thesis)
admin.site.register(Message)