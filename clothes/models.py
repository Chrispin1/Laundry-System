from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
PAYMENT_CHOICES = (
    ("CASH", "CASH"),
    ("MPESA", "MPESA"),
    ("SWIPE", "SWIPE"),
)

CONDITION_CHOICES = (
    ("GOOD", "GOOD"),
    ("BAD", "BAD"),
)


class Client(models.Model):
    client_name = models.CharField(max_length=400, null=True, blank=True)
    check_in_date = models.DateTimeField(null=True, blank=True)
    check_in_time = models.TimeField(null=True, blank=True)
    picked = models.BooleanField(default=False)
    check_out_date = models.DateTimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True)
    amount = models.PositiveIntegerField(null=True, blank=False)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length = 20,choices = PAYMENT_CHOICES, default = 'CASH')   
 

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
# M-pesa Payment models
class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'
class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'
class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    ttype = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
    def __str__(self):
        return self.first_name