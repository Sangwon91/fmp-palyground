#!/usr/bin/env python
"""
기업의 재무제표 데이터를 조회하는 스크립트.

Example
-------
# 삼성전자(한국)
$ python scripts/fetch_kr_financial_data.py --symbol 005930.KS

# Apple(미국)
$ python scripts/fetch_kr_financial_data.py --symbol AAPL

# Toyota(일본)
$ python scripts/fetch_kr_financial_data.py --symbol 7203.T

# Kweichow Moutai(중국)
$ python scripts/fetch_kr_financial_data.py --symbol 600519.SS
"""

import os
import json
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

from fmp_playground.fetch_financial_data import (
    FMPFinancialDataFetcher,
    find_company_by_symbol
)

def setup_argparser() -> argparse.ArgumentParser:
    """커맨드라인 인자 파서를 설정.
    
    Returns
    -------
    argparse.ArgumentParser
        설정된 인자 파서
    """
    parser = argparse.ArgumentParser(description='기업의 재무제표 데이터를 조회')
    parser.add_argument('--symbol', type=str, default='005930.KS',
                       help='조회할 기업의 심볼 (예: 005930.KS, AAPL, 7203.T)')
    return parser

def fetch_financial_data(fetcher: FMPFinancialDataFetcher, symbol: str, period: str = 'annual') -> dict:
    """특정 기간(연간/분기)의 재무제표 데이터를 조회.
    
    Parameters
    ----------
    fetcher : FMPFinancialDataFetcher
        데이터 조회 객체
    symbol : str
        기업 심볼
    period : str, optional
        데이터 주기 ('annual' 또는 'quarter'), by default 'annual'
        
    Returns
    -------
    dict
        조회된 재무제표 데이터
    """
    period_text = "연간" if period == 'annual' else "분기별"
    print(f"\n{period_text} 재무제표 데이터 조회 중...")
    
    return {
        'income_statement': fetcher.get_income_statement(symbol, period=period),
        'balance_sheet': fetcher.get_balance_sheet(symbol, period=period),
        'cash_flow': fetcher.get_cash_flow(symbol, period=period),
        'ratios': fetcher.get_financial_ratios(symbol, period=period),
        'metrics': fetcher.get_key_metrics(symbol, period=period)
    }

def main():
    """메인 함수."""
    # 환경변수 로드
    env_path = Path('.env')
    if not env_path.exists():
        raise FileNotFoundError(
            ".env 파일이 없습니다. 다음 형식으로 .env 파일을 생성해주세요:\n"
            "FMP_API_KEY=your_api_key_here"
        )
    
    load_dotenv()
    api_key = os.getenv('FMP_API_KEY')
    if not api_key:
        raise ValueError("FMP_API_KEY 환경변수가 설정되지 않았습니다.")
    
    # 커맨드라인 인자 파싱
    parser = setup_argparser()
    args = parser.parse_args()
    
    # 데이터 fetcher 초기화
    fetcher = FMPFinancialDataFetcher(api_key)
    
    # 심볼로 기업 정보와 국가 찾기
    company, country = find_company_by_symbol(args.symbol)
    print(f"대상 기업: {company['name']} ({company['symbol']}, {country})")
    
    try:
        # 1. 연간 데이터 조회
        annual_data = fetch_financial_data(fetcher, args.symbol, 'annual')
        
        # 2. 분기별 데이터 조회
        quarterly_data = fetch_financial_data(fetcher, args.symbol, 'quarter')
        
        # 3. LTM 데이터 조회
        print("\nLTM 데이터 조회 중...")
        ltm_data = fetcher.get_ltm_data(args.symbol)
        
        # 4. TTM 데이터 조회
        print("\nTTM 데이터 조회 중...")
        ttm_data = fetcher.get_ttm_data(args.symbol)
        
        # 결과 저장
        output_dir = Path('data/financial_statements')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = output_dir / f"{args.symbol.replace('.', '_')}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'company_info': company,
                'country': country,
                'annual_data': annual_data,
                'quarterly_data': quarterly_data,
                'ltm_data': ltm_data,
                'ttm_data': ttm_data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n데이터가 성공적으로 저장되었습니다: {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == '__main__':
    main() 