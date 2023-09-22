import decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from main.models import CountyCard, HelpInfo
from units.models import Unit, County
from invoices.models import Invoice, InvoiceItems, Paragraph, Section
from enum import Enum
import logging
import datetime

logger = logging.getLogger(__name__)


class ParagraphEnum(Enum):
    MEDIA1 = ['4260-01', 'kWh']
    MEDIA2 = ['4260-02', 'GJ']
    MEDIA3 = ['4260-03', 'kWh']
    MEDIA4 = ['4260-04', 'm3']


class CurrentDate():
    def current_year(self):
        return datetime.date.today().year

    def current_date(self):
        return datetime.date.today()


currentDate = CurrentDate()


# Create your views here.
class WelcomeView(View):
    template_name = 'main/welcome.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            counties = CountyCard.objects.all()
            if not request.user.is_authenticated:
                counties = counties.exclude(name="KWP Poznań")

            context = {'counties': counties}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class LoginView(View):
    template_name = 'main/registration/login.html'
    template_welcome = 'main/welcome.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            return render(request, self.template_name)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

    def post(self, request):
        try:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('main:welcome')  # Przekierowanie po zalogowaniu
                else:
                    # Obsługa błędnych danych logowania
                    return redirect('main:welcome')
                    # return render(request, self.template_welcome, {'error_message': 'Błędna nazwa użytkownika lub hasło.'})
            else:
                return render(request, self.template_name)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class HelpModalView(View):
    template_name = 'main/modal_help.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            text = HelpInfo.objects.last()
            context = {'text': text}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class UnitsListaMainView(View):
    template_name = 'main/list_units.html'
    template_error = 'main/error.html'

    def get(self, request, slug):
        try:
            units = Unit.objects.filter(county_unit__slug=slug)
            activeUnits = len(units.filter(status=True))
            archiveUnits = len(units.filter(status=False))
            county = CountyCard.objects.get(slug=slug)
            context = {'units': units, 'slug': slug, 'county': county, 'activeUnits': activeUnits,
                       'archiveUnits': archiveUnits, 'slugCounty': slug}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CostListMainView(View):
    template_name = 'main/cost_list_unit_main.html'
    template_error = 'main/error.html'

    def get(self, request, countyCardSlug, unitSlug):
        try:
            currentYear = currentDate.current_year()
            unit = get_object_or_404(Unit, slug=unitSlug)
            invoiceItems = InvoiceItems.objects.filter(unit__id=unit.id, invoice_id__date__year=currentYear)
            paragraphs = Paragraph.objects.all()
            paragraph_data = []

            # for paragraph in paragraphs:
            #     items = invoiceItems.filter(paragraph=paragraph)[:4]
            #     paragraph_data.append({'paragraph': paragraph, 'items': items})
            for paragraph in paragraphs:
                paragraph_items = invoiceItems.filter(paragraph=paragraph).order_by('-invoice_id__date')[:4]
                items = []
                for item in paragraph_items:
                    selected_properties = {
                        'id': item.invoice_id.id,
                        'date_receipt': item.invoice_id.date_receipt,
                        'date': item.invoice_id.date,
                        'no_invoice': item.invoice_id.no_invoice,
                        'doc_types': item.invoice_id.doc_types,
                        'contract_types': item.contract_types,
                        'period_from': item.period_from,
                        'period_to': item.period_to,
                        'measurementSystemNumber': item.measurementSystemNumber,
                        'counterReading': item.counterReading,
                        'consumption': item.consumption,
                        'paragraph': str(item.paragraph),
                        'sum': item.sum,
                        'creation_date': item.creation_date,
                        'invoice_slug': item.invoice_id.slug
                        # Dodaj inne wybrane propertisy tutaj
                    }
                    items.append(selected_properties)
                paragraph_data.append({'paragraph': paragraph, 'items': items})
            context = {'unit': unit, 'paragraph_data': paragraph_data, 'currentYear': currentYear,
                       'countyCardSlug': countyCardSlug}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class UnitsView(LoginRequiredMixin, View):
    template_name = 'main/site_units.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            units = Unit.objects.all().order_by('county_unit__id_order')
            activeUnits = len(units.filter(status=True))
            archiveUnits = len(units.filter(status=False))

            query = "Wyczyść"
            search = "Szukaj"
            q = request.GET.get("q")

            if q:
                units = units.filter(unit_full_name__icontains=q) \
                        | units.filter(city__icontains=q) \
                        | units.filter(type__type_short__icontains=q) \
                        | units.filter(manager__icontains=q) \
                        | units.filter(information__icontains=q)

                context = {'units': units, "query": query, 'q': q, 'activeUnits': activeUnits,
                           'archiveUnits': archiveUnits}
                return render(request, self.template_name, context)
            else:

                context = {'units': units, "search": search, 'activeUnits': activeUnits, 'archiveUnits': archiveUnits}
                return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class StatisticsView(LoginRequiredMixin, View):
    template_name = 'main/site_statistics.html'
    template_error = 'main/error.html'

    def get(self, request):

        try:
            title = 'Grupa 6 - Administracja i utrzymanie obiektów'
            currentYear = CurrentDate().current_year()
            paragraphs = Paragraph.objects.all()
            counties = County.objects.all()

            items = []
            # TODO rozrysowac obiekt jak ma wygladać
            for paragraph in paragraphs:
                sum = 0
                units = []
                for item in paragraph.items.all():
                    sum += item.sum
                    unit = item.unit.county_swop
                    units.append({'unit': unit, 'sum': sum})

                items.append({'paragraph': paragraph, 'units': units})

            for item in items:
                print(item)

            context = {'counties': counties, 'currentYear': currentYear, 'paragraphs': paragraphs, 'title': title}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class UsersSiteView(LoginRequiredMixin, View):
    template = 'main/site_users.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            users = User.objects.all()
            context = {'users': users}
            return render(request, self.template, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ArchiveYearCostListView(View):
    template_name = 'main/modal_archive_years.html'
    template_error = 'main/error.html'

    def get(self, request, unitSlug, paragraphSlug):
        try:
            currentYear = currentDate.current_year()
            unit = Unit.objects.get(slug=unitSlug)
            items = InvoiceItems.objects.filter(paragraph__slug=paragraphSlug, unit__id=unit.id)
            yearsSet = set([year.invoice_id.date.year for year in items])
            years = sorted(yearsSet, reverse=True)
            context = {'unitSlug': unitSlug, 'paragraph_slug': paragraphSlug, 'years': years, 'unitCost': False}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ArchiveYearUnitCostListView(View):
    template_name = 'main/modal_archive_years.html'
    template_error = 'main/error.html'

    def get(self, request, slugCounty):
        try:
            currentYear = currentDate.current_year()
            # unit = Unit.objects.filter(county_unit__slug=slugCounty)

            items = InvoiceItems.objects.filter(unit__county_unit__slug=slugCounty)
            yearsSet = set([year.invoice_id.date.year for year in items])
            years = sorted(yearsSet, reverse=True)
            context = {'slugCounty': slugCounty, 'years': years, 'unitCost': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class InvoicesListView(LoginRequiredMixin, View):
    template_name = 'main/site_invoice.html'
    template_error = 'main/error.html'
    paginate_by = 100

    def get(self, request):
        try:
            invoices = Invoice.objects.all()

            paginator = Paginator(invoices, self.paginate_by)
            page_number = request.GET.get('page')
            invoices_pages = paginator.get_page(page_number)

            query = "Wyczyść"
            search = "Szukaj"
            q = request.GET.get("q")

            if q:
                invoices = invoices.filter(no_invoice__icontains=q) \
                           | invoices.filter(sum__icontains=q) \
                           | invoices.filter(items__paragraph__paragraph__icontains=q) \
                           | invoices.filter(doc_types__type__startswith=q) \
                           | invoices.filter(information__icontains=q)

                invoicesSet = set(invoices)
                invoices = sorted(invoicesSet, key=lambda x: x.date, reverse=True)

                context = {'invoices': invoices, "query": query, 'q': q}
                return render(request, self.template_name, context)
            else:
                context = {'invoices': invoices_pages, "search": search}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class InvoiceInfoView(View):
    template_name = 'main/modal_info_invoice.html'
    template_error = 'main/error.html'

    def get(self, request, id):
        try:
            invoice = get_object_or_404(Invoice, pk=id)
            items = invoice.items.all()
            context = {'invoice': invoice, 'items': items, 'id': id}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CostsDetailsListView(View):
    template_name = 'main/cost_list_unit_details.html'
    template_error = 'main/error.html'
    paginate_by = 40

    def get(self, request, countyCardSlug, unitSlug, paragraphSlug):
        try:
            currentYear = CurrentDate().current_year()
            unit = get_object_or_404(Unit, slug=unitSlug)
            items = InvoiceItems.objects.filter(unit__slug=unitSlug, paragraph__slug=paragraphSlug,
                                                invoice_id__date__year=currentYear).order_by('-invoice_id__date')
            lastUpdate = items.last()
            paragraph = Paragraph.objects.get(slug=paragraphSlug)

            paginator = Paginator(items, self.paginate_by)
            page_number = request.GET.get('page')
            itemsList = paginator.get_page(page_number)

            unitOfMeasure = None
            for parEnum in ParagraphEnum:
                if paragraphSlug == parEnum.value[0]:
                    unitOfMeasure = parEnum.value[1]

            context = {'unit': unit, 'items': itemsList, 'currentYear': currentYear, 'paragraph': paragraph,
                       'countyCardSlug': countyCardSlug, 'lastUpdate': lastUpdate, 'unitOfMeasure': unitOfMeasure}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ParagraphModalView(View):
    template_name = 'main/modal_paragraph.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            paragraphs = Paragraph.objects.all()
            context = {'paragraphs': paragraphs}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ParagraphCostListView(LoginRequiredMixin, View):
    template_name_media = 'main/cost_list_media.html'
    template_name_general = 'main/cost_list_general.html'
    template_error = 'main/error.html'
    paginate_by = 80

    def get(self, request, paragraphSlug):
        if paragraphSlug in [
            ParagraphEnum.MEDIA1.value[0], ParagraphEnum.MEDIA2.value[0], ParagraphEnum.MEDIA3.value[0],
            ParagraphEnum.MEDIA4.value[0]]:
            try:
                paragraph = Paragraph.objects.get(slug=paragraphSlug)
                items = InvoiceItems.objects.filter(paragraph__slug=paragraphSlug)

                paginator = Paginator(items, self.paginate_by)
                page_number = request.GET.get('page')
                items_pages = paginator.get_page(page_number)

                unitOfMeasure = None
                for parEnum in ParagraphEnum:
                    if paragraphSlug == parEnum.value[0]:
                        unitOfMeasure = parEnum.value[1]

                query = "Wyczyść"
                search = "Szukaj"
                q = request.GET.get("q")

                if q:
                    items = items.filter(invoice_id__no_invoice__icontains=q) \
                            | items.filter(invoice_id__doc_types__type__startswith=q) \
                            | items.filter(unit__unit_full_name__icontains=q) \
                            | items.filter(information__icontains=q)

                    context = {'items': items, 'paragraph': paragraph, 'unitOfMeasure': unitOfMeasure,
                               "query": query, 'q': q}
                    return render(request, self.template_name_media, context)
                else:
                    context = {'items': items_pages, 'paragraph': paragraph, 'unitOfMeasure': unitOfMeasure,
                               "search": search, 'q': q}
                    return render(request, self.template_name_media, context)

            except Exception as e:
                context = {'error': e}
                logger.error("Error: %s", e)
                return render(request, self.template_error, context)
        else:
            try:
                context = {}
                return render(request, self.template_name_general, context)
            except Exception as e:
                context = {'error': e}
                logger.error("Error: %s", e)
                return render(request, self.template_error, context)


class UnitDetailsView(View):
    template_name = 'main/unit_details_info.html'
    template_error = 'main/error.html'

    def get(self, request, unitSlug):
        title = 'Grupa 6 - Administracja i utrzymanie obiektów'
        unit = get_object_or_404(Unit, slug=unitSlug)
        paragraphs = Paragraph.objects.all()

        items = unit.items.all()
        tableObjects = []

        for item in items:
            year = item.invoice_id.date.year
            year_exist = False

            for year_entry in tableObjects:
                if year_entry['year'] == year:
                    for data_entry in year_entry['data']:
                        if data_entry['paragraph'] == item.paragraph.paragraph:
                            data_entry['sum'] += item.sum
                            year_exist = True
                            break

                    if not year_exist:
                        year_entry['data'].append({'paragraph': item.paragraph.paragraph, 'sum': item.sum})
                        year_exist = True

            if not year_exist:
                new_data_entry = {'paragraph': item.paragraph.paragraph, 'sum': item.sum}
                year_entry = {'year': year, 'data': [new_data_entry]}
                tableObjects.append(year_entry)

        # Dodanie zerowych sum dla paragrafów, które nie miały wydatków w danym roku
        all_paragraphs = set(paragraph['paragraph'] for paragraph in paragraphs.values('paragraph'))
        for year_entry in tableObjects:
            existing_paragraphs = set(data_entry['paragraph'] for data_entry in year_entry['data'])
            missing_paragraphs = all_paragraphs - existing_paragraphs
            for missing_paragraph in missing_paragraphs:
                year_entry['data'].append({'paragraph': missing_paragraph, 'sum': 0})

        context = {'unit': unit, 'paragraphs': paragraphs, 'title': title, 'tableObjects': tableObjects}
        return render(request, self.template_name, context)
