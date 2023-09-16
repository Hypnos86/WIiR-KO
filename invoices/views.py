import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from invoices.models import DocumentTypes, ContractTypes
from invoices.forms import InvoiceForm
from invoices.models import Invoice, InvoiceItems, Paragraph
from units.models import Unit
from main.views import CurrentDate

logger = logging.getLogger(__name__)


class InvoicesListView(LoginRequiredMixin, View):
    template_name = 'invoices/list_invoice.html'

    def get(self, request):
        invoices = Invoice.objects.all()
        context = {'invoices': invoices}
        return render(request, self.template_name, context)


class NewInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    form_class = InvoiceForm

    def get(self, request):
        try:
            form = self.form_class()
            doc_types = form.fields["doc_types"].queryset = DocumentTypes.objects.all()
            type_contract = form.fields["type_contract"].queryset = ContractTypes.objects.all()
            # form.fields["doc_types"].queryset = DocumentTypes.objects.exclude(type="Nota korygująca")
            context = {'form': form, 'doc_types': doc_types, 'type_contract': type_contract, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)

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
                    return redirect(reverse('invoices:items', kwargs={'invoice_slug': instance.slug}))
            context = {'form': form, 'doc_types': doc_types, 'type_contract': type_contract, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)


class EditInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'

    # slugCard
    def get(self, request, invoice_slug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoice_slug)
            form = InvoiceForm(instance=invoice)

            # doc_types = form.fields["doc_types"].queryset = DocumentTypes.objects.all()
            # type_contract = form.fields["type_contract"].queryset = ContractTypes.objects.all()
            # 'doc_types': doc_types, 'type_contract': type_contract,
            context = {'form': form, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)

    def post(self, request, invoice_slug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoice_slug)
            form = InvoiceForm(request.POST, instance=invoice)

            # doc_types = form.fields["doc_types"].queryset = DocumentTypes.objects.all()
            # doc_types = DocumentTypes.objects.all()
            # type_contract = form.fields["type_contract"].queryset = ContractTypes.objects.all()
            type_contract = ContractTypes.objects.all()
            if request.method == 'POST':
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.author = request.user
                    form.save()
                    return redirect(reverse('invoices:items', kwargs={'invoice_slug': instance.slug}))
                # 'doc_types': doc_types,
            context = {'form': form, 'type_contract': type_contract, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)


class InvoiceInfoView(View):
    template_name = 'invoices/modal_invoice_info.html'

    def get(self, request, id):
        try:
            invoice = get_object_or_404(Invoice, pk=id)
            items = InvoiceItems.objects.filter(invoice_id=invoice.id)
            context = {'invoice': invoice, 'items': items, 'id': id}
            return render(request, self.template_name, context)

        except Exception as e:
            logger.error("Error: %s", e)


class InvoiceItemsView(LoginRequiredMixin, View):
    template_name = 'invoices/form_items.html'

    # form_class = InvoiceItemsForm

    def get(self, request, invoice_slug):
        # invoice = get_object_or_404(InvoicesView, slug=invoice_slug)
        # form = self.form_class()
        # invoice_items = InvoiceItems.objects.filter(invoice_id=invoice)
        # 'form': form, "invoice": invoice, "invoice_items": invoice_items,
        context = {
            'new': True}
        return render(request, self.template_name, context)


class UnitCostListView(View):
    template_name = 'invoices/list_invoices_unit.html'

    def get(self, request, unit_slug, paragraph_slug):
        currentYear = CurrentDate().current_year()
        unit = get_object_or_404(Unit, slug=unit_slug)
        items = InvoiceItems.objects.filter(unit__slug=unit_slug, paragraph__slug=paragraph_slug,
                                            invoice_id__date__year=currentYear)
        lastUpdate = items.last()
        paragraph = Paragraph.objects.get(slug=paragraph_slug)

        countyCardSlug = unit.county_unit.slug

        context = {'unit': unit, 'items': items, 'currentYear': currentYear, 'paragraph': paragraph,
                   'countyCardSlug': countyCardSlug, 'lastUpdate': lastUpdate}
        return render(request, self.template_name, context)
