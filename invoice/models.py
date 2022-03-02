from datetime import date
from decimal import Decimal

from django.db import models

# Create your models here.
class Invoice(models.Model):
    invoice_date = models.DateField(default=date.today)
    seller_name = models.CharField("Seller Name", max_length=100)
    seller_address = models.CharField("Seller Addresss", max_length=200)
    seller_mobile = models.BigIntegerField(("Seller Mobile"))
    buyer_name = models.CharField(("Buyer Name"), max_length=50)
    buyer_address = models.CharField(("Buyer Address"), max_length=200)
    buyer_mobile = models.BigIntegerField(("Buyer Mobile"))
    
    # def __str__(self):
    #    return str(self.buyer_name)
    
    def recent_invoices(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now
    
    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total()
        return total
    
    class Meta:
        ordering = ('-invoice_date', 'id')

class Item(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', unique=False, on_delete=models.CASCADE)
    description = models.CharField("Item Name",max_length=100)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def total(self):
        total = Decimal(str(self.unit_price * self.quantity))
        return total.quantize(Decimal('0.01'))

    def __str__(self):
        return self.item_name