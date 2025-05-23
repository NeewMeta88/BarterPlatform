from django.contrib import admin
from .models import Ad, ExchangeProposal

class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'condition', 'created_at')
    list_filter = ('category', 'condition')
    search_fields = ('title', 'description', 'user__username')

class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_sender', 'ad_receiver', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('ad_sender__title', 'ad_receiver__title', 'ad_sender__user__username', 'ad_receiver__user__username')

admin.site.register(Ad, AdAdmin)
admin.site.register(ExchangeProposal, ExchangeProposalAdmin)