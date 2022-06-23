import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

MI_SHEET_KEY = '1IdaTRlRgQXxCAEo42bvAcRexS63lGLMk76mrDJd5tfQ'
DATOS_SHEET = 'datos'
BUSQUEDAS_SHEET = 'busquedas'

CREDS_JSON = 'TelegramBot-00fa5b3420f1.json'

class gsheet_helper:
    def __init__(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            CREDS_JSON,
            scope
        )

        self.client = gspread.authorize(creds)
        self.gsheet = self.client.open_by_key(MI_SHEET_KEY)

    def get_sheet(self):
        sheet = self.gsheet.worksheet(DATOS_SHEET)
        items = pd.DataFrame(sheet.get_all_records())
        return items
    
    def store_user(self, users_dic):
        datos = pd.DataFrame(self.get_sheet())
        sheet = self.gsheet.worksheet(DATOS_SHEET)
        

        condi = datos[datos["id"] == users_dic["id"]].empty

        if condi:
            sheet.add_rows(1)
            
            sheet.append_row([element for element in users_dic.values()])
        else:
            print('Usuario ya existente!')

    def get_sheetB(self):
        sheetB = self.gsheet.worksheet(BUSQUEDAS_SHEET)
        itemsB = pd.DataFrame(sheetB.get_all_records())
        return itemsB

    def store_search(self, user_search):
        datos = pd.DataFrame(self.get_sheetB())
        sheetB = self.gsheet.worksheet(BUSQUEDAS_SHEET)

        sheetB.add_rows(1)
        sheetB.append_row([element for element in user_search.values()])


if __name__ == '__main__':
    print('Hola xdddd')