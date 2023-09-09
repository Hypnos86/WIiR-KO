from django.urls import path
from units.views import AddUnitView, EditUnitView

app_name = 'units'
urlpatterns = [
    path('addUnit/', AddUnitView.as_view(), name='addUnit'),
    path('editUnit/<slug:slug>', EditUnitView.as_view(), name='editUnit')
]
