import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from units.forms import UnitForm
from units.models import Unit, County, TypeUnit

logger = logging.getLogger(__name__)

TEMPLATE_ERROR = "main/error.html"

def handle_exception(request, e, method):
    context = {
        "error": e,
        "method": method,
    }
    logger.error("Error: %s", e)
    return render(request, TEMPLATE_ERROR, context)

# Create your views here.
class AddUnitView(LoginRequiredMixin, View):
    template_name = 'units/unit_form.html'
    form_class = UnitForm
    method = 'AddUnitView'

    def get(self, request):
        try:
            form = self.form_class()
            context = {'form': form, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            return handle_exception(request, e, self.method)

    def post(self, request):
        try:
            form = self.form_class(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                form.save()
                return redirect('main:welcome')
            context = {'form': form, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            return handle_exception(request, e, self.method)


class EditUnitView(LoginRequiredMixin, View):
    template_name = 'units/unit_form.html'
    form_class = UnitForm
    method = 'EditUnitView'

    def get(self, request, slug):
        try:
            unit = get_object_or_404(Unit, slug=slug)
            slugCard = unit.county_unit.slug
            form = self.form_class(instance=unit)
            context = {'form': form, 'slugCard': slugCard, 'new': False}
            return render(request, self.template_name, context)

        except Exception as e:
            return handle_exception(request, e, self.method)

    def post(self, request, slug):
        try:
            unit = get_object_or_404(Unit, slug=slug)
            slugCard = unit.county_unit.slug
            form = self.form_class(request.POST or None, instance=unit)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                form.save()
                return redirect(reverse('main:unitCountyMain', kwargs={'countySlug': unit.county_unit.slug}))
            context = {'form': form, 'slugCard': slugCard, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            return handle_exception(request, e, self.method)
