import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import time

TEAM_NAME = '013_KGI'

################################################################################
# open directory & setting up
################################################################################

output_dir = os.path.expanduser("~/Desktop/competition_api")
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created main directory: {output_dir}")

# file_path = '~/Desktop/Daily_Ticks.csv'  # TODO: Requirement: some files is to be at desktop 
file_path = "Daily_Ticks.csv"
df = pd.read_csv(file_path)

initial_investment = 10000000 

################################################################################
# load previous day data
################################################################################

# load data from previous day
def load_previous(file_type, teamName):
    output_dir = os.path.expanduser("~/Desktop/competition_api")

    folder_path = os.path.join(output_dir, "Previous", file_type)
    file_path = os.path.join(folder_path, f"{teamName}_{file_type}.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        data = pd.read_csv(file_path)
        print(f"Loaded '{file_type}' data for team {teamName}.")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")

    return None

# return initial_balance and start_line_available
def get_initial_balance(prev_summary_df: pd.DataFrame):
    initial_balance = initial_investment
    start_line_available = initial_investment

    if 'End Line available' not in prev_summary_df.columns:
        print("'End Line available' column not found in the file.")
        return initial_balance, start_line_available  # ใช้ค่าตั้งต้นหากไม่มีคอลัมน์

    initial_balance_series = prev_summary_df['End Line available']  # ดึงค่าคอลัมน์ 'End Line available' ทั้งหมด
    if initial_balance_series.empty:  # ตรวจสอบว่าคอลัมน์ไม่ว่างเปล่า
        print("'End Line available' column is empty.")
        return initial_balance, start_line_available  # ใช้ค่าตั้งต้นหากคอลัมน์ว่าง

    balance_first_value = initial_balance_series.iloc[0]  # เข้าถึงค่าแรกของคอลัมน์
    try:  # ลบเครื่องหมายคั่นหลักพันและแปลงเป็น float
        initial_balance = float(str(balance_first_value).replace(',', '').strip())
        start_line_available = initial_balance
        print("End Line available column loaded successfully.")
        print(f"Initial balance (first value): {initial_balance}")
    except ValueError:
        print(f"Error converting '{balance_first_value}' to a float.")  # ใช้ค่าตั้งต้นในกรณีเกิดข้อผิดพลาด

    return initial_balance, start_line_available

# Load the summary file
prev_summary_df = load_previous("summary", TEAM_NAME)
if prev_summary_df:
    initial_balance, start_line_available = get_initial_balance(prev_summary_df)
else:
    initial_balance, start_line_available = initial_investment, initial_investment  # ใช้ค่าตั้งต้นหากไฟล์ไม่โหลด
    print(f"Initial balance = initial_investment: {initial_investment}")

################################################################################
# init dict
################################################################################

# return dicts of {portfolio, statement, summary}
def init_dictionaries():
    PORTFOLIO_FIELDS = [
        'Table Name', 'File Name', 'Stock name', 'Start Vol', 'Actual Vol',
        'Avg Cost', 'Market Price', 'Market Value', 'Amount Cost', 'Unrealized P/L',
        '% Unrealized P/L', 'Realized P/L'
    ]
    STATEMENT_FIELDS = [
        'Table Name', 'File Name', 'Stock Name', 'Date', 'Time',
        'Side', 'Volume', 'Price', 'Amount Cost', 'End Line Available'
    ]
    SUMMARY_FIELDS = [
        'Table Name', 'File Name', 'trading_day', 'NAV', 'Portfolio value',
        'End Line available', 'Number of wins', 'Number of matched trades', 'Number of transactions:', 'Net Amount',
        'Unrealized P/L', '% Unrealized P/L', 'Realized P/L', 'Maximum value', 'Minimum value',
        'Win rate', 'Calmar Ratio', 'Relative Drawdown', 'Maximum Drawdown', '%Return'
    ]        
    portfolio = {field_name: [] for field_name in PORTFOLIO_FIELDS}
    statement = {field_name: [] for field_name in STATEMENT_FIELDS}
    summary = {field_name: [] for field_name in SUMMARY_FIELDS}
    return portfolio, statement, summary

portfolio_data, statement_data, summary_data = init_dictionaries()

################################################################################
# แปลงข้อมูลเป็น DataFrame  # ตัวอย่างการสร้างไฟล์ และสร้างข้อมูล
################################################################################

# my portfolio results here
portfolio_data['Table Name'].append('Portfolio_file')
portfolio_data['File Name'].append(TEAM_NAME)
portfolio_data['Stock name'].append('AOT')
portfolio_data['Start Vol'].append(0)
portfolio_data['Actual Vol'].append(0)
portfolio_data['Avg Cost'].append(0)
portfolio_data['Market Price'].append(61.5)
portfolio_data['Market Value'].append(0)
portfolio_data['Amount Cost'].append(0)
portfolio_data['Unrealized P/L'].append(0)
portfolio_data['% Unrealized P/L'].append(0)
portfolio_data['Realized P/L'].append(0)

portfolio_df = pd.DataFrame(portfolio_data)

# my trading results here
statement_data['Table Name'].append('Statement_file')
statement_data['File Name'].append(TEAM_NAME)
statement_data['Stock Name'].append('AOT')
statement_data['Date'].append('2024-11-21')
statement_data['Time'].append('09:56:23 AM')
statement_data['Side'].append('Buy')
statement_data['Volume'].append('100')
statement_data['Price'].append('60.75')
statement_data['Amount Cost'].append('6075')
statement_data['End Line Available'].append(initial_balance)

statement_df = pd.DataFrame(statement_data)

# my stats here

last_end_line_available = 1
count_win = 1
count_sell = 1

summary_data = {
    'Table Name': ['Sum_file'],
    'File Name': [TEAM_NAME],
    'trading_day': [1],
    'NAV': [portfolio_df['Market Value'].sum() + last_end_line_available],
    'Portfolio value': [portfolio_df['Market Value'].sum()],
    
    'End Line available': [last_end_line_available],  # Use the correct End Line Available
    'Start Line available':[start_line_available],
    'Number of wins': [count_win], 
    'Number of matched trades': [count_sell], #นับ sell เพราะ เทรดbuy sellด้วย volume เท่ากัน
    'Number of transactions:': [len(statement_df)],
    
    'Net Amount': [statement_df['Amount Cost'].sum()],
    'Unrealized P/L': [portfolio_df['Unrealized P/L'].sum()],
    '% Unrealized P/L': [(portfolio_df['Unrealized P/L'].sum() / initial_investment * 100) if initial_investment else 0],
    'Realized P/L': [portfolio_df['Realized P/L'].sum()],
    'Maximum value': [statement_df['End Line Available'].max()],
    
    'Minimum value': [statement_df['End Line Available'].min()],
    'Win rate': [(count_win * 100)/ count_sell],
    'Calmar Ratio': [((portfolio_df['Market Value'].sum() + last_end_line_available - initial_investment) / initial_investment * 100) / \
                           ((portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000)],
    'Relative Drawdown': [(portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000 / statement_df['End Line Available'].max() * 100],
    'Maximum Drawdown': [(portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000],
    
    '%Return': [((portfolio_df['Market Value'].sum() + last_end_line_available - initial_investment) / initial_investment * 100)]
}

summary_df = pd.DataFrame(summary_data)

################################################################################
# save data
################################################################################

def save_output(data, file_type, teamName):
    folder_path = output_dir + f"/Result/{file_type}"
    file_path = folder_path + f"/{teamName}_{file_type}.csv"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"Directory created: '{folder_path}'")

    # Save CSV
    data.to_csv(file_path, index=False)
    print(f"{file_type} saved at {file_path}")

save_output(portfolio_df, "portfolio", TEAM_NAME)
save_output(statement_df, "statement", TEAM_NAME)
save_output(summary_df, "summary", TEAM_NAME)
