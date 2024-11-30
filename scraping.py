# Thêm các thư viện cần thiết
import requests
import os
import csv
import time
import pandas as pd
from datetime import datetime

# Xác nhận các dữ liệu
symbol = "SOLUSDT"
interval = "1m"  # 1m, 3m, 5m, 30m
start_date ="2024-9-30"
end_date = "2024-11-30"

# def inputInfor():
#     global symbol, interval, start_date, end_date
#     symbol = input('Nhập Tên Crpyto cần kiểm tra \n Tên nhập theo yêu cầu: Tên viết tắt của Crpyto viết hoa viết liền với tỉ giá [USDT]: ')
#     interval = input('''Nhập khoảng thời gian của mỗi nến\n Chỉ nhập ['1m','3m','5m','30m']: ''')
#     start_date = input('Nhập ngày bắt đầu thu thập [yyyy-mm-dd]: ')
#     end_date = input('Nhập ngày kết thúc thu thập [yyyy-mm-dd]: ')

# # inputInfor()
def scrapingData(symbol,interval,start_date,end_date):
    start_time = int(time.mktime(time.strptime(start_date, '%Y-%m-%d'))) * 1000
    end_time = int(time.mktime(time.strptime(end_date, '%Y-%m-%d'))) * 1000
    data = []

    # Lấy dữ liệu nến
    while start_time < end_time:
        url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=1000&startTime={start_time}&endTime={end_time}'
        # Gửi yêu cầu
        response = requests.get(url)
        
        if response.status_code == 200:
            candles = response.json()
            if not candles:  # Nếu không còn nến nào, dừng lại
                break
            data.extend(candles)
            
            # Cập nhật start_time cho yêu cầu tiếp theo
            start_time = candles[-1][0] + 1  # Lấy thời gian mở của nến cuối cùng
        else:
            print(f"Error: {response.status_code}, {response.text}")
            break

    # Chuyển đổi dữ liệu thành DataFrame để dễ xử lý
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume','Ignor']
    data = pd.DataFrame(data, columns=columns)
    data.to_csv('D:\Python\Predict_Price_Token\stokeData.csv',index=False)