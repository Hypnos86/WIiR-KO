import csv
import logging
from enum import Enum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from invoices.models import Invoice, InvoiceItems, DocumentTypes, ContractTypes, Group
from invoices.forms import InvoiceForm, InvoiceItemsForm
from units.models import Unit
from django.core.serializers import serialize

logger = logging.getLogger(__name__)


class ParagraphEnum(Enum):
    MEDIA1 = '4260-01'
    MEDIA2 = '4260-02'
    MEDIA3 = '4260-03'
    MEDIA4 = '4260-04'


def get_user_groups(request):
    'Sprawdzanie czy użytkownik nalezy do górpy administratorów'
    return request.user.groups.filter(name='AdminZRiWT').exists()


class NewInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    template_error = 'main/error.html'
    form_class = InvoiceForm
    method = 'NewInvoiceView'

    def handle_exception(self, request, e):
        user_belongs_to_admin_group = get_user_groups(request)
        context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
        logger.error("Error: %s", e)
        return render(request, self.template_error, context)

    def get(self, request):
        try:
            user_belongs_to_admin_group = get_user_groups(request)
            form = self.form_class()
            doc_types = DocumentTypes.objects.all()
            context = {'form': form, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'doc_types': doc_types,
                       'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            return self.handle_exception(request, e)

    def post(self, request):
        try:
            user_belongs_to_admin_group = get_user_groups(request)
            form = self.form_class(request.POST or None)
            doc_types = DocumentTypes.objects.all()
            type_contract = ContractTypes.objects.all()
            if request.method == 'POST':
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.author = request.user
                    form.save()
                    return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': instance.slug}))
            context = {'form': form, 'doc_types': doc_types, 'user_belongs_to_admin_group': user_belongs_to_admin_group,
                       'type_contract': type_contract, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            return self.handle_exception(request, e)


class EditInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    template_error = 'main/error.html'
    method = 'EditInvoiceView'

    def handle_exception(self, request, e):
        user_belongs_to_admin_group = get_user_groups(request)
        context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
        logger.error("Error: %s", e)
        return render(request, self.template_error, context)

    def get_invoice(self, invoiceSlug):
        invoice = Invoice.objects.only("date", "no_invoice", "slug", "sum")
        return get_object_or_404(invoice, slug=invoiceSlug)

    def get(self, request, invoiceSlug):
        try:
            user_belongs_to_admin_group = get_user_groups(request)
            invoice = self.get_invoice(invoiceSlug)
            form = InvoiceForm(instance=invoice)
            context = {'form': form, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'invoice': invoice,
                       'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            return self.handle_exception(request, e)

    def post(self, request, invoiceSlug):
        try:
            user_belongs_to_admin_group = get_user_groups(request)
            invoice = self.get_invoice(invoiceSlug)
            form = InvoiceForm(request.POST, instance=invoice)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                form.save()
                return redirect(reverse('invoices:editInvoice', kwargs={'invoiceSlug': instance.slug}))

            context = {'form': form, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'invoice': invoice,
                       'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            return self.handle_exception(request, e)


class AddInvoiceItemsView(LoginRequiredMixin, View):
    template_name = 'invoices/form_items.html'
    template_error = 'main/error.html'
    form_class = InvoiceItemsForm
    method = 'AddInvoiceItemsView'

    def get_invoice(self, invoiceSlug):
        invoice = Invoice.objects.only("date", "no_invoice", "slug", "sum")
        return get_object_or_404(invoice, slug=invoiceSlug)

    def handle_exception(self, request, e):
        user_belongs_to_admin_group = get_user_groups(request)
        context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
        logger.error("Error: %s", e)
        return render(request, self.template_error, context)

    def get(self, request, invoiceSlug):
        try:
            user_belongs_to_admin_group = get_user_groups(request)
            invoice = self.get_invoice(invoiceSlug)
            items = invoice.items.all()  # Pobierz wszystkie pozycje faktury powiązane z tą fakturą

            # Tworzenie dodatkowych informacji na temat rozdziałów i sumowania ich
            counties = []
            for item in items:
                sum_value = item.sum
                exist = False
                for county in counties:
                    if item.section.section == county['county']:
                        county['sum'] += sum_value
                        exist = True
                if not exist:
                    counties.append({'county': item.section.section, 'sum': sum_value})

            # ---------------------------------------------
            objectsForFile = []
            for item in invoice.items.all():
                sum_value = item.sum
                exist = False
                for row in objectsForFile:
                    if item.unit.county_swop.name == row['county']:
                        row['sum'] = + sum_value
                        exist = True
                if not exist:
                    objectsForFile.append(
                        {'section': item.section.section, 'county': item.unit.county_swop.name, 'sum': item.sum})
            # ---------------------------------------------
            form = self.form_class(
                initial={'contract_types': ContractTypes.objects.first()}
            )

            context = {'form': form,
                       "invoice": invoice,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group,
                       "items": items,
                       'invoiceSlug': invoiceSlug,
                       'countiesSum': counties,
                       }
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

    def post(self, request, invoiceSlug):
        try:
            user_belongs_to_admin_group = get_user_groups(request)
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            form = self.form_class(request.POST)
            items = InvoiceItems.objects.filter(invoice_id=invoice)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.invoice_id = invoice
                instance.author = request.user
                form.save()

                return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': invoice.slug}))
            context = {'form': form, 'invoice': invoice, 'user_belongs_to_admin_group': user_belongs_to_admin_group,
                       'items': items,
                       'invoiceSlug': invoiceSlug}
            return render(request, self.template_name, context)
        except Exception as e:
            return self.handle_exception(request, e)


class EditInvoiceItemsView(LoginRequiredMixin, View):
    template_name = 'invoices/form_items.html'
    template_error = 'main/error.html'
    form_class = InvoiceItemsForm
    method = 'EditInvoiceItemsView'

    def handle_exception(self, request, e):
        user_belongs_to_admin_group = get_user_groups(request)
        context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
        logger.error("Error: %s", e)
        return render(request, self.template_error, context)

    def get(self, request, invoiceSlug, itemId):
        try:
            user_belongs_to_admin_group = get_user_groups(request)
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            items = invoice.items.all()
            units = Unit.objects.all()
            item = get_object_or_404(InvoiceItems, id=itemId)
            form = self.form_class(instance=item)
            contract_types = ContractTypes.objects.all()

            # measurementSystemNumberList = []
            #
            # for unit in units:
            #     selected_items = unit.items.all()
            #     data = []
            #     for type_object in contract_types:
            #         for paragraph_enum in ParagraphEnum:
            #             media_last = selected_items.filter(paragraph__paragraph=paragraph_enum.value).filter(
            #                 contract_types__id=type_object.id).first()
            #             if media_last:
            #                 data.append({
            #                     "par": media_last.paragraph.paragraph,
            #                     "type": media_last.contract_types.type,
            #                     "period": f"{media_last.period_from.strftime('%d.%m.%Y')}-{media_last.period_to.strftime('%d.%m.%Y')}",
            #                     "counterReading": str(media_last.counterReading),
            #                     "measurement": str(media_last.measurementSystemNumber)
            #                 })
            #
            #     measurementSystemNumberList.append({"unit_id": unit.id, "data": data})

            counties = []
            for item in items:
                sum_value = item.sum
                exist = False
                for county in counties:
                    if item.section.section == county['county']:
                        county['sum'] += sum_value
                        exist = True

                if not exist:
                    counties.append({'county': item.section.section, 'sum': sum_value})

            context = {'form': form,
                       "invoice": invoice,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group,
                       "items": items,
                       'invoiceSlug': invoiceSlug,
                       'counties_sum': counties,
                       # 'measurementData': measurementSystemNumberList
                       }
            return render(request, self.template_name, context)

        except Exception as e:
            self.handle_exception(request, e)

    def post(self, request, invoiceSlug, itemId):

        try:
            user_belongs_to_group = get_user_groups(request)
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            # item_id = request.POST.get('item_id')  # Assuming 'item_id' is a hidden input in your form
            item = get_object_or_404(InvoiceItems, id=itemId)

            form = self.form_class(request.POST, instance=item)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.invoice_id = invoice
                instance.author = request.user
                form.save()

                return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': invoice.slug}))

            context = {'form': form, 'invoice': invoice, 'user_belongs_to_group': user_belongs_to_group,
                       'item_id': itemId}
            return render(request, self.template_name, context)

        except Exception as e:
            self.handle_exception(request, e)


class DeleteInvoiceView(LoginRequiredMixin, View):
    template_error = 'main/error.html'
    method = 'DeleteInvoiceView'

    def handle_exception(self, request, e):
        user_belongs_to_admin_group = get_user_groups(request)
        context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
        logger.error("Error: %s", e)
        return render(request, self.template_error, context)

    def get(self, request, invoiceSlug):
        user_belongs_to_admin_group = get_user_groups(request)
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            invoice.delete()
            return redirect("main:invoiceSite")
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)


class DeleteInvoiceItemView(LoginRequiredMixin, View):
    template_error = 'main/error.html'
    method = 'DeleteInvoiceItemView'

    def get(self, request, invoiceSlug, item_id):
        user_belongs_to_admin_group = get_user_groups(request)
        try:
            item = get_object_or_404(InvoiceItems, pk=item_id)
            item.delete()
            return redirect(reverse("invoices:addItems", kwargs={"invoiceSlug": invoiceSlug}))
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)


class CreateCSVForItems(View):
    template_error = 'main/error.html'
    method = 'CreateCSVForItems'

    def handle_exception(self, request, e):
        user_belongs_to_admin_group = get_user_groups(request.user)
        context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
        logger.error("Error: %s", e)
        return render(request, self.template_error, context)

    def get(self, request, invoice_id):
        try:
            invoice = get_object_or_404(Invoice, pk=invoice_id)
            # ---------------------------------------------
            objectsForFile = []
            for item in invoice.items.all():
                sum_value = item.sum
                exist = False
                for row in objectsForFile:
                    if item.unit.county_swop.name == row['county']:
                        row['sum'] += sum_value
                        exist = True
                if not exist:
                    objectsForFile.append(
                        {'section': item.section.section, 'county': item.unit.county_swop.name, 'sum': item.sum})

            # ---------------------------------------------

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="Podział fv:{invoice}.csv"'
            # Ustawienie kodowania utf-8
            response.write(u'\ufeff'.encode('utf8'))

            # Tworzenie obiektu writer i zapis do pliku csv
            writer = csv.writer(response, delimiter=';', dialect='excel', lineterminator='\n')
            # Dodaj linię z tekstem "Załącznik do faktury {invoices}"
            response.write(f'Załącznik do faktury {invoice}\n')
            writer.writerow(['Rozdział', 'Powiat', 'Kwota'])
            for row in objectsForFile:
                strSum = str(row['sum'])
                rowSum = strSum.replace('.', ',')
                writer.writerow([row['section'], row['county'], rowSum])
            return response
        except Exception as e:
            self.handle_exception(request, e)


class HandleRequestView(View):
    method = 'HandleRequestView'

    def get(self, request, invoiceSlug):
        try:
            unit_id = request.GET.get('unit_id', '')
            contractTypes_id = request.GET.get('contractTypes_id')
            paragraph_id = request.GET.get('paragraph_id')

            invoiceItem = InvoiceItems.objects.filter(unit=unit_id, contract_types=contractTypes_id,
                                                      paragraph=paragraph_id).values('period_from', 'period_to',
                                                                                     'counterReading',
                                                                                     'consumption',
                                                                                     'measurementSystemNumber').first()
            if invoiceItem and all(invoiceItem.get(key) is not None for key in
                                   ['period_from', 'period_to', 'counterReading', 'consumption',
                                    'measurementSystemNumber']):
                return JsonResponse(invoiceItem, status=200)
            return JsonResponse({'period_from': None, 'period_to': None, 'counterReading': None, 'consumption': None,
                                 'measurementSystemNumber': None}, status=200)
        except Exception as e:
            logger.error(f"Błąd podczas przetwarzania żądania: {e}")
            return JsonResponse({'error': str(e)}, status=500)
