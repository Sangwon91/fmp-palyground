import json
import os
from typing import Any
import requests
import pandas as pd
from datetime import datetime

class FMPFinancialDataFetcher:
    """FMP API를 사용하여 기업의 재무제표 데이터를 조회하는 클래스.
    
    Parameters
    ----------
    api_key : str
        FMP API 키
    
    Attributes
    ----------
    base_url : str
        FMP API의 기본 URL
    """
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v3"
    
    def _make_request(self, endpoint: str, params: dict[str, Any] | None = None) -> dict:
        """API 요청을 보내는 메서드.
        
        Parameters
        ----------
        endpoint : str
            API 엔드포인트
        params : dict[str, Any] | None, optional
            요청 파라미터, by default None
            
        Returns
        -------
        dict
            API 응답 데이터
            
        Raises
        ------
        requests.exceptions.RequestException
            API 요청 중 오류 발생 시
        """
        if params is None:
            params = {}
        
        params['apikey'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_income_statement(self, symbol: str, period: str = 'annual', limit: int = 5) -> dict:
        """손익계산서 데이터 조회.
        
        Parameters
        ----------
        symbol : str
            기업 심볼
        period : str, optional
            데이터 주기 ('annual' 또는 'quarter'), by default 'annual'
        limit : int, optional
            조회할 데이터 수, by default 5
            
        Returns
        -------
        dict
            손익계산서 데이터
        """
        return self._make_request(f'income-statement/{symbol}', {'period': period, 'limit': limit})
    
    def get_balance_sheet(self, symbol: str, period: str = 'annual', limit: int = 5) -> dict:
        """재무상태표 데이터 조회.
        
        Parameters
        ----------
        symbol : str
            기업 심볼
        period : str, optional
            데이터 주기 ('annual' 또는 'quarter'), by default 'annual'
        limit : int, optional
            조회할 데이터 수, by default 5
            
        Returns
        -------
        dict
            재무상태표 데이터
        """
        return self._make_request(f'balance-sheet-statement/{symbol}', {'period': period, 'limit': limit})
    
    def get_cash_flow(self, symbol: str, period: str = 'annual', limit: int = 5) -> dict:
        """현금흐름표 데이터 조회.
        
        Parameters
        ----------
        symbol : str
            기업 심볼
        period : str, optional
            데이터 주기 ('annual' 또는 'quarter'), by default 'annual'
        limit : int, optional
            조회할 데이터 수, by default 5
            
        Returns
        -------
        dict
            현금흐름표 데이터
        """
        return self._make_request(f'cash-flow-statement/{symbol}', {'period': period, 'limit': limit})
    
    def get_financial_ratios(self, symbol: str, period: str = 'annual', limit: int = 5) -> dict:
        """재무비율 데이터 조회.
        
        Parameters
        ----------
        symbol : str
            기업 심볼
        period : str, optional
            데이터 주기 ('annual' 또는 'quarter'), by default 'annual'
        limit : int, optional
            조회할 데이터 수, by default 5
            
        Returns
        -------
        dict
            재무비율 데이터
        """
        return self._make_request(f'ratios/{symbol}', {'period': period, 'limit': limit})
    
    def get_key_metrics(self, symbol: str, period: str = 'annual', limit: int = 5) -> dict:
        """주요 메트릭스 데이터 조회.
        
        Parameters
        ----------
        symbol : str
            기업 심볼
        period : str, optional
            데이터 주기 ('annual' 또는 'quarter'), by default 'annual'
        limit : int, optional
            조회할 데이터 수, by default 5
            
        Returns
        -------
        dict
            주요 메트릭스 데이터
        """
        return self._make_request(f'key-metrics/{symbol}', {'period': period, 'limit': limit})
    
    def get_ltm_data(self, symbol: str) -> dict:
        """LTM 데이터 조회.
        
        Parameters
        ----------
        symbol : str
            기업 심볼
            
        Returns
        -------
        dict
            LTM 데이터 (손익계산서, 재무상태표, 현금흐름표)
        """
        return {
            'income_statement': self._make_request(f'income-statement-ltm/{symbol}'),
            'balance_sheet': self._make_request(f'balance-sheet-statement-ltm/{symbol}'),
            'cash_flow': self._make_request(f'cash-flow-statement-ltm/{symbol}')
        }

def load_korean_companies() -> list[dict]:
    """한국 기업 목록을 로드.
    
    Returns
    -------
    list[dict]
        한국 기업 목록 (KOSPI + KOSDAQ)
    """
    companies = []
    
    # KOSPI 기업 로드
    with open('assets/KR_KSC_companies.json', 'r', encoding='utf-8') as f:
        companies.extend(json.load(f))
    
    # KOSDAQ 기업 로드
    with open('assets/KR_KOE_companies.json', 'r', encoding='utf-8') as f:
        companies.extend(json.load(f))
    
    return companies

def main():
    # API 키 환경변수에서 로드
    api_key = os.getenv('FMP_API_KEY')
    if not api_key:
        raise ValueError("FMP_API_KEY 환경변수를 설정해주세요.")
    
    # 데이터 fetcher 초기화
    fetcher = FMPFinancialDataFetcher(api_key)
    
    # 한국 기업 목록 로드
    companies = load_korean_companies()
    
    # 테스트를 위해 첫 번째 기업 선택 (삼성전자)
    test_company = next(company for company in companies if company['symbol'] == '005930.KS')
    print(f"테스트 기업: {test_company['name']} ({test_company['symbol']})")
    
    try:
        # 재무제표 데이터 조회
        symbol = test_company['symbol']
        
        # 1. 연간 데이터 조회
        print("\n1. 연간 재무제표 데이터 조회 중...")
        income_stmt = fetcher.get_income_statement(symbol)
        balance_sheet = fetcher.get_balance_sheet(symbol)
        cash_flow = fetcher.get_cash_flow(symbol)
        
        # 2. LTM 데이터 조회
        print("\n2. LTM 데이터 조회 중...")
        ltm_data = fetcher.get_ltm_data(symbol)
        
        # 3. 재무비율 및 메트릭스 조회
        print("\n3. 재무비율 및 메트릭스 조회 중...")
        ratios = fetcher.get_financial_ratios(symbol)
        metrics = fetcher.get_key_metrics(symbol)
        
        # 결과 저장
        output_dir = 'data/financial_statements'
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"{output_dir}/{symbol.replace('.', '_')}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'company_info': test_company,
                'annual_data': {
                    'income_statement': income_stmt,
                    'balance_sheet': balance_sheet,
                    'cash_flow': cash_flow,
                    'ratios': ratios,
                    'metrics': metrics
                },
                'ltm_data': ltm_data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n데이터가 성공적으로 저장되었습니다: {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == '__main__':
    main() 