from django.urls import path
from units.views import AddUnitView, EditUnitView

app_name = 'units'
urlpatterns = [
    path('newUnit/', AddUnitView.as_view(), name='newUnit'),
    path('editUnit/<slug:slug>', EditUnitView.as_view(), name='editUnit')
]
