from django.contrib import admin

from .models import *


class ListingAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "image", "description", "condition", "category", 
                    "active_status", "winner", "time"]
    list_editable = ["condition", "category", "active_status", "image", "description"]


class BidAdmin(admin.ModelAdmin):
    list_display = ["price", "user", "time"]
    list_display_links = ["price", "user", "time"]


class TimeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False


class CommentAdmin(admin.ModelAdmin):
    list_display = ["commentator", "message", "time", "is_modified"]
    list_editable = ["message", "is_modified"]


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserBiddingActivity)