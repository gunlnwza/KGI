import pandas as pd
import numpy as np
import os
from datetime import datetime, time

TEAM_NAME = "003_MooDengJengJing"
INITIAL_INVESTMENT = 10000000  # must be positive
OUTPUT_DIR = "competition_api"


def init_portfolio_data() -> dict:
	PORTFOLIO_FIELDS = [
		'Table Name', 'File Name', 'Stock name', 'Start Vol', 'Actual Vol',
		'Avg Cost', 'Market Price', 'Market Value', 'Amount Cost', 'Unrealized P/L',
		'% Unrealized P/L', 'Realized P/L'
	]
	return {field_name: [] for field_name in PORTFOLIO_FIELDS}

def init_statement_data() -> dict:
	STATEMENT_FIELDS = [
		'Table Name', 'File Name', 'Stock Name', 'Date', 'Time',
		'Side', 'Volume', 'Price', 'Amount Cost', 'End Line Available'
	]
	return {field_name: [] for field_name in STATEMENT_FIELDS}

def init_summary_data() -> dict:
	SUMMARY_FIELDS = [
		'Table Name', 'File Name', 'trading_day', 'NAV', 'Portfolio value',
		'End Line available', 'Start Line available', 'Number of wins', 'Number of matched trades', 'Number of transactions:',
		'Net Amount', 'Unrealized P/L', '% Unrealized P/L', 'Realized P/L', 'Maximum value',
		'Minimum value', 'Win rate', 'Calmar Ratio', 'Relative Drawdown', 'Maximum Drawdown',
		'%Return'
	]
	return {field_name: [] for field_name in SUMMARY_FIELDS}

def calculate_nav():
	return

def calculate_portfolio_value():
	return

"""
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
"""

def calculate_summary_data(portfolio_df, statement_df):
	summary_data = init_summary_data()

	start_line_available = INITIAL_INVESTMENT
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

	calmar_ratio = ((portfolio_df['Market Value'].sum() + last_end_line_available - INITIAL_INVESTMENT) / INITIAL_INVESTMENT * 100) / \
						((portfolio_df['Market Value'].sum() + last_end_line_available - INITIAL_INVESTMENT) / INITIAL_INVESTMENT)
	summary_data['Calmar Ratio'].append(calmar_ratio)
	summary_data['Relative Drawdown'].append()
	summary_data['Maximum Drawdown'].append()

	summary_data['%Return'].append()

	return summary_data

def calculate():
	portfolio_data = init_portfolio_data()
	portfolio_df = pd.DataFrame(portfolio_data)
	
	statement_data = init_statement_data()
	statement_df = pd.DataFrame(statement_data)

	summary_data = calculate_summary_data(portfolio_df, statement_df)
	summary_df = pd.DataFrame(summary_data)

	return portfolio_df, statement_df, summary_df


def save_output(data: pd.DataFrame, team_name, file_type):
	folder_path = os.path.join(OUTPUT_DIR, "Result", file_type)
	file_path = os.path.join(folder_path, f"{team_name}_{file_type}.csv")

	if not os.path.exists(folder_path):
		os.makedirs(folder_path, exist_ok=True)
		print(f"Directory created: '{folder_path}'")

	data.to_csv(file_path, index=False)
	print(f"{file_type} saved at {file_path}")


def main():
	# output_dir = os.path.expanduser("~/Desktop/competition_api")
	output_dir = OUTPUT_DIR
	if not os.path.exists(output_dir):
		os.makedirs(output_dir, exist_ok=True)
		print(f"Created main directory: {output_dir}")

	# file_path = '~/Desktop/Daily_Ticks.csv'
	daily_ticks_path = "Daily_Ticks_small.csv"
	daily_ticks_df = pd.read_csv(daily_ticks_path)

	portfolio_df, statement_df, summary_df = calculate()

	save_output(portfolio_df, TEAM_NAME, "portfolio")
	save_output(statement_df, TEAM_NAME, "statement")
	save_output(summary_df, TEAM_NAME, "summary")

if __name__ == "__main__":
	main()
