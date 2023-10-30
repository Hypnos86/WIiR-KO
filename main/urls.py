from django.urls import path, include
from main.views import WelcomeView, HelpModalView, UnitsListaMainView, CostListMainView, LoginView, UnitsView, \
    InvoiceInfoView, StatisticsView, UsersSiteView, ArchiveYearCostListView, InvoicesListView, CostsDetailsListView, \
    ArchiveYearUnitCostListView, ParagraphModalView, ParagraphCostListView, UnitDetailsView, MediaInfoUnitView, \
    CountyCostUnitListView, TrezorViews

app_name = 'main'
urlpatterns = [
    # Modale
    path('modal/help/', HelpModalView.as_view(), name='showHelpModal'),
    path('modal/info/<int:id>/', InvoiceInfoView.as_view(), name='infoInvoice'),
    path('modal/archive/<slug:unitSlug>/<slug:paragraphSlug>/', ArchiveYearCostListView.as_view(), name='archiveYears'),
    path('modal/archive/<slug:slugCounty>/', ArchiveYearUnitCostListView.as_view(),
         name='archiveYearsUnitCost'),
    path('modal/paragraph/', ParagraphModalView.as_view(), name='paragraphModal'),
    path('modal/mediaInfoUnit/<int:id>/', MediaInfoUnitView.as_view(), name='mediaInfoModal'),

    # Lista obiektów
    path('card/<slug:slug>/', UnitsListaMainView.as_view(), name='unitCountyMain'),
    # Koszty jednostek w powiecie
    path('card/<slug:countyCardSlug>/cost/<int:year>', CountyCostUnitListView.as_view(), name='countyCostUnit'),
    # Lista kosztów jednostki
    path('card/<slug:countyCardSlug>/<slug:unitSlug>/', CostListMainView.as_view(), name='unit_details'),
    # Szczegóły kosztów
    path('card/<slug:countyCardSlug>/<slug:unitSlug>/<slug:paragraphSlug>/<int:year>/', CostsDetailsListView.as_view(),
         name='unitCostList'),
    # Szczegóły jednostki - informacje
    path('info/unit/<slug:unitSlug>/', UnitDetailsView.as_view(), name='unitDetailsInfo'),

    # Nagłówek menu
    # Statystyki
    path('statistics/', StatisticsView.as_view(), name='statisticsSite'),

    # Faktury
    path('invoices/', InvoicesListView.as_view(), name='invoiceSite'),
    #  Trezor
    path('trezor/', TrezorViews.as_view(), name='trezorSite'),
    # Lista kosztów danego paragrafu
    path('invoices/paragraph/<slug:paragraphSlug>/', ParagraphCostListView.as_view(), name='paragraphCostList'),

    # Jednostki
    path('units/', UnitsView.as_view(), name='unitsSite'),
    # Uzytkownicy
    path('users/', UsersSiteView.as_view(), name='usersSite'),
    # Logowanie
    path('login/', LoginView.as_view(), name="loginApp"),
    # Lista kart obiektów - strona główna
    path('', WelcomeView.as_view(), name='welcome')

]
