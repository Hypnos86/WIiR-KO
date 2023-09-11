import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from invoices.models import DocumentTypes
from invoices.forms import InvoiceForm

logger = logging.getLogger(__name__)


class InvoicesView(LoginRequiredMixin, View):
    template_name = 'invoices/list_invoice.html'

    def get(self, request):
        return render(request, self.template_name)


class NewInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    form_class = InvoiceForm

    def get(self, request):
        try:
            form = self.form_class()
            doc_types = form.fields["doc_types"].queryset = DocumentTypes.objects.all()
            # form.fields["doc_types"].queryset = DocumentTypes.objects.exclude(type="Nota korygująca")
            context = {'form': form, 'doc_types': doc_types, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)

    def post(self, request):
        try:
            form = self.form_class(request.POST or None)
            if request.method == 'POST':
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.author = request.user
                    form.save()
                    return redirect('main:welcome')
            context = {'form': form, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)


class InvoiceItemsView(LoginRequiredMixin, View):
    template_name = ''
    def get(self, slug):
        pass

