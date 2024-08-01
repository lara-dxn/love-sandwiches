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

    while True:
        print("Please enter sales data from the last market day")
        print('Data should be in the format of six numbers, separated by commas')
        print('Example: 0, 10, 20, 30, 40, 50\n')

        data_str = input('Enter your data here: \n')
        
        sales_data = data_str.split(',')
        

        if validate_data(sales_data):
            print('Valid data provided')
            
            break

    return sales_data


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
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Updates specified worksheet with data provided
    """

    print(f'Updating {worksheet} worksheet \n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated \n')

def get_last_5_sales_days():
    """
    Gets the last 5 market day sales data for each sandwich and returns data as list of lists
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind) ## indices passed to gspread start at 1, not 0
        columns.append(column[-5:])

    return columns
    


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus
    - positive surplus indicates waste
    - negative surplus indicates extra made on demand when stock ran out
    """

    print('Calculating surplus data \n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    stock_row = [int(x) for x in stock_row]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)

    return surplus_data

def calculate_stock_data(data):
    """
    Calculate average sales to estimate needed stock for each item, adding 10%
    """

    print('Calculating stock data \n')   
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Run main program functions
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    last_5_sales = get_last_5_sales_days()
    stock_data = calculate_stock_data(last_5_sales)
    update_worksheet(stock_data, 'stock')

print('Welcome to Love Sandwiches Data Automation')
main()
