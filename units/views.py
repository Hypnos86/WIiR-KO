import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from units.forms import UnitForm
from units.models import Unit, County, TypeUnit

logger = logging.getLogger(__name__)


# Create your views here.
class AddUnitView(LoginRequiredMixin, View):
    template_name = 'units/unit_form.html'
    form_class = UnitForm

    def get(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            form = self.form_class()
            context = {'form': form, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)

    def post(self, request):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            form = self.form_class(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                form.save()
                return redirect('main:welcome')
            context = {'form': form, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'new': True}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error:s%", e)


class EditUnitView(LoginRequiredMixin, View):
    template_name = 'units/unit_form.html'
    form_class = UnitForm

    def get(self, request, slug):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            unit = get_object_or_404(Unit, slug=slug)
            slugCard = unit.county_unit.slug
            form = self.form_class(instance=unit)
            context = {'form': form, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'slugCard': slugCard, 'new': False}
            return render(request, self.template_name, context)

        except Exception as e:
            logger.error("Error: %s", e)

    def post(self, request, slug):
        user_belongs_to_admin_group = request.user.groups.filter(name='AdminZRiWT').exists()
        try:
            unit = get_object_or_404(Unit, slug=slug)
            slugCard = unit.county_unit.slug
            form = self.form_class(request.POST or None, instance=unit)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                form.save()
                return redirect(reverse('main:unitCountyMain', kwargs={'countySlug': unit.county_unit.slug}))
            context = {'form': form, 'user_belongs_to_admin_group': user_belongs_to_admin_group, 'slugCard': slugCard, 'new': False}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("Error: %s", e)
