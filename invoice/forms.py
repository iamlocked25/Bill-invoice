from django import forms

from .models import Invoice, Item

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'invoice_date',
            'seller_name',
            'seller_address',
            'seller_mobile',
            'buyer_name',
            'buyer_address',
            'buyer_mobile',
        ]
    # def __init__(self, *args, **kwargs):
    #     super(InvoiceForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'description',
            'unit_price',
            'quantity'
        ]
    # def __init__(self, *args, **kwargs):
    #     super(ItemForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'