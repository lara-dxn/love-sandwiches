import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)

def get_sales_data():

    """
    Get sales figures input from user
    """

    print("Please enter sales data from the last market day")
    print('Daa should be in the format of six numbers, separated by commas')
    print('Example: 0, 10, 20, 30, 40, 50\n')

    data_str = input('Enter your data here: ')
    
    sales_data = data_str.split(',')
    validate_data(sales_data)


def validate_data(values):
    """
    Attempts to convert string vslues to int, raises ValueError if not possible or there are not exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f'6 Values required, user provided {len(values)}')
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")

get_sales_data()