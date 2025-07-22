from django.urls import path
from main.views import WelcomeView, HelpModalView, UnitsListMainView, CostListMainView, LoginView, UnitsView, \
    InvoiceInfoView, StatisticsView, UsersSiteView, ArchiveYearCostListView, InvoicesListView, CostsDetailsListView, \
    ArchiveYearUnitCostListView, ParagraphModalView, ParagraphCostListView, UnitDetailsView, MediaInfoUnitView, \
    CountyCostUnitListView, TrezorViews, ArchiveYearStatisticView, StatisticsYearView, CreateCSVForCountySum, \
    CreateCSVForCountyYearSum, MediaInfoCountyView, MediaInfoAllCountyView, ArchiveYearUnitMainView, CreateCSVForUnit, \
    CreateCSVForTrezor, CreateCSVForCountyUnit, CreateGraphView, TypeUnitsListView, CreateCSVForCostListUnitDetails

app_name = 'main'
urlpatterns = [
    # Modale
    path('modal/help/', HelpModalView.as_view(), name='showHelpModal'),
    path('modal/info/<int:id>/', InvoiceInfoView.as_view(), name='infoInvoice'),
    path('modal/archive/<slug:unitSlug>/<slug:paragraphSlug>/', ArchiveYearCostListView.as_view(), name='archiveYears'),
    path('modal/archive/<slug:slugCounty>/', ArchiveYearUnitCostListView.as_view(),
         name='archiveYearsUnitCost'),
    path('modal/archiveUnitMain/<slug:slugUnit>', ArchiveYearUnitMainView.as_view(), name='archiveYearsUnitMain'),
    path('modal/archive/', ArchiveYearStatisticView.as_view(), name='archiveYearsStatistic'),
    path('modal/paragraph/', ParagraphModalView.as_view(), name='paragraphModal'),
    path('modal/mediaInfoUnit/id/<int:id>/', MediaInfoUnitView.as_view(), name='mediaInfoModal'),
    path('modal/mediaInfoCounty/<slug:countyCardSlug>/year/<int:year>/', MediaInfoCountyView.as_view(),
         name='mediaInfoCountyModal'),
    path('modal/mediaInfoAllCounty/year/<int:year>/', MediaInfoAllCountyView.as_view(),
         name='mediaInfoAllCountyModal'),
    # Lista obiektów
    path('card/<slug:countySlug>/', UnitsListMainView.as_view(), name='unitCountyMain'),
    # Koszty jednostek w powiecie
    path('card/<slug:countyCardSlug>/cost/<int:year>', CountyCostUnitListView.as_view(), name='countyCostUnit'),
    # Lista kosztów jednostki
    path('card/<slug:countyCardSlug>/<slug:unitSlug>/year/<int:year>/', CostListMainView.as_view(),
         name='unit_details'),
    # Szczegóły kosztów
    path('card/<slug:countyCardSlug>/<slug:unitSlug>/paragraph/<slug:paragraphSlug>/year/<int:year>/',
         CostsDetailsListView.as_view(),
         name='unitCostList'),
    # Szczegóły jednostki - informacje
    path('info/unit/<slug:unitSlug>/', UnitDetailsView.as_view(), name='unitDetailsInfo'),

    # Nagłówek menu
    # Statystyki
    path('statistics/<int:year>/', StatisticsYearView.as_view(), name='statisticYear'),
    path('statistics/', StatisticsView.as_view(), name='statisticsSite'),

    # Faktury
    path('invoices/', InvoicesListView.as_view(), name='invoiceSite'),
    #  Trezor
    path('trezor/', TrezorViews.as_view(), name='trezorSite'),
    # Lista kosztów danego paragrafu
    path('invoices/paragraph/<slug:paragraphSlug>/', ParagraphCostListView.as_view(), name='paragraphCostList'),

    # Jednostki
    path('units/', UnitsView.as_view(), name='unitsSite'),
    path('units/<slug:type_units>/', TypeUnitsListView.as_view(), name='typeUnitsList'),
    # Uzytkownicy
    path('users/', UsersSiteView.as_view(), name='usersSite'),
    # Tworzenie plików CSV
    path('csvForCountySum/', CreateCSVForCountySum.as_view(), name='csvForCountySumCurrentYear'),
    path('csvForCountyYearSum/<int:year>', CreateCSVForCountyYearSum.as_view(), name='csvForCountyYearSum'),
    path('csvForCountyYearSum/<slug:countyCardSlug>/<int:year>', CreateCSVForCountyUnit.as_view(),
         name='csvForCountyUnit'),
    path('csvForUnit', CreateCSVForUnit.as_view(), name='csvForUnit'),
    path('csvForTrezor', CreateCSVForTrezor.as_view(), name='csvForTrezor'),
    path('csvForCostListUnitDetails/<slug:unitSlug>/<slug:paragraphSlug>/<int:year>/', CreateCSVForCostListUnitDetails.as_view(), name='csvForCostListUnitDetails'),
    # Tworzenie grafów
    path('graph/<int:year>/<str:par>/', CreateGraphView.as_view(), name='createGraph'),
    # Tworzenie pliku zapasowego
    # path('backUP/', CreateBackupDB.as_view(), name='backupDB'),
    # Logowanie
    path('login/', LoginView.as_view(), name="loginApp"),
    # Lista kart obiektów - strona główna
    path('', WelcomeView.as_view(), name='welcome')

]
