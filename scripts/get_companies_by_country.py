import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv
from typing import Dict, List

# 환경 변수 로드
load_dotenv()

# API 키 가져오기
API_KEY = os.getenv('FMP_API_KEY')

# 국가별 거래소 매핑
COUNTRY_EXCHANGES = {
    'US': ['NYSE', 'NASDAQ', 'AMEX'],
    'CN': ['SHH', 'SHZ'],
    'JP': ['JPX'],
    'KR': ['KSC', 'KOE']
}

def get_stock_list() -> List[Dict]:
    """
    FMP API를 사용하여 전체 주식 목록을 가져옵니다.
    
    Returns
    -------
    list
        주식 목록 데이터
    """
    url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}'
    print(f'Fetching stock list from: {url}')
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        print(f'Response status code: {response.status_code}')
        stocks = response.json()
        print(f'Total stocks fetched: {len(stocks)}')
        
        return stocks
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching stock list: {e}')
        return []

def filter_companies_by_country(stocks: List[Dict], country_code: str) -> Dict[str, List[Dict]]:
    """
    주식 목록에서 특정 국가의 거래소별 기업 정보를 필터링합니다.
    
    Parameters
    ----------
    stocks : list
        전체 주식 목록
    country_code : str
        국가 코드 (ISO 3166-1 alpha-2)
        
    Returns
    -------
    dict
        거래소별 기업 목록
    """
    if country_code not in COUNTRY_EXCHANGES:
        raise ValueError(f'지원하지 않는 국가 코드입니다: {country_code}')
    
    exchanges = COUNTRY_EXCHANGES[country_code]
    companies_by_exchange = {exchange: [] for exchange in exchanges}
    
    for stock in stocks:
        exchange = stock.get('exchangeShortName', '')
        type_ = stock.get('type', '')
        
        if exchange in exchanges and type_ == 'stock':
            companies_by_exchange[exchange].append(stock)
    
    return companies_by_exchange

def save_to_json(data: List[Dict], filename: str):
    """
    데이터를 JSON 파일로 저장합니다.
    
    Parameters
    ----------
    data : list
        저장할 데이터
    filename : str
        파일 이름
    """
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    file_path = assets_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f'데이터가 {file_path}에 저장되었습니다.')

def main():
    # 전체 주식 목록 가져오기
    stocks = get_stock_list()
    
    if not stocks:
        print('주식 목록을 가져오는데 실패했습니다.')
        return
    
    # 각 국가별로 처리
    for country_code in COUNTRY_EXCHANGES.keys():
        print(f'\n{country_code} 기업 정보 처리 중...')
        
        try:
            # 국가별 거래소 기업 정보 필터링
            companies_by_exchange = filter_companies_by_country(stocks, country_code)
            
            # 거래소별로 파일 저장
            for exchange, companies in companies_by_exchange.items():
                filename = f'{country_code}_{exchange}_companies.json'
                print(f'{exchange}: {len(companies)}개 기업')
                save_to_json(companies, filename)
                
        except Exception as e:
            print(f'{country_code} 처리 중 오류 발생: {e}')
            continue

if __name__ == '__main__':
    main() 