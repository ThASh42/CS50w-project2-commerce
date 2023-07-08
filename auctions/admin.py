from django.contrib import admin

from .models import *


class ListingAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "condition", "category", 
                    "active_status", "winner",]
    
    list_editable = ["condition", "category", "active_status",]
    
    filter_horizontal = ("watchlist", "comments",)
    
    readonly_fields = ["bids", "time", "winner",]
    
    fields = ["owner", "title", "description", "start_bid", "image", "condition", "category",]


class BidAdmin(admin.ModelAdmin):
    readonly_fields = ["price", "user"]
    
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False


class TimeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Comment)