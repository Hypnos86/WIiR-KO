import csv
import logging
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from invoices.models import Invoice, InvoiceItems, DocumentTypes, ContractTypes, Group
from invoices.forms import InvoiceForm, InvoiceItemsForm
from units.models import Unit
from django.core.serializers import serialize
from core.data_db import ParagraphEnum, GroupsApp

logger = logging.getLogger(__name__)

TEMPLATE_ERROR = "main/error.html"

def handle_exception(request, e, method):
    context = {
        "error": e,
        "method": method,
    }
    logger.error("Error: %s", e)
    return render(request, TEMPLATE_ERROR, context)

class NewInvoiceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = "invoices/form_invoice.html"
    form_class = InvoiceForm
    method = "NewInvoiceView"

    # wymagane uprawnienie Django (user + grupy + superuser)
    permission_required = "invoices.add_invoice"
    raise_exception = True  # zamiast redirectu na login -> 403 przy braku perms

    def get(self, request):
        try:
            form = self.form_class()
            doc_types = DocumentTypes.objects.all()
            context = {
                "form": form,
                "doc_types": doc_types,
                "new": True,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            return handle_exception(request, e, self.method)

    def post(self, request):
        try:
            form = self.form_class(request.POST or None)

            doc_types = DocumentTypes.objects.all()
            type_contract = ContractTypes.objects.all()

            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()  # ważne: zapisujemy instancję z ustawionym author

                return redirect(
                    reverse("invoices:addItems", kwargs={"invoiceSlug": instance.slug})
                )

            context = {
                "form": form,
                "doc_types": doc_types,
                "type_contract": type_contract,
                "new": True,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            return handle_exception(request, e, self.method)


class EditInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    method = 'EditInvoiceView'

    def get_invoice(self, invoiceSlug):
        invoice = Invoice.objects.only("date", "no_invoice", "slug", "sum")
        return get_object_or_404(invoice, slug=invoiceSlug)

    def get(self, request, invoiceSlug):
        try:
            invoice = self.get_invoice(invoiceSlug)
            form = InvoiceForm(instance=invoice)
            context = {'form': form, 'invoice': invoice, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            return handle_exception(request, e, self.method)

    def post(self, request, invoiceSlug):
        try:
            invoice = self.get_invoice(invoiceSlug)
            form = InvoiceForm(request.POST, instance=invoice)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                form.save()
                return redirect(reverse('invoices:editInvoice', kwargs={'invoiceSlug': instance.slug}))

            context = {'form': form, 'invoice': invoice,'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            return handle_exception(request, e, self.method)


class AddInvoiceItemsView(LoginRequiredMixin, View):
    template_name = 'invoices/form_items.html'
    form_class = InvoiceItemsForm
    method = 'AddInvoiceItemsView'

    def get_invoice(self, invoiceSlug):
        invoice = Invoice.objects.only("date", "no_invoice", "slug", "sum")
        return get_object_or_404(invoice, slug=invoiceSlug)

    def get(self, request, invoiceSlug):
        try:
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
                       "items": items,
                       'invoiceSlug': invoiceSlug,
                       'countiesSum': counties,
                       'edit_item': False
                       }
            return render(request, self.template_name, context)

        except Exception as e:
            return handle_exception(request, e, self.method)

    def post(self, request, invoiceSlug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            form = self.form_class(request.POST)
            items = InvoiceItems.objects.filter(invoice_id=invoice)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.invoice_id = invoice
                instance.author = request.user
                form.save()

                return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': invoice.slug}))
            context = {'form': form, 'invoice': invoice,
                       'items': items,
                       'invoiceSlug': invoiceSlug}
            return render(request, self.template_name, context)
        except Exception as e:
            return handle_exception(request, e, self.method)


class EditInvoiceItemsView(LoginRequiredMixin, View):
    template_name = 'invoices/form_items.html'
    form_class = InvoiceItemsForm
    method = 'EditInvoiceItemsView'


    def get(self, request, invoiceSlug, itemId):
        try:
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
                       "items": items,
                       'invoiceSlug': invoiceSlug,
                       'counties_sum': counties,
                       'edit_item': True
                       # 'measurementData': measurementSystemNumberList
                       }
            return render(request, self.template_name, context)

        except Exception as e:
            return handle_exception(request, e, self.method)

    def post(self, request, invoiceSlug, itemId):

        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            item = get_object_or_404(InvoiceItems, id=itemId)

            form = self.form_class(request.POST, instance=item)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.invoice_id = invoice
                instance.author = request.user
                form.save()

                return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': invoice.slug}))

            context = {'form': form, 
                       'invoice': invoice, 
                       'item_id': itemId}
            return render(request, self.template_name, context)

        except Exception as e:
            return handle_exception(request, e, self.method)


class DeleteInvoiceView(LoginRequiredMixin, View):
    method = 'DeleteInvoiceView'

    def get(self, request, invoiceSlug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            invoice.delete()
            return redirect("main:invoiceSite")
        except Exception as e:
            return handle_exception(request, e, self.method)


class DeleteInvoiceItemView(LoginRequiredMixin, View):
    method = 'DeleteInvoiceItemView'

    def get(self, request, invoiceSlug, item_id):
        try:
            item = get_object_or_404(InvoiceItems, pk=item_id)
            item.delete()
            return redirect(reverse("invoices:addItems", kwargs={"invoiceSlug": invoiceSlug}))
        except Exception as e:
            return handle_exception(request, e, self.method)


class CreateCSVForItems(View):
    method = 'CreateCSVForItems'

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
            return handle_exception(request, e, self.method)


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
