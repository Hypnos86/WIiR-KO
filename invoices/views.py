import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from invoices.models import Invoice, InvoiceItems, DocumentTypes, ContractTypes, Group
from invoices.forms import InvoiceForm, InvoiceItemsForm

logger = logging.getLogger(__name__)


class NewInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    template_error = 'main/error.html'
    form_class = InvoiceForm

    def get(self, request):
        try:
            form = self.form_class()
            doc_types = form.fields["doc_types"].queryset = DocumentTypes.objects.all()
            context = {'form': form, 'doc_types': doc_types, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

    def post(self, request):
        try:
            form = self.form_class(request.POST or None)
            # doc_types = form.fields["doc_types"].queryset = DocumentTypes.objects.all()
            doc_types = DocumentTypes.objects.all()
            # type_contract = form.fields["type_contract"].queryset = ContractTypes.objects.all()
            type_contract = ContractTypes.objects.all()
            if request.method == 'POST':
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.author = request.user
                    form.save()
                    return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': instance.slug}))
            context = {'form': form, 'doc_types': doc_types, 'type_contract': type_contract, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


# class NewInvoiceItemsView(LoginRequiredMixin, View):
#     template_name = 'invoices/form_items.html'
#     template_error = 'main/error.html'
#     form_class = InvoiceItemsForm
#
#     def get(self, request, invoiceSlug):
#         invoice = get_object_or_404(Invoice, slug=invoiceSlug)
#         form = self.form_class()
#
#         context = {'form': form, "invoice": invoice, 'invoiceSlug': invoiceSlug, 'new': True}
#         return render(request, self.template_name, context)


class EditInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    template_error = 'main/error.html'

    def get(self, request, invoiceSlug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            form = InvoiceForm(instance=invoice)
            context = {'form': form, 'invoice': invoice, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

    def post(self, request, invoiceSlug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            form = InvoiceForm(request.POST, instance=invoice)

            if request.method == 'POST':
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.author = request.user
                    form.save()
                    return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': instance.slug}))
            context = {'form': form, 'invoice': invoice, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class AddInvoiceItemsView(LoginRequiredMixin, View):
    template_name = 'invoices/form_items.html'
    template_error = 'main/error.html'
    form_class = InvoiceItemsForm

    def get(self, request, invoiceSlug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            items = invoice.items.all()  # Pobierz wszystkie pozycje faktury powiązane z tą fakturą
            form = self.form_class(
                initial={'contract_types': ContractTypes.objects.first(),
                         'group': Group.objects.first()
                         }
            )
            # form.fields['group'].widget.attrs['disabled'] = 'true'
            context = {'form': form, "invoice": invoice, "items": items, 'invoiceSlug': invoiceSlug}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

    def post(self, request, invoiceSlug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            form = self.form_class(request.POST)
            items = InvoiceItems.objects.filter(invoice_id=invoice)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.invoice_id = invoice
                form.save()

                return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': invoice.slug}))
            context = {'form': form, 'invoice': invoice, 'items': items, 'invoiceSlug': invoiceSlug}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error('Error: %s', e)
            return render(request, self.template_error, context)


class DeleteInvoiceItemView(View):
    template_error = 'main/error.html'

    def get(self, request, invoiceSlug, item_id):
        try:
            item = get_object_or_404(InvoiceItems, pk=item_id)
            item.delete()
            return redirect(reverse("invoices:addItems", kwargs={"invoiceSlug": invoiceSlug}))
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e}
            logger.error("Error: %s", e)
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)
