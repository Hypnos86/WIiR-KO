import datetime
import logging
from django.shortcuts import render
from django.views import View
from cpvdict.models import Genre, OrderLimit, Typecpv

logger = logging.getLogger(__name__)


class CurrentDate():
    def current_year(self):
        return datetime.date.today().year

    def current_date(self):
        return datetime.date.today()


currentDate = CurrentDate()

TEMPLATE_ERROR = "main/error.html"


def handle_exception(request, e, method):
    context = {
        "error": e,
        "method": method,
    }
    logger.error("Error: %s", e)
    return render(request, TEMPLATE_ERROR, context)

class GenreMainView( View):
    template = "cpvdict/site_genre.html"
    method = "GenreMainView"

    def get(self, request):
        try:
            limits = OrderLimit.objects.order_by("-id").first
            year = CurrentDate().current_year()
            genres = Genre.objects.all().exclude(name_id="RB")

            context = {'year': year, 'genres':genres, "limits":limits, "site_genre":True}
            return render(request, self.template, context)
        except Exception as e:
            return handle_exception(request, e,self.method)

class CpvDictionaryView(View):
    template = "cpvdict/dictionary.html"
    method = "CpvDictionaryView"

    def get(self, request):
        try:
            cpvs = Typecpv.objects.all()
            query = "Wyczyść"
            search = "Szukaj"
            sumcpv = len(cpvs)
            q = request.GET.get("q")

            if q:
                cpvs = cpvs.filter(no_cpv__startswith=q) | cpvs.filter(name__icontains=q)
                qsum = len(cpvs)
                context = {'cpvs': cpvs, 'sumcpv': sumcpv, 'query': query, 'qsum': qsum, "q": q}
                return render(request, self.template, context)
            else:
                context = {'cpvs': cpvs, 'sumcpv': sumcpv, 'search': search}
                return render(request, self.template, context)
        except Exception as e:
            return handle_exception(request, e,self.method)


