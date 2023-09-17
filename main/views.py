from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
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
    template_name = 'main/card.html'
    template_error = 'main/error.html'

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
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CostListMainView(View):
    template_name = 'main/cost_list_main.html'
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


class ArchiveView(LoginRequiredMixin, View):
    template_name = 'main/site_archive.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            now_year = currentDate.current_year()
            archiveYears = Invoice.objects.all().values('date__year').exclude(date__year=now_year)
            archiveYearsSet = set([year['date__year'] for year in archiveYears])
            archiveYearsList = sorted(archiveYearsSet, reverse=True)
            context = {'archiveYearsList': archiveYearsList}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class AnalysisView(LoginRequiredMixin, View):
    template_name = 'main/site_analysis.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            return render(request, self.template_name)
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


class ArchiveYearListView(View):
    template_name = 'main/modal_archive_years.html'
    template_error = 'main/error.html'

    def get(self, request, unitSlug, paragraphSlug):
        try:
            currentYear = currentDate.current_year()
            unit = Unit.objects.get(slug=unitSlug)
            items = InvoiceItems.objects.filter(paragraph__slug=paragraphSlug, unit__id=unit.id)
            yearsSet = set([year.invoice_id.date.year for year in items])
            years = sorted(yearsSet, reverse=True)
            print(years)
            context = {'unit_slug': unitSlug, 'paragraph_slug': paragraphSlug, 'years': years}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class InvoicesListView(LoginRequiredMixin, View):
    template_name = 'main/site_invoice.html'
    template_error = 'main/error.html'

    def get(self, request):
        try:
            invoices = Invoice.objects.all()
            context = {'invoices': invoices}
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
            items = InvoiceItems.objects.filter(invoice_id=invoice.id)
            context = {'invoice': invoice, 'items': items, 'id': id}
            return render(request, self.template_name, context)

        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)


class CostsDetailsListView(View):
    template_name = 'main/cost_list_details.html'
    template_error = 'main/error.html'
    paginate_by = 40

    def get(self, request, countyCardSlug, unitSlug, paragraphSlug):
        try:
            currentYear = CurrentDate().current_year()
            unit = get_object_or_404(Unit, slug=unitSlug)
            items = InvoiceItems.objects.filter(unit__slug=unitSlug, paragraph__slug=paragraphSlug,
                                                invoice_id__date__year=currentYear)
            lastUpdate = items.last()
            paragraph = Paragraph.objects.get(slug=paragraphSlug)

            countyCardSlug = unit.county_unit.slug

            paginator = Paginator(items, self.paginate_by)
            page_number = request.GET.get('page')
            itemsList = paginator.get_page(page_number)

            context = {'unit': unit, 'items': itemsList, 'currentYear': currentYear, 'paragraph': paragraph,
                       'countyCardSlug': countyCardSlug, 'lastUpdate': lastUpdate}
            return render(request, self.template_name, context)
        except Exception as e:
            context = {'error': e}
            logger.error("Error: %s", e)
            return render(request, self.template_error, context)
