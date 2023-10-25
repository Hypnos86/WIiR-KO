from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib import messages
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
            # Tworzenie i przypisywanie zmiennej grup
            admin, created = Group.objects.get_or_create(name="AdminZRiWT")
            viewers, created = Group.objects.get_or_create(name="Viewers")
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
            counties = CountyCard.objects.all()
            # print(request.user.groups.all())
            # if not request.user.is_authenticated :
            if not request.user.is_authenticated or not (
                    admin in request.user.groups.all() or viewers in request.user.groups.all()):
                counties = counties.exclude(name="KWP Poznań")

            context = {'counties': counties, 'user_belongs_to_group': user_belongs_to_group}
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
                    messages.success(request, 'Zalogowano pomyślnie.')
                    return redirect('main:welcome')  # Przekierowanie po zalogowaniu
                else:
                    # Obsługa błędnych danych logowania
                    messages.error(request, 'Błędna nazwa użytkownika lub hasło.')
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
            year = currentDate.current_year()
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
            units = Unit.objects.filter(county_unit__slug=slug)
            activeUnits = len(units.filter(status=True))
            archiveUnits = len(units.filter(status=False))
            county = CountyCard.objects.get(slug=slug)
            context = {'units': units, 'slug': slug, 'county': county, 'activeUnits': activeUnits,
                       'archiveUnits': archiveUnits, 'slugCounty': slug, 'year': year,
                       'user_belongs_to_group': user_belongs_to_group}
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
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
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
            context = {'unit': unit, 'paragraph_data': paragraph_data, 'user_belongs_to_group': user_belongs_to_group,
                       'year': currentYear, 'countyCardSlug': countyCardSlug}
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
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
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
                           'archiveUnits': archiveUnits, 'user_belongs_to_group': user_belongs_to_group}
                return render(request, self.template_name, context)
            else:

                context = {'units': units, "search": search, 'activeUnits': activeUnits, 'archiveUnits': archiveUnits,
                           'user_belongs_to_group': user_belongs_to_group}
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
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
            currentYear = CurrentDate().current_year()
            paragraphs = Paragraph.objects.all()
            counties = County.objects.all()

            items = []
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

            context = {'counties': counties, 'user_belongs_to_group': user_belongs_to_group, 'currentYear': currentYear,
                       'paragraphs': paragraphs, 'title': title}
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
            countySlug = unit.county_unit.slug
            items = InvoiceItems.objects.filter(paragraph__slug=paragraphSlug, unit__id=unit.id)
            yearsSet = set([year.invoice_id.date.year for year in items])
            years = sorted(yearsSet, reverse=True)
            context = {'countySlug': countySlug, 'unitSlug': unitSlug, 'paragraphSlug': paragraphSlug, 'years': years,
                       'unitCost': False}
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
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
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

                context = {'invoices': invoices, 'user_belongs_to_group': user_belongs_to_group, 'query': query, 'q': q}
                return render(request, self.template_name, context)
            else:
                context = {'invoices': invoices_pages, 'user_belongs_to_group': user_belongs_to_group, 'search': search}
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
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
            invoice = get_object_or_404(Invoice, pk=id)
            items = invoice.items.all()
            context = {'invoice': invoice, 'user_belongs_to_group': user_belongs_to_group, 'items': items, 'id': id}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CostsDetailsListView(View):
    template_name = 'main/cost_list_unit_details.html'
    template_error = 'main/error.html'
    paginate_by = 40

    def get(self, request, countyCardSlug, unitSlug, paragraphSlug, year):
        try:
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
            unit = get_object_or_404(Unit, slug=unitSlug)
            items = InvoiceItems.objects.filter(unit__slug=unitSlug, paragraph__slug=paragraphSlug,
                                                invoice_id__date__year=year).order_by('-invoice_id__date')
            lastUpdate = items.last()
            paragraph = Paragraph.objects.get(slug=paragraphSlug)

            paginator = Paginator(items, self.paginate_by)
            page_number = request.GET.get('page')
            itemsList = paginator.get_page(page_number)

            unitOfMeasure = None
            for parEnum in ParagraphEnum:
                if paragraphSlug == parEnum.value[0]:
                    unitOfMeasure = parEnum.value[1]

            context = {'unit': unit, 'items': itemsList, 'year': year, 'paragraph': paragraph,
                       'countyCardSlug': countyCardSlug, 'lastUpdate': lastUpdate, 'unitOfMeasure': unitOfMeasure,
                       'user_belongs_to_group': user_belongs_to_group}
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
        user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
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

                    context = {'items': items, 'user_belongs_to_group': user_belongs_to_group, 'paragraph': paragraph,
                               'unitOfMeasure': unitOfMeasure,
                               "query": query, 'q': q}
                    return render(request, self.template_name_media, context)
                else:
                    context = {'items': items_pages, 'user_belongs_to_group': user_belongs_to_group,
                               'paragraph': paragraph, 'unitOfMeasure': unitOfMeasure,
                               "search": search, 'q': q}
                    return render(request, self.template_name_media, context)

            except Exception as e:
                context = {'error': e}
                logger.error("Error: %s", e)
                return render(request, self.template_error, context)
        else:
            try:
                paragraph = Paragraph.objects.get(slug=paragraphSlug)
                items = InvoiceItems.objects.filter(paragraph__slug=paragraphSlug)

                paginator = Paginator(items, self.paginate_by)
                page_number = request.GET.get('page')
                items_pages = paginator.get_page(page_number)

                query = "Wyczyść"
                search = "Szukaj"
                q = request.GET.get("q")

                if q:
                    items = items.filter(invoice_id__no_invoice__icontains=q) \
                            | items.filter(invoice_id__doc_types__type__startswith=q) \
                            | items.filter(unit__unit_full_name__icontains=q) \
                            | items.filter(information__icontains=q)

                    context = {'items': items, 'user_belongs_to_group': user_belongs_to_group, 'paragraph': paragraph,
                               "query": query, 'q': q}
                    return render(request, self.template_name_general, context)
                else:
                    context = {'items': items_pages, 'user_belongs_to_group': user_belongs_to_group,
                               'paragraph': paragraph,
                               "search": search, 'q': q}
                    return render(request, self.template_name_general, context)

            except Exception as e:
                context = {'error': e}
                logger.error("Error: %s", e)
                return render(request, self.template_error, context)


class UnitDetailsView(View):
    template_name = 'main/unit_details_info.html'
    template_error = 'main/error.html'

    def get(self, request, unitSlug):
        try:
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
            title = 'Grupa 6 - Administracja i utrzymanie obiektów'
            unit = get_object_or_404(Unit, slug=unitSlug)
            paragraphs = Paragraph.objects.all()

            items = unit.items.all()
            tableObjects = []

            for item in items:
                year = item.invoice_id.date_of_payment.year
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

            context = {'unit': unit, 'user_belongs_to_group': user_belongs_to_group, 'paragraphs': paragraphs,
                       'title': title, 'tableObjects': tableObjects}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class MediaInfoUnitView(View):
    template_name = 'main/modal_info_unit.html'
    template_error = 'main/error.html'

    def get(self, request, id):
        try:
            title = 'Zużycie mediów'
            unit = get_object_or_404(Unit, pk=id)
            paragraphsModel = Paragraph.objects.all().filter(paragraph__contains='4260')
            print(paragraphsModel)
            items = unit.items.all().exclude(contract_types__type__icontains='Sprzedaż')
            tableObjects = []

            for item in items:
                year = item.invoice_id.date_of_payment.year
                year_exist = False
                for year_entry in tableObjects:
                    if year_entry['year'] == year:
                        for data_entry in year_entry['data']:
                            if data_entry['paragraph'] == item.paragraph.paragraph:
                                data_entry['consumption'] += item.consumption
                                year_exist = True
                                break

                        if not year_exist:
                            year_entry['data'].append(
                                {'paragraph': item.paragraph.paragraph, 'consumption': item.consumption})
                            year_exist = True

                if not year_exist:
                    new_data_entry = {'paragraph': item.paragraph.paragraph, 'consumption': item.consumption}
                    year_entry = {'year': year, 'data': [new_data_entry]}
                    tableObjects.append(year_entry)

            # Dodanie zerowych sum dla paragrafów, które nie miały wydatków w danym roku
            all_paragraphs = set(paragraph['paragraph'] for paragraph in paragraphsModel.values('paragraph'))
            for year_entry in tableObjects:
                existing_paragraphs = set(data_entry['paragraph'] for data_entry in year_entry['data'])
                missing_paragraphs = all_paragraphs - existing_paragraphs
                for missing_paragraph in missing_paragraphs:
                    year_entry['data'].append({'paragraph': missing_paragraph, 'consumption': 0})

            context = {'title': title, 'unit': unit, 'paragraphs': paragraphsModel, 'tableObjects': tableObjects}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CountyCostUnitListView(View):
    template_name = 'main/cost_list_county_unit.html'
    template_error = 'main/error.html'

    def get(self, request, countyCardSlug, year):
        try:
            user_belongs_to_group = request.user.groups.filter(name='AdminZRiWT').exists()
            county_unit = CountyCard.objects.get(slug=countyCardSlug)
            units = Unit.objects.filter(county_unit=county_unit)
            paragraphs = Paragraph.objects.all()
            objectDatas = []

            for unit in units:
                policeUnit = f'{unit.unit_full_name}'
                status = unit.status
                items = unit.items.all()
                costObjectDict = {}

                # Inicjujemy kwoty dla wszystkich paragrafów jako 0
                for paragraph in paragraphs:
                    costObjectDict[paragraph.paragraph] = 0

                for item in items:
                    if item.invoice_id.date_of_payment.year == year:
                        paragraph = item.paragraph.paragraph
                        sumUnit = item.sum
                        # if paragraph in costObjectDict:
                        #     costObjectDict[paragraph] += sumUnit
                        # else:
                        #     costObjectDict[paragraph] = sumUnit
                        # Aktualizujemy kwotę dla danego paragrafu
                        costObjectDict[paragraph] += sumUnit

                costObjectList = [{'paragraph': paragraph, 'sum': sumUnit} for paragraph, sumUnit in
                                  costObjectDict.items()]

                objectDatas.append({'unit': policeUnit, 'status': status, 'objects': costObjectList})

            # Tworzymy słownik do przechowywania sum paragrafów
            paragraphSums = {}

            # Iterujemy przez objectDatas
            for unit_data in objectDatas:
                for object in unit_data['objects']:
                    paragraph = object['paragraph']
                    sum_value = object['sum']
                    # Dodajemy sumę do istniejącej sumy paragrafu lub inicjujemy nową
                    if paragraph in paragraphSums:
                        paragraphSums[paragraph] += sum_value
                    else:
                        paragraphSums[paragraph] = sum_value

            # Teraz paragraph_sums zawiera sumy paragrafów
            # Możesz je przekazać do szablonu lub wyświetlić
            # for paragraph, sum_value in paragraphSums.items():
            #     print(f'Paragraf: {paragraph}, Suma: {sum_value}')

            # print(objectDatas)
            context = {'county': county_unit, 'user_belongs_to_group': user_belongs_to_group, 'year': year,
                       'paragraphs': paragraphs, 'slugCounty': countyCardSlug,
                       "items": objectDatas, 'paragraphSums': paragraphSums}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)
