from django.contrib import admin
from rest_adv.models import Restaurant,Review
# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','restaurant', 'message', 'rate')

admin.site.register(Restaurant)
admin.site.register(Review, ReviewAdmin)
