import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키 가져오기
API_KEY = os.getenv('FMP_API_KEY')

def get_stock_list():
    """
    FMP API를 사용하여 전체 주식 목록을 가져옵니다.
    """
    url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}'
    print(f'Fetching stock list from: {url}')
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        print(f'Response status code: {response.status_code}')
        stocks = response.json()
        print(f'Total stocks fetched: {len(stocks)}')
        
        # 첫 번째 항목의 구조 출력
        if stocks:
            print('\nFirst stock item structure:')
            print(json.dumps(stocks[0], indent=2))
            
            # 거래소 정보 샘플 출력
            print('\nUnique exchange names in first 1000 items:')
            unique_exchanges = {(stock.get('exchange', ''), stock.get('exchangeShortName', '')) 
                              for stock in stocks[:1000]}
            for full_name, short_name in sorted(unique_exchanges):
                print(f'  {short_name}: {full_name}')
        
        return stocks
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching stock list: {e}')
        return []

def analyze_exchanges(stocks):
    """
    주식 목록에서 거래소 정보를 분석합니다.
    
    Parameters
    ----------
    stocks : list
        주식 목록 데이터
        
    Returns
    -------
    dict
        거래소 정보를 담은 딕셔너리
    """
    # 거래소 정보를 저장할 세트
    exchanges = set()
    exchange_info = {}
    
    for stock in stocks:
        exchange_short = stock.get('exchangeShortName', '')
        exchange_full = stock.get('exchange', '')
        type_ = stock.get('type', '')
        
        # 주식(stock)인 경우에만 처리
        if exchange_short and type_ == 'stock':
            exchanges.add(exchange_short)
            if exchange_short not in exchange_info:
                exchange_info[exchange_short] = {
                    'fullName': exchange_full,
                    'stockCount': 0
                }
            exchange_info[exchange_short]['stockCount'] += 1
    
    # 결과 출력
    print('\n거래소별 주식 수:')
    for exchange in sorted(exchange_info.keys()):
        info = exchange_info[exchange]
        print(f"{exchange} ({info['fullName']}): {info['stockCount']}개 주식")
    
    return {
        'exchanges': sorted(list(exchanges)),
        'exchangeInfo': exchange_info
    }

def save_to_json(data, filename):
    """
    데이터를 JSON 파일로 저장합니다.
    """
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    file_path = assets_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f'\n데이터가 {file_path}에 저장되었습니다.')

def main():
    # 전체 주식 목록 가져오기
    stocks = get_stock_list()
    
    if not stocks:
        print('주식 목록을 가져오는데 실패했습니다.')
        return
    
    # 거래소 분석
    exchange_data = analyze_exchanges(stocks)
    
    # JSON 파일로 저장
    save_to_json(exchange_data, 'exchanges.json')

if __name__ == '__main__':
    main() 