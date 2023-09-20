from django.urls import path, include
from main.views import WelcomeView, HelpModalView, UnitsListaMainView, CostListMainView, LoginView, ArchiveView, \
    InvoiceInfoView, StatisticsView, UsersSiteView, ArchiveYearCostListView, InvoicesListView, CostsDetailsListView, \
    ArchiveYearUnitCostListView, ParagraphModalView, ParagraphCostListView

app_name = 'main'
urlpatterns = [
    # Modale
    path('modal/help/', HelpModalView.as_view(), name='showHelpModal'),
    path('modal/info/<int:id>/', InvoiceInfoView.as_view(), name='infoInvoice'),
    path('modal/archive/<slug:unitSlug>/<slug:paragraphSlug>/', ArchiveYearCostListView.as_view(), name='archiveYears'),
    path('modal/archive/<slug:slugCounty>/', ArchiveYearUnitCostListView.as_view(),
         name='archiveYearsUnitCost'),
    path('modal/paragraph/', ParagraphModalView.as_view(), name='paragraphModal'),

    # Lista obiektów
    path('card/<slug:slug>/', UnitsListaMainView.as_view(), name='unitCountyMain'),
    # Lista kosztów jednostki
    path('card/<slug:countyCardSlug>/<slug:unitSlug>/', CostListMainView.as_view(), name='unit_details'),
    # Szczegóły kosztów
    path('card/<slug:countyCardSlug>/<slug:unitSlug>/<slug:paragraphSlug>/', CostsDetailsListView.as_view(),
         name='unitCostList'),
    # Nagłówek menu
    # Statystyki
    path('statistics/', StatisticsView.as_view(), name='statisticsSite'),

    # Faktury
    path('invoices/', InvoicesListView.as_view(), name='invoiceSite'),
    # Lista kosztów danego paragrafu
    path('invoices/paragraph/<slug:paragraphSlug>/', ParagraphCostListView.as_view(), name='paragraphCostList'),

    # Archiwum
    path('archives/', ArchiveView.as_view(), name='archiveSite'),
    # Uzytkownicy
    path('users/', UsersSiteView.as_view(), name='usersSite'),
    # Logowanie
    path('login/', LoginView.as_view(), name="loginApp"),
    # Lista kart obiektów - strona główna
    path('', WelcomeView.as_view(), name='welcome')

]
