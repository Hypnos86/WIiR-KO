from django.urls import path, include
from main.views import WelcomeView, HelpModalView, UnitCountyMainView, UnitDetailsView, LoginView, ArchiveView, \
    AnalysisView, UsersSiteView, ArchiveYearListView

app_name = 'main'
urlpatterns = [

    path('help/', HelpModalView.as_view(), name='showHelpModal'),
    path('card/<slug:slug>/', UnitCountyMainView.as_view(), name='unitCountyMain'),
    path('card/<slug:countyCardSlug>/unit/<slug:slug_unit>/', UnitDetailsView.as_view(), name='unit_details'),
    path('card/archive/', ArchiveYearListView.as_view(), name='archiveYears'),
    path('archive/', ArchiveView.as_view(), name='archiveSite'),
    path('analysis/', AnalysisView.as_view(), name='analysisSite'),
    path('users/', UsersSiteView.as_view(), name='usersSite'),
    path('login/', LoginView.as_view(), name="loginApp"),
    path('', WelcomeView.as_view(), name='welcome')

]
