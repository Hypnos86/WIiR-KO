from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from main.models import CountyCard, HelpInfo
from units.models import Unit
import logging

logger = logging.getLogger(__name__)


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
        return render(request, self.template_name)

    def post(self, request):
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


class HelpModalView(View):
    template_name = 'main/modal-help.html'

    def get(self, request):
        text = HelpInfo.objects.last()
        context = {'text': text}
        return render(request, self.template_name, context)


class UnitCountyMainView(View):
    template_name = 'main/unit_county_main.html'

    def get(self, request, slug):
        units = Unit.objects.filter(county_unit__slug=slug)
        county = CountyCard.objects.get(slug=slug)

        context = {'units': units, 'slug': slug, 'county': county}
        return render(request, self.template_name, context)


class UnitDetailsView(View):
    template_name = 'main/unit_list.html'

    def get(self, request, slug, slug_unit):
        unit = Unit.objects.get(slug=slug_unit)
        context = {'unit': unit, 'slug': slug}
        return render(request, self.template_name, context)
