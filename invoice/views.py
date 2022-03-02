from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.template.loader import get_template
from django.views import generic
from django.forms import formset_factory

from io import BytesIO
from xhtml2pdf import pisa

from .models import Invoice, Item
from .forms import InvoiceForm, ItemForm


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_invoice_list'

    def get_queryset(self):
        """Return the last five created Invoice."""
        return Invoice.objects.order_by('-invoice_date')[:5]

class DetailView(generic.DetailView):
    model = Invoice
    template_name = 'detail.html'

class DynamicFormView(generic.FormView):
    form_class = InvoiceForm
    template_name = "create.html"


def create(request):
    invoice_form = InvoiceForm()
    OrderFormSet = formset_factory(ItemForm)
    order_formset = OrderFormSet()
    if request.method == 'POST':

        invoice_form = InvoiceForm(request.POST)
        OrderFormSet = formset_factory(ItemForm)
        order_formset = OrderFormSet(request.POST)

        if order_formset.is_valid() and invoice_form.is_valid():
            invoice = invoice_form.save()
            
            for order_form in order_formset:
                description = order_form.cleaned_data['description']
                unit_price = order_form.cleaned_data['unit_price']
                quantity = order_form.cleaned_data['quantity']
                item = Item(
                    invoice=invoice,
                    description=description,
                    unit_price=unit_price,
                    quantity=quantity
                )
                item.save()
            return redirect("display", invoice_id=invoice.id)

    template_context = {
        'invoice_form': invoice_form,
        'order_formset': order_formset,
    }

    template = 'create.html'

    return render(request, template, template_context)

def display_pdf(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        raise Http404("Invoice does not exist or Have been deleted")
    
    template_path = 'invoice_printer.html'
    context = {
        'invoice': invoice,
        'total' : 1
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice_.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
