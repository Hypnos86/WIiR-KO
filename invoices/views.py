from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class InvoicesView(LoginRequiredMixin, View):
    template_name = 'invoices/list_invoice.html'

    def get(self, request):
        return render(request, self.template_name)


class NewInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'

    def get(self, request):
        context = {'new': True}
        return render(request, self.template_name, context)

    def post(self, request):
        context = {'new': True}
        return render(request, self.template_name, context)
