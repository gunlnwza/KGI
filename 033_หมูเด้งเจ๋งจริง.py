import os
from datetime import datetime, time

import pandas as pd
import numpy as np

################################################################################
# constants

TEAM_NAME = "003_หมูเด้งเจ๋งจริง"
INITIAL_INVESTMENT = 10000000
ROOT_DIR = os.path.join(os.path.expanduser("~"), "Desktop")
OUTPUT_DIR = os.path.join(ROOT_DIR, "competition_api")

################################################################################
# summarizing results

def init_portfolio_data() -> dict:  # TODO: wait for official field names
	PORTFOLIO_FIELDS = [
		'Table Name', 'File Name', 'Stock name', 'Start Vol', 'Actual Vol',
		'Avg Cost', 'Market Price', 'Market Value', 'Amount Cost', 'Unrealized P/L',
		'% Unrealized P/L', 'Realized P/L'
	]
	return {field_name: [] for field_name in PORTFOLIO_FIELDS}

def init_statement_data() -> dict:  # TODO: wait for official field names
	STATEMENT_FIELDS = [
		'Table Name', 'File Name', 'Stock Name', 'Date', 'Time',
		'Side', 'Volume', 'Price', 'Amount Cost', 'End Line Available'
	]
	return {field_name: [] for field_name in STATEMENT_FIELDS}

def init_summary_data() -> dict:  # TODO: wait for official field names
	SUMMARY_FIELDS = [
		'Table Name', 'File Name', 'trading_day', 'NAV', 'Portfolio value',
		'End Line available', 'Start Line available', 'Number of wins', 'Number of matched trades', 'Number of transactions:',
		'Net Amount', 'Unrealized P/L', '% Unrealized P/L', 'Realized P/L', 'Maximum value',
		'Minimum value', 'Win rate', 'Calmar Ratio', 'Relative Drawdown', 'Maximum Drawdown',
		'%Return'
	]
	return {field_name: [] for field_name in SUMMARY_FIELDS}

def calculate_portfolio_data():  # TODO: connect with trading logic
	portfolio_data = init_portfolio_data()

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

	return portfolio_data

def calculate_statement_data(initial_balance):  # TODO: connect with trading logic
	statement_data = init_statement_data()

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

	return statement_data

def calculate_summary_data(portfolio_df, statement_df, start_line_available):  # TODO: Check Calmar Ratio calculation; Check Maximum Drawdown calculation
	summary_data = init_summary_data()

	last_end_line_available = 1
	count_win = 1
	count_sell = 1

	summary_data['Table Name'].append("Sum_file")
	summary_data['File Name'].append(TEAM_NAME)
	summary_data['trading_day'].append(1)
	summary_data['NAV'].append(portfolio_df['Market Value'].sum() + last_end_line_available)
	summary_data['Portfolio value'].append(portfolio_df['Market Value'].sum())

	summary_data['End Line available'].append(last_end_line_available)
	summary_data['Start Line available'].append(start_line_available)
	summary_data['Number of wins'].append(count_win)
	summary_data['Number of matched trades'].append(count_sell)
	summary_data['Number of transactions:'].append(len(statement_df))

	summary_data['Net Amount'].append(statement_df['Amount Cost'].sum())
	summary_data['Unrealized P/L'].append(portfolio_df['Unrealized P/L'].sum())
	summary_data['% Unrealized P/L'].append((portfolio_df['Unrealized P/L'].sum() / INITIAL_INVESTMENT) * 100)
	summary_data['Realized P/L'].append(portfolio_df['Realized P/L'].sum())
	summary_data['Maximum value'].append(statement_df['End Line Available'].max())

	summary_data['Minimum value'].append(statement_df['End Line Available'].min())
	summary_data['Win rate'].append((count_win / count_sell) * 100)
	return_ = (portfolio_df['Market Value'].sum() + last_end_line_available - INITIAL_INVESTMENT) / INITIAL_INVESTMENT
	drawdown = (portfolio_df['Market Value'].sum() + last_end_line_available - INITIAL_INVESTMENT) / INITIAL_INVESTMENT
	summary_data['Calmar Ratio'].append((return_ / drawdown) * 100)
	summary_data['Relative Drawdown'].append((drawdown / statement_df['End Line Available'].max()) * 100)
	summary_data['Maximum Drawdown'].append(drawdown)

	summary_data['%Return'].append(return_ * 100)

	return summary_data

def summarize_results(initial_balance, start_line_available):  # TODO: connect with trading logic
	portfolio_data = calculate_portfolio_data()
	portfolio_df = pd.DataFrame(portfolio_data)
	
	statement_data = calculate_statement_data(initial_balance)
	statement_df = pd.DataFrame(statement_data)

	summary_data = calculate_summary_data(portfolio_df, statement_df, start_line_available)
	summary_df = pd.DataFrame(summary_data)

	return portfolio_df, statement_df, summary_df

################################################################################
# working with files

def load_previous_df(team_name, file_type):
	# load data from previous day

    folder_path = os.path.join(OUTPUT_DIR, "Previous", file_type)
    file_path = os.path.join(folder_path, f"{team_name}_{file_type}.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        data = pd.read_csv(file_path)
        print(f"Loaded '{file_type}' data for team {team_name}.")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")

    return None

def get_money_data(prev_summary_df: pd.DataFrame) -> list[int, int]:
	# return initial_balance and start_line_available

	initial_balance = INITIAL_INVESTMENT
	start_line_available = INITIAL_INVESTMENT

	if not prev_summary_df:  # ใช้ค่าตั้งต้นหากไฟล์ไม่โหลด
		print(f"Initial balance = initial_investment: {INITIAL_INVESTMENT}")
		return initial_balance, start_line_available

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

def save_output(data: pd.DataFrame, team_name, file_type):
	folder_path = os.path.join(OUTPUT_DIR, "Result", file_type)
	file_path = os.path.join(folder_path, f"{team_name}_{file_type}.csv")

	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
		print(f"Directory created: '{folder_path}'")

	data.to_csv(file_path, index=False)
	print(f"{file_type} saved at {file_path}")

################################################################################

def main():
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)
		print(f"Created main directory: {OUTPUT_DIR}")

	daily_ticks_path = os.path.join(ROOT_DIR, "Daily_Ticks.csv")
	daily_ticks_df = pd.read_csv(daily_ticks_path)

	prev_summary_df = load_previous_df(TEAM_NAME, "Summary")
	initial_balance, start_line_available = get_money_data(prev_summary_df)

	# TODO: Do some preprocessing and calculation here

	portfolio_df, statement_df, summary_df = summarize_results(initial_balance, start_line_available)
	save_output(portfolio_df, TEAM_NAME, "portfolio")
	save_output(statement_df, TEAM_NAME, "statement")
	save_output(summary_df, TEAM_NAME, "summary")

if __name__ == "__main__":
	main()
