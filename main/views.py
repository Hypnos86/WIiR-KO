from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from main.models import CountyCard, HelpInfo
from units.models import Unit
from invoices.models import Invoice, InvoiceItems, Paragraph
from django.db.models import Max
import logging
import datetime

logger = logging.getLogger(__name__)


class CurrentDate():
    def current_year(self):
        return datetime.date.today().year

    def current_date(self):
        return datetime.date.today()


currentDate = CurrentDate()


# Create your views here.
class WelcomeView(View):
    template_name = 'main/welcome.html'

    def get(self, request):
        try:
            counties = CountyCard.objects.all()
            if not request.user.is_authenticated:
                counties = counties.exclude(name="KWP Poznań")

            context = {'counties': counties}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)


class LoginView(View):
    template_name = 'main/registration/login.html'
    template_welcome = 'main/welcome.html'

    def get(self, request):
        try:
            return render(request, self.template_name)
        except Exception as e:
            logger.error("Error: %s", e)

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
            logger.error("Error: %s", e)


class HelpModalView(View):
    template_name = 'main/modal-help.html'

    def get(self, request):
        try:
            text = HelpInfo.objects.last()
            context = {'text': text}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)


class UnitCountyMainView(View):
    template_name = 'main/unit_county_main.html'

    def get(self, request, slug):
        try:
            units = Unit.objects.filter(county_unit__slug=slug)
            activeUnits = len(units.filter(status=True))
            archiveUnits = len(units.filter(status=False))
            county = CountyCard.objects.get(slug=slug)
            context = {'units': units, 'slug': slug, 'county': county, 'activeUnits': activeUnits,
                       'archiveUnits': archiveUnits}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)


class UnitDetailsView(View):
    template_name = 'main/unit_details.html'

    def get(self, request, slug, slug_unit):
        try:
            now_year = currentDate.current_year()
            unit = get_object_or_404(Unit, slug=slug_unit)
            invoiceItems = InvoiceItems.objects.filter(unit__id=unit.id, invoice_id__date__year=now_year)
            paragraphs = Paragraph.objects.all()

            paragraph_data = []

            # for paragraph in paragraphs:
            #     items = invoiceItems.filter(paragraph=paragraph)[:4]
            #     paragraph_data.append({'paragraph': paragraph, 'items': items})

            # Wybierz tylko niektóre propertisy z modelu Invoice
            last_update = []

            for paragraph in paragraphs:
                paragraph_items = invoiceItems.filter(paragraph=paragraph).order_by('-invoice_id__date')[:4]

                items = []
                for item in paragraph_items:
                    selected_properties = {
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
                        # Dodaj inne wybrane propertisy tutaj
                    }
                    items.append(selected_properties)
                paragraph_data.append({'paragraph': paragraph, 'items': items})

            context = {'unit': unit, 'paragraph_data': paragraph_data, 'now_year': now_year, 'slug': slug}
            return render(request, self.template_name, context)

        except Exception as e:
            logger.error("Error: %s", e)


class ArchiveView(LoginRequiredMixin, View):
    template_name = 'main/archive_site.html'

    def get(self, request):
        try:
            now_year = currentDate.current_year()
            archiveYears = Invoice.objects.all().values('date__year').exclude(date__year=now_year)
            archiveYearsSet = set([year['date__year'] for year in archiveYears])
            archiveYearsList = sorted(archiveYearsSet, reverse=True)
            context = {'archiveYearsList': archiveYearsList}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)


class AnalysisView(LoginRequiredMixin, View):
    template_name = 'main/analysis_site.html'

    def get(self, request):
        try:
            return render(request, self.template_name)
        except Exception as e:
            logger.error("Error: %s", e)


class UsersSiteView(LoginRequiredMixin, View):
    template = 'main/users_site.html'

    def get(self, request):
        users = User.objects.all()
        context = {'users': users}
        return render(request, self.template, context)
