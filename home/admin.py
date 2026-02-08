from django.contrib import admin
from .models import NewsletterSubscriber
from .models import ContactInquiry

# Register your models here.


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_added',)
    ordering = ('-date_added',)


@admin.register(ContactInquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message')
    ordering = ('-date_submitted',)
