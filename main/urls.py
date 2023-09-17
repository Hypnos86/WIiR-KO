from django.urls import path, include
from main.views import WelcomeView, HelpModalView, UnitsListaMainView, CostListMainView, LoginView, ArchiveView, \
    InvoiceInfoView, AnalysisView, UsersSiteView, ArchiveYearListView, InvoicesListView, CostsDetailsListView

app_name = 'main'
urlpatterns = [
    # Modale
    path('modal/help/', HelpModalView.as_view(), name='showHelpModal'),
    path('modal/info/<int:id>/', InvoiceInfoView.as_view(), name='infoInvoice'),
    path('modal/archive/<slug:unitSlug>/<slug:paragraphSlug>/', ArchiveYearListView.as_view(), name='archiveYears'),

    # Lista obiektów
    path('card/<slug:slug>/', UnitsListaMainView.as_view(), name='unitCountyMain'),
    # Lista kosztów jednostki
    path('card/<slug:countyCardSlug>/<slug:unitSlug>/', CostListMainView.as_view(), name='unit_details'),
    # Szczegóły kosztów
    path('card/<slug:countyCardSlug>/<slug:unitSlug>/<slug:paragraphSlug>/', CostsDetailsListView.as_view(),
         name='unitCostList'),

    # Analiza
    path('analysis/', AnalysisView.as_view(), name='analysisSite'),
    # Faktury
    path('invoices/', InvoicesListView.as_view(), name='invoiceSite'),
    # Archiwum
    path('archives/', ArchiveView.as_view(), name='archiveSite'),
    # Uzytkownicy
    path('users/', UsersSiteView.as_view(), name='usersSite'),
    # Logowanie
    path('login/', LoginView.as_view(), name="loginApp"),
    # Lista kart obiektów - strona główna
    path('', WelcomeView.as_view(), name='welcome')

]
