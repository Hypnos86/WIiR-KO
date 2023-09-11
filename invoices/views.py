from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from invoices.models import DocumentTypes
from invoices.forms import InvoiceForm


class InvoicesView(LoginRequiredMixin, View):
    template_name = 'invoices/list_invoice.html'

    def get(self, request):
        return render(request, self.template_name)


class NewInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    form_class = InvoiceForm

    def get(self, request):
        form = self.form_class()
        doc_types = form.fields["doc_types"].queryset = DocumentTypes.objects.all()
        # form.fields["doc_types"].queryset = DocumentTypes.objects.exclude(type="Nota korygująca")
        context = {'form': form, 'doc_types': doc_types, 'new': True}
        return render(request, self.template_name, context)

    def post(self, request):
        context = {'new': True}
        return render(request, self.template_name, context)
