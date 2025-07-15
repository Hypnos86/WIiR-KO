from enum import Enum


class GroupsApp(Enum):
    ADMINZRIWT = 'AdminZRiWT'
    VIEWERS = 'Viewers'


class ParagraphEnum(Enum):
    MEDIA1 = ['4260-01', 'kWh']
    MEDIA2 = ['4260-02', 'GJ']
    MEDIA3 = ['4260-03', 'kWh']
    MEDIA4 = ['4260-04', 'm3']


class DataApp:
    @staticmethod
    def invoice_type_data() -> list[dict:str, str]:
        return [{"type": "Faktura"},
                {"type": "Korekta"},
                {"type": "Pismo"}]

    @staticmethod
    def contract_types_data():
        return [{"type": "Nie dotyczy"},
                {"type": "Kompleksowa"},
                {"type": "OSD"},
                {"type": "Sprzedaż"}]

    @staticmethod
    def section_data():
        return [{"section": "75401", "name": "CBŚP"},
                {"section": "75402", "name": "BSW"},
                {"section": "75404", "name": "KWP"},
                {"section": "75405", "name": "Powiaty"},
                {"section": "75407", "name": "CBZC"}]

    @staticmethod
    def group_data():
        return [{"group": "6", "name": "Grupa 6 - Administracja i utrzymanie obiektów"}]

    @staticmethod
    def paragraph_data():
        return [
            {"paragraph": "4170-01", "name": "Wynagrodzenia płacowe na podstawie umowy zlecenia lub umowy o dzieło"},
            {"paragraph": "4210-03", "name": "Opał (węgiel, koks, olej opałowy, drewno, paliwa zastępcze)"},
            {"paragraph": "4260-01", "name": "Energia elektryczna"},
            {"paragraph": "4260-02", "name": "Energia cieplna"},
            {"paragraph": "4260-03", "name": "Gaz"},
            {"paragraph": "4260-04", "name": "Woda"},
            {"paragraph": "4300-10", "name": "Usługi komunalne i mieszkaniowe"},
            {"paragraph": "4300-19", "name": "Pozostałe usługi"},
            {"paragraph": "4400-00",
             "name": "Opłaty za administrowanie i czynsze za budynki, lokale i pomieszczenia garażowe"},
            {"paragraph": "4480-00", "name": "Podatek od nieruchomości"},
            {"paragraph": "4510-02", "name": "Trwały zarząd"},
            {"paragraph": "4510-03", "name": "Wody opadowe"},
            {"paragraph": "4520-03", "name": "Opłaty za korzystanie ze środowiska"},
            {"paragraph": "4520-04", "name": "Inne (podatek od śmieci)"}, ]
