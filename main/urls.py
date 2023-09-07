from django.urls import path
from main.views import WelcomeView, HelpModalView, UnitCountyMainView, UnitDetailsView, LoginView

app_name = 'main'
urlpatterns = [

    path('help/', HelpModalView.as_view(), name='showHelpModal'),
    path('card/<slug:slug>/', UnitCountyMainView.as_view(), name='unit_county_main'),
    path('card/<slug:slug>/unit/<slug:slug_unit>/', UnitDetailsView.as_view(), name='unit_details'),
    path('login', LoginView.as_view(), name="loginApp"),
    path('', WelcomeView.as_view(), name='welcome')

]
