from django.contrib import admin

from .models import *


class ListingAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "condition", "category", "active_status"]
    list_editable = ["condition", "category"]
    filter_horizontal = ("comments",)


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Time)
admin.site.register(Comment)