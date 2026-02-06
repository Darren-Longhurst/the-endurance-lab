from django.db import models

# Create your models here.

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#Contact Form

class ContactInquiry(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_submitted']
        verbose_name = 'Contact enquiry'
        verbose_name_plural = 'Contact enquiries'

    def __str__(self):
        return f"Inquiry from {self.full_name} - {self.date_submitted.strftime('%d/%m/%Y')}"
