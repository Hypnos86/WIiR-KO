from django.shortcuts import render
from django.views import View
from main.models import CountyCard


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
        return render(request, self.template_name)
