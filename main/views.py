from django.shortcuts import render
from django.views import View
from main.models import CountyCard, HelpInfo


# Create your views here.
class WelcomeView(View):
    template_name = 'main/welcome.html'

    def get(self, request):
        counties = CountyCard.objects.all()
        context = {'counties': counties}
        return render(request, self.template_name, context)


class HelpModalView(View):
    template_name = 'main/modal-help.html'

    def get(self, request):
        text = HelpInfo.objects.last()
        context = {'text': text}
        return render(request, self.template_name, context)


class UnitCountyMainView(View):
    template_name = 'main/unit_county_main.html'

    def get(self, request, slug):
        counties = CountyCard.objects.filter(slug=slug)

        context = {'counties': counties}
        return render(request, self.template_name, context)
