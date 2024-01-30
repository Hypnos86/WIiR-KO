from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import csv
from io import BytesIO
from django.contrib.auth.models import User
from main.models import CountyCard, HelpInfo
from units.models import Unit, County, TypeUnit
from invoices.models import Invoice, InvoiceItems, Paragraph, Section, DocumentTypes, ContractTypes
from enum import Enum
import logging
import datetime
import matplotlib.pyplot as plt

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
    method = 'WelcomeView'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
        try:
            yearObject = CurrentDate()
            year = yearObject.current_year()

            # Tworzenie i przypisywanie zmiennej grup
            admin, created = Group.objects.get_or_create(name="AdminZRiWT")
            viewers, created = Group.objects.get_or_create(name="Viewers")

            # Pobieranie i sprawdzanie, czy istnieją obiekty w bazie
            counties = CountyCard.objects.all()
            if not counties.exists():
                CountyCard.create_county_cards()

            sections = Section.objects.all()
            if not sections.exists():
                Section.create_section()

            paragraphs = Paragraph.objects.all()
            if not paragraphs.exists():
                Paragraph.create_paragraph()

            # Tworzenie typów dokumentów
            types = DocumentTypes.objects.all()
            if not types.exists():
                DocumentTypes.create_type()

            # Tworzenie typów umów
            contract_types = ContractTypes.objects.all()
            if not contract_types.exists():
                ContractTypes.create_contract_types()

            # Tworzenie grup
            groups = Group.objects.all()
            if not groups.exists():
                Group.create_group()

            county = County.objects.all()
            if not county.exists():
                County.create_county()

            type_unit = TypeUnit.objects.all()
            if not type_unit.exists():
                TypeUnit.create_type_unit()

            if not request.user.is_authenticated or not (
                    admin in request.user.groups.all() or viewers in request.user.groups.all()):
                counties = counties.exclude(name="KWP Poznań")

            context = {'counties': counties, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'year': year}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class LoginView(View):
    template_name = 'main/registration/login.html'
    template_welcome = 'main/welcome.html'
    template_error = 'main/error.html'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            return render(request, self.template_name)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group}
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
                    messages.success(request, 'Zalogowano pomyślnie')
                    return redirect('main:welcome')  # Przekierowanie po zalogowaniu
                else:
                    # Obsługa błędnych danych logowania
                    messages.error(request, 'Błędna nazwa użytkownika lub hasło')
                    return redirect('main:welcome')
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
            content = HelpInfo.objects.all()
            if not content.exists():
                HelpInfo.create_support()

            aut = [65, 117, 116, 111, 114, 32, 97, 112, 108, 105, 107, 97, 99, 106, 105, 58, 32, 75, 97, 109, 105, 108,
                   32, 75, 117, 98, 105, 97, 107, 32, 50, 48, 50, 51]
            # inAut = [101, 109, 97, 105, 108, 58, 32, 107, 117, 98, 105, 97, 107, 46, 107, 97, 109, 105, 108, 50, 51, 64,
            #          103, 109, 97, 105, 108, 46, 99, 111, 109]
            mainEnco = ''.join([chr(val) for val in aut])
            # inAutEnco = ''.join([chr(val) for val in inAut])
            context = {'content': content.last(), 'mainEnco': mainEnco}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class UnitsListMainView(View):
    template_name = 'main/list_units.html'
    template_error = 'main/error.html'
    method = 'UnitsListMainView'

    def get(self, request, countySlug):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
        try:
            yearObject = CurrentDate()
            year = yearObject.current_year()
            units = Unit.objects.filter(county_unit__slug=countySlug)
            activeUnits = len(units.filter(status=True))
            archiveUnits = len(units.filter(status=False))
            county = CountyCard.objects.get(slug=countySlug)
            context = {'units': units,
                       'slug': countySlug, 'county': county, 'slugCounty': countySlug,
                       'activeUnits': activeUnits,
                       'archiveUnits': archiveUnits, 'year': year, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group,
                       'user_belongs_to_group': user_belongs_to_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class TypeUnitsListView(LoginRequiredMixin, View):
    template_name = 'main/site_units.html'
    template_error = 'main/error.html'
    method = 'UnitsView'

    def get(self, request, type_units):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()

        try:
            currentYear = currentDate.current_year()
            units = Unit.objects.all().filter(type__type_short=type_units).order_by('county_unit__id_order')
            activeUnits = len(units.filter(status=True))
            archiveUnits = len(units.filter(status=False))
            policeManager = units.filter(manager='Policja').count()
            othersManager = units.exclude(manager='Policja').count()
            slugTypeUnits = TypeUnit.objects.get(type_short=type_units)
            typesUnit = TypeUnit.objects.all()

            typesList = []
            for element in typesUnit:
                if element.type_short in ('KMP', 'KPP', 'KP', 'PP'):
                    item = {'index': element.type_short.lower(), 'type_short': element.type_short,
                            'type_full': element.type_full}

                    typesList.append(item)
            query = "Wyczyść"
            search = "Szukaj"
            q = request.GET.get("q")

            if q:
                units = units.filter(unit_full_name__icontains=q) \
                        | units.filter(county_swop__name__icontains=q) \
                        | units.filter(city__icontains=q) \
                        | units.filter(type__type_full__icontains=q) \
                        | units.filter(manager__icontains=q) \
                        | units.filter(information__icontains=q)

                context = {'year': currentYear, 'units': units, "query": query, 'q': q, 'activeUnits': activeUnits,
                           'archiveUnits': archiveUnits, 'typesList': typesList, 'slugTypeUnits': slugTypeUnits,
                           'policeManager': policeManager, 'othersManager': othersManager,
                           'user_belongs_to_group': user_belongs_to_group,
                           'user_belongs_to_admin_group': user_belongs_to_admin_group}
                return render(request, self.template_name, context)
            else:

                context = {'year': currentYear, 'units': units, "search": search, 'activeUnits': activeUnits,
                           'archiveUnits': archiveUnits, 'typesList': typesList, 'slugTypeUnits': slugTypeUnits,
                           'policeManager': policeManager, 'othersManager': othersManager,
                           'user_belongs_to_group': user_belongs_to_group,
                           'user_belongs_to_admin_group': user_belongs_to_admin_group}
                return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CostListMainView(View):
    template_name = 'main/cost_list_unit_main.html'
    template_error = 'main/error.html'
    method = 'CostListMainView'

    def get(self, request, countyCardSlug, unitSlug, year):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
        try:
            unit = get_object_or_404(Unit, slug=unitSlug)
            invoiceItems = InvoiceItems.objects.filter(unit__id=unit.id, invoice_id__date__year=year)
            paragraphs = Paragraph.objects.all()
            paragraph_data = []

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
                       'user_belongs_to_admin_group': user_belongs_to_admin_group,
                       'year': year, 'countyCardSlug': countyCardSlug}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class UnitsView(LoginRequiredMixin, View):
    template_name = 'main/site_units.html'
    template_error = 'main/error.html'
    method = 'UnitsView'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
        try:
            currentYear = currentDate.current_year()
            units = Unit.objects.all().order_by('county_unit__id_order')
            activeUnits = len(units.filter(status=True))
            archiveUnits = len(units.filter(status=False))
            policeManager = units.filter(manager='Policja').count()
            othersManager = units.exclude(manager='Policja').count()
            typesUnit = TypeUnit.objects.all()

            typesList = []
            index = 1
            for element in typesUnit:
                if element.type_short in ('KMP', 'KPP', 'KP', 'PP'):
                    item = {'index': element.type_short.lower(), 'type_short': element.type_short,
                            'type_full': element.type_full}
                    index += 1
                    typesList.append(item)

            query = "Wyczyść"
            search = "Szukaj"
            q = request.GET.get("q")

            if q:
                units = units.filter(unit_full_name__icontains=q) \
                        | units.filter(county_swop__name__icontains=q) \
                        | units.filter(city__icontains=q) \
                        | units.filter(type__type_full__icontains=q) \
                        | units.filter(manager__icontains=q) \
                        | units.filter(information__icontains=q)

                activeUnits = len(units.filter(status=True))
                archiveUnits = len(units.filter(status=False))
                policeManager = units.filter(manager='Policja').count()
                othersManager = units.exclude(manager='Policja').count()

                context = {'year': currentYear, 'units': units, "query": query, 'q': q, 'typesList': typesList,
                           'activeUnits': activeUnits, 'archiveUnits': archiveUnits, 'policeManager': policeManager,
                           'othersManager': othersManager, 'user_belongs_to_group': user_belongs_to_group,
                           'user_belongs_to_admin_group': user_belongs_to_admin_group}
                return render(request, self.template_name, context)
            else:

                context = {'year': currentYear, 'units': units, "search": search, 'activeUnits': activeUnits,
                           'archiveUnits': archiveUnits, 'typesList': typesList, 'policeManager': policeManager,
                           'othersManager': othersManager, 'user_belongs_to_group': user_belongs_to_group,
                           'user_belongs_to_admin_group': user_belongs_to_admin_group}
                return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class StatisticsView(LoginRequiredMixin, View):
    template_name = 'main/site_statistics.html'
    template_error = 'main/error.html'
    method = 'StatisticsView'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
        try:
            title = 'Grupa 6 - Administracja i utrzymanie obiektów'
            paragraphs = Paragraph.objects.all()
            counties = County.objects.all()
            yearObject = CurrentDate()
            year = yearObject.current_year()

            objectDatas = []

            for county in counties:
                sectionObject = county.section.first()
                section = sectionObject.section
                units = county.unit.all()
                costObjectDict = {}

                for paragraph in paragraphs:
                    costObjectDict[paragraph.paragraph] = 0

                for unit in units:
                    # Filtruj elementy na podstawie roku płatności
                    items = unit.items.filter(invoice_id__date_of_payment__year=year)

                    for item in items:
                        costObjectDict[item.paragraph.paragraph] += item.sum

                costObjectList = [{'paragraph': paragraph, 'sum': sumUnit} for paragraph, sumUnit in
                                  costObjectDict.items()]
                objectDatas.append({'county': county.name, 'section': section, 'data': costObjectList})

            paragraphSums = {}

            for data in objectDatas:
                for item in data['data']:
                    paragraph = item['paragraph']
                    sum_value = item['sum']
                    # Dodajemy sumę do istniejącej sumy paragrafu lub inicjujemy nową
                    if paragraph in paragraphSums:
                        paragraphSums[paragraph] += sum_value
                    else:
                        paragraphSums[paragraph] = sum_value
            # -------------
            # fig, ax = plt.subplots()  # Inicjalizacja obiektu figury i osi
            par = '4260-01'
            graph_data = []

            for item in objectDatas:
                for data in item['data']:
                    if par == data['paragraph']:
                        graph_data.append({'county': item['county'], 'sum': data['sum']})

            # Wygenerowanie wykresu słupkowego na podstawie danych z graph_data
            x = [county['county'] for county in graph_data]
            y = [sum_graph['sum'] for sum_graph in graph_data]
            # ax.bar([county['county'] for county in graph_data], [sum_graph['sum'] for sum_graph in graph_data])

            # Zapisanie wykresu do pliku nazwa.jng (należy sprawdzić, czy chodziło o .png czy .jpg)
            # plt.savefig('nazwa.png')

            context = {'objectDatas': objectDatas, 'paragraphSums': paragraphSums,
                       'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'title': title,
                       'paragraphs': paragraphs, 'year': year, 'statisticsSite': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class StatisticsYearView(LoginRequiredMixin, View):
    template_name = 'main/site_statistics.html'
    template_error = 'main/error.html'
    method = 'StatisticsYearView'

    def get(self, request, year):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
        try:
            title = 'Grupa 6 - Administracja i utrzymanie obiektów'
            paragraphs = Paragraph.objects.all()
            counties = County.objects.all()

            # ----------------------------------------
            objectDatas = []

            for county in counties:
                sectionObject = county.section.first()
                section = sectionObject.section
                units = county.unit.all()
                costObjectDict = {}

                for paragraph in paragraphs:
                    costObjectDict[paragraph.paragraph] = 0

                for unit in units:
                    # Filtruj elementy na podstawie roku płatności
                    items = unit.items.filter(invoice_id__date_of_payment__year=year)

                    for item in items:
                        costObjectDict[item.paragraph.paragraph] += item.sum

                costObjectList = [{'paragraph': paragraph, 'sum': sumUnit} for paragraph, sumUnit in
                                  costObjectDict.items()]
                objectDatas.append({'county': county.name, 'section': section, 'data': costObjectList})

            # Tworzenie podsumowania i sum paragrafów
            paragraphSums = {}

            for data in objectDatas:
                for item in data['data']:
                    paragraph = item['paragraph']
                    sum_value = item['sum']
                    # Dodajemy sumę do istniejącej sumy paragrafu lub inicjujemy nową
                    if paragraph in paragraphSums:
                        paragraphSums[paragraph] += sum_value
                    else:
                        paragraphSums[paragraph] = sum_value

            context = {'objectDatas': objectDatas, 'paragraphSums': paragraphSums,
                       'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'title': title,
                       'paragraphs': paragraphs, 'year': year, 'statisticYear': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class UsersSiteView(LoginRequiredMixin, View):
    template = 'main/site_users.html'
    template_error = 'main/error.html'
    method = 'UsersSiteView'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
        try:
            users = User.objects.all()
            context = {'users': users, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group}
            return render(request, self.template, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ArchiveYearCostListView(View):
    template_name = 'main/modal_archive_years.html'
    template_error = 'main/error.html'
    method = 'ArchiveYearCostListView'

    def get(self, request, unitSlug, paragraphSlug):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            unit = Unit.objects.get(slug=unitSlug)
            countySlug = unit.county_unit.slug
            items = InvoiceItems.objects.filter(paragraph__slug=paragraphSlug, unit__id=unit.id)
            yearsSet = set([year.invoice_id.date.year for year in items])
            years = sorted(yearsSet, reverse=True)

            context = {'countySlug': countySlug, 'unitSlug': unitSlug, 'paragraphSlug': paragraphSlug, 'years': years,
                       'unitCost': False, 'archiveYears': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ArchiveYearUnitCostListView(View):
    template_name = 'main/modal_archive_years.html'
    template_error = 'main/error.html'
    method = 'ArchiveYearUnitCostListView'

    def get(self, request, slugCounty):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            currentYear = currentDate.current_year()
            # unit = Unit.objects.filter(county_unit__slug=slugCounty)

            items = InvoiceItems.objects.filter(unit__county_unit__slug=slugCounty)
            yearsSet = set([year.invoice_id.date.year for year in items])
            years = sorted(yearsSet, reverse=True)
            context = {'slugCounty': slugCounty, 'years': years, 'archiveYearsUnitCost': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ArchiveYearUnitMainView(View):
    template_name = 'main/modal_archive_years.html'
    template_error = 'main/error.html'
    method = 'ArchiveYearUnitMainView'

    def get(self, request, slugUnit):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            currentYear = currentDate.current_year()
            unit = Unit.objects.get(slug=slugUnit)
            countySlug = unit.county_unit.slug
            items = InvoiceItems.objects.filter(unit__slug=slugUnit)

            yearsSet = set([year.invoice_id.date.year for year in items])
            years = sorted(yearsSet, reverse=True)
            context = {'countySlug': countySlug, 'unitSlug': slugUnit, 'years': years, 'year': currentYear,
                       'archiveYearsUnitMain': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ArchiveYearStatisticView(View):
    template_name = 'main/modal_archive_years.html'
    template_error = 'main/error.html'
    method = 'ArchiveYearStatisticView'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            items = InvoiceItems.objects.filter()
            yearsSet = set([year.invoice_id.date.year for year in items])
            years = sorted(yearsSet, reverse=True)
            context = {'years': years, 'archiveYearsStatistic': True}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class InvoicesListView(LoginRequiredMixin, View):
    template_name = 'main/site_invoice.html'
    template_error = 'main/error.html'
    paginate_by = 100
    method = 'InvoicesListView'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
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

                context = {'invoices': invoices, 'user_belongs_to_group': user_belongs_to_group,
                           'user_belongs_to_admin_group': user_belongs_to_admin_group, 'query': query, 'q': q}
                return render(request, self.template_name, context)
            else:
                context = {'invoices': invoices_pages, 'user_belongs_to_group': user_belongs_to_group,
                           'user_belongs_to_admin_group': user_belongs_to_admin_group, 'search': search}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class InvoiceInfoView(View):
    template_name = 'main/modal_info_invoice.html'
    template_error = 'main/error.html'
    method = 'InvoiceInfoView'

    def get(self, request, id):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            accessSection = '75405'
            yearObject = CurrentDate()
            year = yearObject.current_year()
            invoice = get_object_or_404(Invoice, pk=id)
            items = invoice.items.all()
            context = {'invoice': invoice, 'accessSection': accessSection,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'items': items, 'id': id,
                       'year': year}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CostsDetailsListView(View):
    template_name = 'main/cost_list_unit_details.html'
    template_error = 'main/error.html'
    paginate_by = 40
    method = 'CostsDetailsListView'

    def get(self, request, countyCardSlug, unitSlug, paragraphSlug, year):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
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
                       'user_belongs_to_admin_group': user_belongs_to_admin_group}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ParagraphModalView(View):
    template_name = 'main/modal_paragraph.html'
    template_error = 'main/error.html'
    method = 'ParagraphModalView'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            paragraphs = Paragraph.objects.all()
            context = {'paragraphs': paragraphs}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class ParagraphCostListView(LoginRequiredMixin, View):
    template_name_media = 'main/cost_list_media.html'
    template_name_general = 'main/cost_list_general.html'
    template_error = 'main/error.html'
    paginate_by = 80
    method = 'ParagraphCostListView'

    def get(self, request, paragraphSlug):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()

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

                    context = {'items': items, 'user_belongs_to_group': user_belongs_to_group,
                               'user_belongs_to_admin_group': user_belongs_to_admin_group, 'paragraph': paragraph,
                               'unitOfMeasure': unitOfMeasure, "query": query, 'q': q}
                    return render(request, self.template_name_media, context)
                else:
                    context = {'items': items_pages, 'user_belongs_to_group': user_belongs_to_group,
                               'user_belongs_to_admin_group': user_belongs_to_admin_group,
                               'paragraph': paragraph, 'unitOfMeasure': unitOfMeasure,
                               "search": search, 'q': q}
                    return render(request, self.template_name_media, context)

            except Exception as e:
                context = {'error': e, 'user_belongs_to_group': user_belongs_to_group,
                           'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
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

                    context = {'items': items, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'paragraph': paragraph,
                               "query": query, 'q': q}
                    return render(request, self.template_name_general, context)
                else:
                    context = {'items': items_pages, 'user_belongs_to_admin_group': user_belongs_to_admin_group,
                               'paragraph': paragraph,
                               "search": search, 'q': q}
                    return render(request, self.template_name_general, context)

            except Exception as e:
                context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
                logger.error("Error: %s", e)
                return render(request, self.template_error, context)


class UnitDetailsView(View):
    template_name = 'main/unit_details_info.html'
    template_error = 'main/error.html'
    method = "UnitDetailsView"

    def get(self, request, unitSlug):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            title = 'Grupa 6 - Administracja i utrzymanie obiektów'
            current_year = currentDate.current_year()
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

            context = {'unit': unit, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'paragraphs': paragraphs,
                       'title': title, 'tableObjects': tableObjects, 'year': current_year}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class MediaInfoUnitView(View):
    template_name = 'main/modal_info_unit.html'
    template_error = 'main/error.html'
    method = "MediaInfoUnitView"

    def get(self, request, id):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            title = 'Zużycie mediów'
            unit = get_object_or_404(Unit, pk=id)
            paragraphsModel = Paragraph.objects.all().filter(paragraph__contains='4260')
            items = unit.items.all().exclude(contract_types__type__icontains='Sprzedaż').filter(
                paragraph__paragraph__contains='4260')
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

            context = {'title': title, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'unit': unit,
                       'paragraphs': paragraphsModel, 'tableObjects': tableObjects}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class MediaInfoCountyView(View):
    template_name = 'main/modal_info_county_media.html'
    template_error = 'main/error.html'
    method = "MediaInfoCountyView"

    def get(self, request, countyCardSlug, year):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            title = 'Zużycie mediów'
            county = get_object_or_404(CountyCard, slug=countyCardSlug)
            paragraphsModel = Paragraph.objects.all().filter(paragraph__contains='4260')
            tableObjects = []
            try:
                units = Unit.objects.filter(county_unit__slug=countyCardSlug)
                for unit in units:
                    unit_id = unit.id
                    unit_name = f"{unit.type.type_full} {unit.city}"
                    status = unit.status
                    address = unit.address
                    objectName = unit.object_name
                    items = unit.items.all().exclude(contract_types__type__icontains='Sprzedaż').filter(
                        invoice_id__date_of_payment__year=year).filter(paragraph__paragraph__contains='4260')
                    for item in items:
                        exist_unit = False
                        for object in tableObjects:
                            if object['id'] == unit_id:
                                for data_entry in object['data']:
                                    if data_entry['paragraph'] == item.paragraph.paragraph:
                                        data_entry['consumption'] += item.consumption
                                        exist_unit = True
                                        break
                                if not exist_unit:
                                    object['data'].append(
                                        {'paragraph': item.paragraph.paragraph, 'consumption': item.consumption})
                                    exist_unit = True

                        if not exist_unit:
                            new_data_entry = {'paragraph': item.paragraph.paragraph, 'consumption': item.consumption}
                            year_entry = {'id': unit_id, 'unit': unit_name, 'objectName': objectName,
                                          'address': address, 'status': status, 'data': [new_data_entry]}
                            tableObjects.append(year_entry)
                # ----------------------------------------------------------------------------------------------------------

                # Dodanie zerowych sum dla paragrafów, które nie miały wydatków w danym roku
                all_paragraphs = set(paragraph['paragraph'] for paragraph in paragraphsModel.values('paragraph'))
                for year_entry in tableObjects:
                    existing_paragraphs = set(data_entry['paragraph'] for data_entry in year_entry['data'])
                    missing_paragraphs = all_paragraphs - existing_paragraphs
                    for missing_paragraph in missing_paragraphs:
                        year_entry['data'].append({'paragraph': missing_paragraph, 'consumption': 0})

                context = {'title': title, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'county': county,
                           'units': unit,
                           'paragraphs': paragraphsModel, 'tableObjects': tableObjects, 'year': year}
            except Exception:
                context = {'title': title, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'county': county,
                           'year': year}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class MediaInfoAllCountyView(View):
    template_name = 'main/modal_info_all_county_media.html'
    template_error = 'main/error.html'
    method = "MediaInfoCountyView"

    def get(self, request, year):
        try:
            user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
            title = 'Zużycie mediów'

            counties = CountyCard.objects.prefetch_related('unit__items__paragraph').all()
            paragraphs_model = Paragraph.objects.filter(paragraph__contains='4260')

            table_objects = []

            for county in counties:
                county_id = county.id
                units = county.unit.all()

                for unit in units:
                    items = unit.items.exclude(contract_types__type__icontains='Sprzedaż') \
                        .filter(invoice_id__date_of_payment__year=year) \
                        .filter(paragraph__paragraph__contains='4260')

                    for item in items:
                        exist_unit = False

                        for table_object in table_objects:
                            if table_object['id'] == county_id:
                                for data_entry in table_object['data']:
                                    if data_entry['paragraph'] == item.paragraph.paragraph:
                                        data_entry['consumption'] += item.consumption
                                        exist_unit = True
                                        break

                                if not exist_unit:
                                    table_object['data'].append({'paragraph': item.paragraph.paragraph,
                                                                 'consumption': item.consumption})
                                    exist_unit = True

                        if not exist_unit:
                            new_data_entry = {'paragraph': item.paragraph.paragraph,
                                              'consumption': item.consumption}
                            year_entry = {'id': county_id, 'county': county.name, 'data': [new_data_entry]}
                            table_objects.append(year_entry)

            all_paragraphs = set(paragraph['paragraph'] for paragraph in paragraphs_model.values('paragraph'))

            for year_entry in table_objects:
                existing_paragraphs = set(data_entry['paragraph'] for data_entry in year_entry['data'])
                missing_paragraphs = all_paragraphs - existing_paragraphs

                for missing_paragraph in missing_paragraphs:
                    year_entry['data'].append({'paragraph': missing_paragraph, 'consumption': 0})
            context = {'title': title, 'user_belongs_to_admin_group': user_belongs_to_admin_group,
                       'paragraphs': paragraphs_model, 'tableObjects': table_objects, 'year': year}

            return render(request, self.template_name, context)

        except ObjectDoesNotExist as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Object does not exist: %s", e)
            return render(request, self.template_error, context)

        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CountyCostUnitListView(View):
    template_name = 'main/cost_list_county_unit.html'
    template_error = 'main/error.html'
    method = 'CountyCostUnitListView'

    def get(self, request, countyCardSlug, year):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()
        try:
            county = CountyCard.objects.get(slug=countyCardSlug)
            units = Unit.objects.filter(county_unit=county)
            paragraphs = Paragraph.objects.all()
            objectDatas = []

            for unit in units:
                policeUnit = f'{unit.type.type_full} {unit.city}'
                status = unit.status
                items = unit.items.all()
                costObjectDict = {}
                address = unit.address
                objectName = unit.object_name

                # Inicjujemy kwoty dla wszystkich paragrafów jako 0
                for paragraph in paragraphs:
                    costObjectDict[paragraph.paragraph] = 0

                for item in items:
                    if item.invoice_id.date_of_payment.year == year:
                        paragraph = item.paragraph.paragraph
                        sumUnit = item.sum
                        costObjectDict[paragraph] += sumUnit

                costObjectList = [{'paragraph': paragraph, 'sum': sumUnit} for paragraph, sumUnit in
                                  costObjectDict.items()]

                objectDatas.append({'unit': policeUnit, 'address': address, 'objectName': objectName, 'status': status,
                                    'objects': costObjectList})

            # Tworzymy słownik do przechowywania sum paragrafów
            paragraphSums = {}

            # Iterujemy przez objectDatas i zliczamy sumy do stopki
            for unit_data in objectDatas:
                for object in unit_data['objects']:
                    paragraph = object['paragraph']
                    sum_value = object['sum']
                    # Dodajemy sumę do istniejącej sumy paragrafu lub inicjujemy nową
                    if paragraph in paragraphSums:
                        paragraphSums[paragraph] += sum_value
                    else:
                        paragraphSums[paragraph] = sum_value

            context = {'county': county, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'year': year,
                       'paragraphs': paragraphs, 'slugCounty': countyCardSlug,
                       "items": objectDatas, 'paragraphSums': paragraphSums}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e, 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class TrezorViews(LoginRequiredMixin, View):
    template_name = "main/site_trezor.html"
    template_error = 'main/error.html'
    method = 'TrezorViews'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        user_belongs_to_group = request.user.groups.filter(name='Viewers').exists()

        try:
            invoices = Invoice.objects.all().order_by("date_of_payment")

            query = "Wyczyść"
            search = "Szukaj"
            year_instance = CurrentDate()
            year = year_instance.current_year()

            date_from = request.GET.get("from")
            date_to = request.GET.get("to")

            date_from_obj = None
            date_to_obj = None

            if date_from:
                try:
                    date_from_obj = datetime.datetime.strptime(date_from, "%Y-%m-%d")
                except ValueError:
                    date_from_obj = None

            if date_to:
                try:
                    date_to_obj = datetime.datetime.strptime(date_to, "%Y-%m-%d")
                except ValueError:
                    date_to_obj = None

            if date_from_obj and date_to_obj:
                invoice_list = invoices.filter(date_of_payment__range=[date_from_obj, date_to_obj])

                day_sum = {}
                verification_all = 0

                days = set([day["date_of_payment"] for day in invoice_list.values("date_of_payment", "sum")])

                for day in days:
                    sum = 0
                    for invoice in invoice_list:
                        if day == invoice.date_of_payment:
                            sum += invoice.sum if invoice.sum is not None else 0  # Sprawdź, czy invoice.sum nie jest None
                    day_sum[day] = sum
                    verification_all += sum  # Aktualizuj sumę ogólną

                invoices_sum = len(invoice_list)

                verification_all_dict = invoice_list.aggregate(Sum("sum"))
                verification_all = round(verification_all_dict["sum__sum"] or 0, 2)

                context = {
                    'invoices': invoice_list,
                    'invoices_sum': invoices_sum,
                    'query': query,
                    'year': year,
                    'date_from': date_from,
                    'date_to': date_to,
                    'day_sum': day_sum,
                    'date_from_obj': date_from_obj,
                    'date_to_obj': date_to_obj,
                    'verification_all': verification_all,
                    'user_belongs_to_admin_group': user_belongs_to_admin_group
                }
                return render(request, self.template_name, context)
            else:
                invoices_sum = 0
                context = {'user_belongs_to_group': user_belongs_to_group,
                           'user_belongs_to_admin_group': user_belongs_to_admin_group, 'invoices_sum': invoices_sum,
                           'search': search, 'year': year}
                return render(request, self.template_name, context)
        except Exception as e:
            # Zapisanie informacji o błędzie do loga
            context = {'error': str(e), 'user_belongs_to_group': user_belongs_to_group,
                       'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CreateCSVForCountySum(View):
    template_error = 'main/error.html'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            paragraphs = Paragraph.objects.all()
            counties = County.objects.all()
            dateObject = CurrentDate()
            nowDate = dateObject.current_date()
            year = dateObject.current_year()

            objectDatas = []

            for county in counties:
                sectionObject = county.section.first()
                section = sectionObject.section
                units = county.unit.all()
                costObjectDict = {}

                for paragraph in paragraphs:
                    costObjectDict[paragraph.paragraph] = 0

                for unit in units:
                    # Filtruj elementy na podstawie roku płatności
                    items = unit.items.filter(invoice_id__date_of_payment__year=year)

                    for item in items:
                        costObjectDict[item.paragraph.paragraph] += item.sum

                costObjectList = [{'paragraph': paragraph, 'sum': sumUnit} for paragraph, sumUnit in
                                  costObjectDict.items()]
                objectDatas.append({'county': county.name, 'section': section, 'data': costObjectList})
            # -----------------------------------
            paragraphSums = {}

            for data in objectDatas:
                for object in data['data']:
                    paragraph = object['paragraph']
                    sum_value = object['sum']
                    # Dodajemy sumę do istniejącej sumy paragrafu lub inicjujemy nową
                    if paragraph in paragraphSums:
                        paragraphSums[paragraph] += sum_value
                    else:
                        paragraphSums[paragraph] = sum_value
            # ---------------------------------------------

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="Zestawienie kosztów gr.6 za {year}.csv"'
            # Ustawienie kodowania utf-8
            response.write(u'\ufeff'.encode('utf8'))

            # Tworzenie obiektu writer i zapis do pliku csv
            writer = csv.writer(response, delimiter=';', dialect='excel', lineterminator='\n')
            # Dodaj linię z tekstem "Załącznik do faktury {invoices}"
            response.write(f'Zestawienie kosztów gr.6 za {year}. Stan na {nowDate.strftime("%d.%m.%Y")}\n')
            writer.writerow(['Jednostka', 'Rozdział'] + [paragraph.paragraph for paragraph in paragraphs])

            for row in objectDatas:
                paragtaphSum = [str(item['sum']).replace('.', ',') for item in row['data']]
                writer.writerow([row['county'], row['section']] + paragtaphSum)

            writer.writerow(
                ['', 'Razem'] + [str(paragraphSums.get(paragraph, 0)).replace('.', ',') for paragraph in paragraphSums])

            return response
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group}
            logger.error("Error: %s", e)
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)


class CreateCSVForCountyYearSum(View):
    template_error = 'main/error.html'

    def get(self, request, year):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            paragraphs = Paragraph.objects.all()
            counties = County.objects.all()
            dateObject = CurrentDate()
            nowDate = dateObject.current_date()

            objectDatas = []

            for county in counties:
                sectionObject = county.section.first()
                section = sectionObject.section
                units = county.unit.all()
                costObjectDict = {}

                for paragraph in paragraphs:
                    costObjectDict[paragraph.paragraph] = 0

                for unit in units:
                    # Filtruj elementy na podstawie roku płatności
                    items = unit.items.filter(invoice_id__date_of_payment__year=year)

                    for item in items:
                        costObjectDict[item.paragraph.paragraph] += item.sum

                costObjectList = [{'paragraph': paragraph, 'sum': sumUnit} for paragraph, sumUnit in
                                  costObjectDict.items()]
                objectDatas.append({'county': county.name, 'section': section, 'data': costObjectList})
                # -----------------------------------
            paragraphSums = {}

            for data in objectDatas:
                for item in data['data']:
                    paragraph = item['paragraph']
                    sum_value = item['sum']
                    # Dodajemy sumę do istniejącej sumy paragrafu lub inicjujemy nową
                    if paragraph in paragraphSums:
                        paragraphSums[paragraph] += sum_value
                    else:
                        paragraphSums[paragraph] = sum_value
            # ---------------------------------------------

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="Zestawienie kosztów gr.6 za {year}.csv"'
            # Ustawienie kodowania utf-8
            response.write(u'\ufeff'.encode('utf8'))

            # Tworzenie obiektu writer i zapis do pliku csv
            writer = csv.writer(response, delimiter=';', dialect='excel', lineterminator='\n')
            # Dodaj linię z tekstem "Załącznik do faktury {invoices}"
            response.write(f'Zestawienie kosztów gr.6 za {year}. Stan na {nowDate.strftime("%d.%m.%Y")}\n')
            writer.writerow(['Jednostka', 'Rozdział'] + [paragraph.paragraph for paragraph in paragraphs])

            for row in objectDatas:
                paragtaphSum = [str(item['sum']).replace('.', ',') for item in row['data']]
                writer.writerow([row['county'], row['section']] + paragtaphSum)

            writer.writerow(
                ['', 'Razem'] + [str(paragraphSums.get(paragraph, 0)).replace('.', ',') for paragraph in
                                 paragraphSums])

            return response
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group}
            logger.error("Error: %s", e)
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)


class CreateCSVForCountyUnit(View):
    template_error = 'main/error.html'
    method = 'CreateCSVForCountyUnit'

    def get(self, request, countyCardSlug, year):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            nowDate = currentDate.current_date()
            county = CountyCard.objects.get(slug=countyCardSlug)
            units = Unit.objects.filter(county_unit=county)
            paragraphs = Paragraph.objects.all()
            objectDatas = []

            for unit in units:
                policeUnit = f'{unit.type.type_full} {unit.city}'
                status = unit.status
                items = unit.items.all()
                costObjectDict = {}
                address = unit.address
                objectName = unit.object_name

                # Inicjujemy kwoty dla wszystkich paragrafów jako 0
                for paragraph in paragraphs:
                    costObjectDict[paragraph.paragraph] = 0

                for item in items:
                    if item.invoice_id.date_of_payment.year == year:
                        paragraph = item.paragraph.paragraph
                        sumUnit = item.sum
                        costObjectDict[paragraph] += sumUnit

                costObjectList = [{'paragraph': paragraph, 'sum': sumUnit} for paragraph, sumUnit in
                                  costObjectDict.items()]

                objectDatas.append({'unit': policeUnit, 'address': address, 'objectName': objectName, 'status': status,
                                    'objects': costObjectList})
            # Tworzymy słownik do przechowywania sum paragrafów
            paragraphSums = {}
            # Iterujemy przez objectDatas i zliczamy sumy do stopki
            for unit_data in objectDatas:
                for object in unit_data['objects']:
                    paragraph = object['paragraph']
                    sum_value = object['sum']
                    # Dodajemy sumę do istniejącej sumy paragrafu lub inicjujemy nową
                    if paragraph in paragraphSums:
                        paragraphSums[paragraph] += sum_value
                    else:
                        paragraphSums[paragraph] = sum_value
            # ---------------------------------------------
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{countyCardSlug} za {year}-koszty.csv"'
            # Ustawienie kodowania utf-8
            response.write(u'\ufeff'.encode('utf8'))
            # Tworzenie obiektu writer i zapis do pliku csv
            writer = csv.writer(response, delimiter=';', dialect='excel', lineterminator='\n')
            # Dodaj linię z tekstem

            response.write(f'Zestawienie kosztów dla {county}. Stan na {nowDate.strftime("%d.%m.%Y")}\n')

            writer.writerow(['Jednostka', 'Adres'] + [paragraph.paragraph for paragraph in paragraphs])
            for row in objectDatas:
                paragtaphSum = [str(item['sum']).replace('.', ',') for item in row['objects']]

                writer.writerow([row['unit'], row['address']] + paragtaphSum)

            writer.writerow(
                ['', 'Razem'] + [str(paragraphSums.get(paragraph, 0)).replace('.', ',') for paragraph in
                                 paragraphSums])

            return response
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)


class CreateCSVForUnit(View):
    template_error = 'main/error.html'
    method = 'CreateCSVForUnit'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            nowDate = currentDate.current_date()
            units = Unit.objects.all()
            response = HttpResponse(content_type='text/csv')
            response[
                'Content-Disposition'] = f'attachment; filename="Zest.Jedn.gr.6 - {nowDate.strftime("%d.%m.%Y")}.csv"'
            # Ustawienie kodowania utf-8
            response.write(u'\ufeff'.encode('utf8'))
            # Tworzenie obiektu writer i zapis do pliku csv
            writer = csv.writer(response, delimiter=';', dialect='excel', lineterminator='\n')
            # response.write(f'Zestawienie jednostek. Stan na {nowDate.strftime("%d.%m.%Y")}\n')
            writer.writerow(["Zestawienie jednostek", f'Stan na {nowDate.strftime("%d.%m.%Y")}r.'])
            writer.writerow(
                ['Powiat', 'Rozdział', 'Rodzaj jednostki', 'Adres', 'Kod pocztowy', 'Miasto', 'Nazwa obiektu',
                 'Administrator', 'Status obiektu', 'Informacje'])

            for unit in units:
                writer.writerow(
                    [unit.county_swop.name, unit.county_swop.section.first(), unit.type.type_full, unit.address,
                     unit.zip_code, unit.city, unit.object_name, unit.manager, unit.status, unit.information])

            return response
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)


class CreateCSVForTrezor(View):
    template_error = 'main/error.html'
    method = 'CreateCSVForTrezor'

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            nowDate = currentDate.current_date()
            invoices = Invoice.objects.all().order_by("date_of_payment")
            # ---Pobieranie dat jako stringi
            date_from = request.GET.get("from")
            date_to = request.GET.get("to")
            invoiceList = []
            # ---Zamiana stringów dat na datatime
            if date_from:
                try:
                    date_from_obj = datetime.datetime.strptime(date_from, "%Y-%m-%d")
                except ValueError:
                    date_from_obj = None

            if date_to:
                try:
                    date_to_obj = datetime.datetime.strptime(date_to, "%Y-%m-%d")
                except ValueError:
                    date_to_obj = None

            # sprawdzanie czy istnieją daty i tworzenie obiektu z zakresem danych
            if date_from_obj and date_to_obj:
                days = [date_from_obj + datetime.timedelta(days=x) for x in
                        range((date_to_obj - date_from_obj).days + 1)]
                for day in days:
                    invoiceSums = 0
                    invoice_list = invoices.filter(date_of_payment=day)
                    objects = []
                    for invoice in invoice_list:
                        if invoice.sum == None:
                            invoice.sum = 0
                        invoiceSums += invoice.sum
                        objects.append({'invoice_no': invoice.no_invoice, 'date': invoice.date.strftime("%d.%m.%Y"),
                                        'sum': invoice.sum})
                    invoiceList.append(
                        {'day': day.strftime("%d.%m.%Y"), 'invoiceSums': invoiceSums, 'objects': objects})

            sumAll = 0
            for lista in invoiceList:
                sumAll += lista['invoiceSums']
            sumAll = str(sumAll).replace('.', ',')
            strDateFrom = date_from_obj.strftime("%d.%m.%Y")
            strDateTo = date_to_obj.strftime("%d.%m.%Y")
            # ---------------------------------------------
            response = HttpResponse(content_type='text/csv')
            response[
                'Content-Disposition'] = f'attachment; filename="Weryfikacja trezora- {nowDate.strftime("%d.%m.%Y")}.csv"'
            # Ustawienie kodowania utf-8
            response.write(u'\ufeff'.encode('utf8'))
            # # Tworzenie obiektu writer i zapis do pliku csv
            writer = csv.writer(response, delimiter=';', dialect='excel', lineterminator='\n')
            response.write(f'Weryfikacja trezora z dnia {nowDate}\n')
            response.write(f'Zapotrzebowanie środków w okresie od {strDateFrom} do {strDateTo} w kwocie {sumAll} zł\n')
            for item in invoiceList:
                invoiceSum = str(item["invoiceSums"]).replace('.', ',')
                writer.writerow([f'Data:', f'{item["day"]}', f'Suma:', f'{invoiceSum} zł'])
                for invoice in item['objects']:
                    sumValue = str(invoice['sum']).replace('.', ',')
                    writer.writerow(
                        ['', f'{invoice["invoice_no"]} z dnia {invoice["date"]}', f'Kwota:', f'{sumValue} zł'])

            return response
        except Exception as e:
            # Obsłuż wyjątek, jeśli coś pójdzie nie tak
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            # Zwróć odpowiednią stronę błędu lub obsługę błędu
            return render(request, self.template_error, context)


class CreateGraphView(View):
    template_error = 'main/error.html'
    method = 'CreateGraphView'

    def get(self, request, year, par):
        try:
            user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
            paragraphs = Paragraph.objects.all()
            parObj = Paragraph.objects.get(paragraph=par)
            parTitle = parObj.name
            counties = County.objects.prefetch_related('section', 'unit__items__invoice_id').all()

            objectDatas = []
            paragraphSums = {}

            for county in counties:
                section = county.section.first().section
                costObjectDict = {paragraph.paragraph: 0 for paragraph in paragraphs}

                for unit in county.unit.all():
                    items = unit.items.filter(invoice_id__date_of_payment__year=year)
                    for item in items:
                        costObjectDict[item.paragraph.paragraph] += item.sum

                costObjectList = [{'paragraph': paragraph, 'sum': sumUnit} for paragraph, sumUnit in
                                  costObjectDict.items()]
                objectDatas.append({'county': county.name, 'section': section, 'data': costObjectList})

                for data in objectDatas:
                    for item in data['data']:
                        paragraph = item['paragraph']
                        sum_value = item['sum']
                        paragraphSums[paragraph] = paragraphSums.get(paragraph, 0) + sum_value

            graph_data = [{'county': item['county'], 'sum': data['sum']} for item in objectDatas for data in
                          item['data'] if par == data['paragraph']]
            counties = [county['county'] for county in graph_data]
            sums = [sum_graph['sum'] for sum_graph in graph_data]

            fig, ax = plt.subplots(figsize=(15, 9))
            ax.bar(counties, sums)
            plt.xlabel('Jednostki')
            plt.xticks(rotation=90, fontsize='small')
            plt.subplots_adjust(bottom=0.2)
            plt.ylabel('Suma w zł')
            plt.title(f'Wydział Inwestycji i Remontów KWP w Poznaniu\nWydatki: § {par} w {year} roku.\n{parTitle}')
            try:
                # Dodanie daty na górnym rogu wykresu
                date_text = currentDate.current_date()  # Przykładowa data
                plt.text(1.00, 1.10, date_text.strftime('%d.%m.%Y'), ha='right', va='top', transform=ax.transAxes)

                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                plt.close()

                response = FileResponse(buffer, as_attachment=True, filename=f'Wykres §{par}-{year}.png')
                return response
            except RuntimeError as tk_error:
                # Tutaj obsłużamy błąd związanym z Tkinter
                # Możesz dodać kod obsługi tego błędu lub zwrócić komunikat o błędzie
                context = {'error': str(tk_error), 'user_belongs_to_admin_group': user_belongs_to_admin_group,
                           'method': self.method}
                logger.error("Error: %s", tk_error)
                return render(request, self.template_error, context)

        except Exception as e:
            context = {'error': e, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'method': self.method}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)

# class CreateBackupDB(View):
#     template_error = 'main/error.html'
#     method = 'CreateBackupDB'
#
#     def get(self, request):
#         try:
#             # Ścieżka do katalogu kopii zapasowej bazy danych
#             BACKUP_FOLDER = os.path.join(settings.BASE_DIR, 'dbBackup')
#
#             # Ścieżka do oryginalnej bazy danych
#             DB_MAIN = os.path.join(settings.BASE_DIR, 'db.sqlite3')
#
#             # Tworzenie katalogu na kopie zapasowe, jeśli nie istnieje
#             if not os.path.exists(BACKUP_FOLDER):
#                 os.makedirs(BACKUP_FOLDER)
#
#             # Generowanie nazwy pliku na podstawie aktualnego czasu
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             backup_filename = f"db_backup_{timestamp}.sqlite3"  # Nowa nazwa pliku kopii zapasowej
#
#             # Ścieżka do nowej kopii zapasowej bazy danych
#             NEW_BACKUP_PATH = os.path.join(BACKUP_FOLDER, backup_filename)
#
#             # Wykonanie kopii zapasowej bazy danych z nową nazwą pliku
#             shutil.copy2(DB_MAIN, NEW_BACKUP_PATH)
#             return HttpResponse(status=200)
#         except Exception as e:
#             context = {'error': e, 'method': self.method}
#             logger.error("Error: %s", e)
#             return render(request, self.template_error, context, status=500)
