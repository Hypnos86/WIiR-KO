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
    def create_invoice_type(self):
        return [{"type": "Faktura"},
                {"type": "Korekta"},
                {"type": "Pismo"}]
