import csv
import logging
from enum import Enum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from invoices.models import Invoice, InvoiceItems, DocumentTypes, ContractTypes, Group
from invoices.forms import InvoiceForm, InvoiceItemsForm
from units.models import Unit

logger = logging.getLogger(__name__)


class ParagraphEnum(Enum):
    MEDIA1 = '4260-01'
    MEDIA2 = '4260-02'
    MEDIA3 = '4260-03'
    MEDIA4 = '4260-04'


class NewInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    template_error = 'main/error.html'
    form_class = InvoiceForm

    def get(self, request):
        user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:

            form = self.form_class()
            doc_types = form.fields["doc_types"].queryset = DocumentTypes.objects.all()
            context = {'form': form, 'user_belongs_to_group': user_belongs_to_group, 'doc_types': doc_types,
                       'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group, }
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

    def post(self, request):
        user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
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
            context = {'form': form, 'doc_types': doc_types, 'user_belongs_to_group': user_belongs_to_group,
                       'type_contract': type_contract, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group, }
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

class EditInvoiceView(LoginRequiredMixin, View):
    template_name = 'invoices/form_invoice.html'
    template_error = 'main/error.html'

    def get(self, request, invoiceSlug):
        user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            form = InvoiceForm(instance=invoice)
            context = {'form': form, 'user_belongs_to_group': user_belongs_to_group, 'invoice': invoice, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group, }
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

    def post(self, request, invoiceSlug):
        user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            form = InvoiceForm(request.POST, instance=invoice)

            if request.method == 'POST':
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.author = request.user
                    form.save()
                    return redirect(reverse('invoices:addItems', kwargs={'invoiceSlug': instance.slug}))
            context = {'form': form, 'user_belongs_to_group': user_belongs_to_group, 'invoice': invoice, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group, }
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class AddInvoiceItemsView(LoginRequiredMixin, View):
    template_name = 'invoices/form_items.html'
    template_error = 'main/error.html'
    form_class = InvoiceItemsForm

    def get(self, request, invoiceSlug):
        user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            items = invoice.items.all()  # Pobierz wszystkie pozycje faktury powiązane z tą fakturą
            units = Unit.objects.all()
            contractTypes = ContractTypes.objects.all()

            measurementSystemNumberList = []

            for unit in units:
                selectedItesms = unit.items.all()
                data = []
                for typeObject in contractTypes:

                    media_1_last = selectedItesms.filter(paragraph__paragraph=ParagraphEnum.MEDIA1.value).filter(
                        contract_types__id=typeObject.id).first()
                    if media_1_last:
                        data.append({"par": media_1_last.paragraph.paragraph, "type": media_1_last.contract_types.type,
                                     "period": f"{media_1_last.period_from.strftime('%d.%m.%Y')}-{media_1_last.period_to.strftime('%d.%m.%Y')}",
                                     "counterReading": str(media_1_last.counterReading),
                                     "measurement": str(media_1_last.measurementSystemNumber)})

                    media_2_last = selectedItesms.filter(paragraph__paragraph=ParagraphEnum.MEDIA2.value).filter(
                        contract_types__id=typeObject.id).first()
                    if media_2_last:
                        data.append({"par": media_2_last.paragraph.paragraph, "type": media_2_last.contract_types.type,
                                     "period": f"{media_2_last.period_from.strftime('%d.%m.%Y')}-{media_2_last.period_to.strftime('%d.%m.%Y')}",
                                     "counterReading": str(media_2_last.counterReading),
                                     "measurement": str(media_2_last.measurementSystemNumber)})

                    media_3_last = selectedItesms.filter(paragraph__paragraph=ParagraphEnum.MEDIA3.value).filter(
                        contract_types__id=typeObject.id).first()
                    if media_3_last:
                        data.append({"par": media_3_last.paragraph.paragraph, "type": media_3_last.contract_types.type,
                                     "period": f"{media_3_last.period_from.strftime('%d.%m.%Y')}-{media_3_last.period_to.strftime('%d.%m.%Y')}",
                                     "counterReading": str(media_3_last.counterReading),
                                     "measurement": str(media_3_last.measurementSystemNumber)})

                    media_4_last = selectedItesms.filter(paragraph__paragraph=ParagraphEnum.MEDIA4.value).filter(
                        contract_types__id=typeObject.id).first()
                    if media_4_last:
                        data.append({"par": media_4_last.paragraph.paragraph, "type": media_4_last.contract_types.type,
                                     "period": f"{media_4_last.period_from.strftime('%d.%m.%Y')}-{media_4_last.period_to.strftime('%d.%m.%Y')}",
                                     "counterReading": str(media_4_last.counterReading),
                                     "measurement": str(media_4_last.measurementSystemNumber)})

                measurementSystemNumberList.append({"unit_id": unit.id, "data": data})

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
            context = {'form': form, "invoice": invoice, 'user_belongs_to_group': user_belongs_to_group, "items": items,
                       'invoiceSlug': invoiceSlug, 'countiesSum': counties,
                       'measurementData': measurementSystemNumberList}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group, }
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

    def post(self, request, invoiceSlug):
        user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
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
            context = {'form': form, 'invoice': invoice, 'user_belongs_to_group': user_belongs_to_group, 'items': items,
                       'invoiceSlug': invoiceSlug}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group, }
            logger.error('Error: %s', e)
            return render(request, self.template_error, context)


class DeleteInvoiceView(View):
    template_error = 'main/error.html'

    def get(self, request, invoiceSlug):
        try:
            invoice = get_object_or_404(Invoice, slug=invoiceSlug)
            invoice.delete()
            return redirect("main:invoiceSite")
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e}
            logger.error("Error: %s", e)
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
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


class CreateCSVForItems(View):
    template_error = 'main/error.html'

    def get(self, request, invoice_id):
        user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            invoice = get_object_or_404(Invoice, pk=invoice_id)
            # ---------------------------------------------
            objectsForFile = []
            for item in invoice.items.all():
                sum_value = item.sum
                exist = False
                print(sum_value)
                for row in objectsForFile:
                    if item.unit.county_swop.name == row['county']:
                        row['sum'] += sum_value
                        exist = True
                        print(item)
                if not exist:
                    objectsForFile.append(
                        {'section': item.section.section, 'county': item.unit.county_swop.name, 'sum': item.sum})

            print(objectsForFile)
            # ---------------------------------------------

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="Koszty faktury {invoice}.csv"'
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
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group}
            logger.error("Error: %s", e)
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)
