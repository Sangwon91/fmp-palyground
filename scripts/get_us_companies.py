import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키 가져오기
API_KEY = os.getenv('FMP_API_KEY')

# 미국 주요 거래소 목록
US_EXCHANGES = ['NYSE', 'NASDAQ', 'AMEX']  # OTC는 제외 (너무 많은 종목이 있음)

def get_us_companies():
    """
    FMP API를 사용하여 미국 거래소에 상장된 모든 기업의 정보를 가져옵니다.
    """
    url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}'
    print(f'Fetching stock list from: {url}')
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        print(f'Response status code: {response.status_code}')
        all_stocks = response.json()
        print(f'Total stocks fetched: {len(all_stocks)}')
        
        # 미국 거래소의 주식만 필터링
        us_companies = [
            stock for stock in all_stocks
            if stock.get('exchangeShortName') in US_EXCHANGES
            and stock.get('type') == 'stock'
        ]
        
        print(f'\n미국 주요 거래소별 기업 수:')
        for exchange in US_EXCHANGES:
            count = sum(1 for company in us_companies if company['exchangeShortName'] == exchange)
            print(f'{exchange}: {count}개 기업')
        
        return us_companies
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching stock list: {e}')
        return []

def save_to_json(data, filename):
    """
    데이터를 JSON 파일로 저장합니다.
    """
    # assets 디렉토리가 없으면 생성
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    # 파일 저장
    file_path = assets_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f'\n데이터가 {file_path}에 저장되었습니다.')
    
    # 저장된 데이터의 첫 번째 항목 출력 (샘플)
    if data:
        print('\n저장된 데이터 샘플 (첫 번째 항목):')
        print(json.dumps(data[0], indent=2))

def main():
    # 미국 기업 정보 가져오기
    companies = get_us_companies()
    
    if not companies:
        print('기업 정보를 가져오는데 실패했습니다.')
        return
    
    # 결과 출력
    print(f'\n총 {len(companies)}개의 미국 기업 정보를 가져왔습니다.')
    
    # JSON 파일로 저장
    save_to_json(companies, 'us_companies.json')

if __name__ == '__main__':
    main() 