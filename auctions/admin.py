from django.contrib import admin

from .models import *


class ListingAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "condition", "category", 
                    "active_status", "winner",]
    
    list_editable = ["condition", "category", "active_status",]
    
    filter_horizontal = ("watchlist", "comments",)
    
    readonly_fields = ["bids", "time", "winner",]
    
    def get_fieldsets(self, request, obj=None):
        if obj:
            # Fields to display when editing an existing listing
            fieldsets = (
                ('Edit Listing', {
                    'fields': ('owner', 'title', 'description', 'start_bid', 'image', 'condition', 'category', 'active_status', 'watchlist', 'comments')
                }),
            )
        else:
            # Fields to display when adding a new listing
            fieldsets = (
                ('Add Listing', {
                    'fields': ('owner', 'title', 'description', 'start_bid', 'image', 'condition', 'category')
                }),
            )
        
        return fieldsets


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


class CommentAdmin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj=None):
        if obj:
            # Fields to display when editing an existing listing
            fieldsets = (
                ('Edit Comment', {
                    'fields': ("commentator", "message", "is_modified",)
                }),
            )
        else:
            # Fields to display when adding a new listing
            fieldsets = (
                ('Add Comment', {
                    'fields': ("commentator", "message",)
                }),
            )
        
        return fieldsets


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Comment, CommentAdmin)