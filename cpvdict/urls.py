from django.urls import path
from . import views
from cpvdict.views import GenreMainView,CpvDictionaryView

app_name = 'cpvdict'
urlpatterns = [
    path('cpv_dict/', CpvDictionaryView.as_view(), name='cpvDictionary'),
]
