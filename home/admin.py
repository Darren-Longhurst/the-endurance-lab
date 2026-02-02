from django.contrib import admin
from .models import NewsletterSubscriber

# Register your models here.

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_added',)
    ordering = ('-date_added',)
