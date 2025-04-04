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
import time
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from functools import wraps
from typing import Any, Callable

from fmp_playground.fetch_financial_data import (
    FMPFinancialDataFetcher,
    find_company_by_symbol
)

class TimingStats:
    """함수 실행 시간을 저장하고 관리하는 클래스."""
    
    def __init__(self):
        self.stats = {}
        self.total_time = 0
    
    def add_timing(self, name: str, elapsed: float) -> None:
        """실행 시간 정보를 추가.
        
        Parameters
        ----------
        name : str
            함수 또는 작업 이름
        elapsed : float
            실행 시간 (초)
        """
        self.stats[name] = elapsed
        self.total_time += elapsed
    
    def print_summary(self) -> None:
        """전체 실행 시간 요약을 출력."""
        print("\n실행 시간 요약:")
        for name, elapsed in self.stats.items():
            print(f"- {name}: {elapsed:.2f}초")
        print(f"- 전체 실행 시간: {self.total_time:.2f}초")

# 전역 타이밍 통계 객체
timing_stats = TimingStats()

def measure_time(task_name: str) -> Callable:
    """함수의 실행 시간을 측정하는 데코레이터.
    
    Parameters
    ----------
    task_name : str
        작업 이름
        
    Returns
    -------
    Callable
        데코레이터 함수
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            timing_stats.add_timing(task_name, elapsed_time)
            return result
        return wrapper
    return decorator

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

@measure_time('연간 데이터 조회')
def fetch_annual_data(fetcher: FMPFinancialDataFetcher, symbol: str) -> dict:
    """연간 재무제표 데이터를 조회.
    
    Parameters
    ----------
    fetcher : FMPFinancialDataFetcher
        데이터 조회 객체
    symbol : str
        기업 심볼
        
    Returns
    -------
    dict
        조회된 재무제표 데이터
    """
    print("\n연간 재무제표 데이터 조회 중...")
    return {
        'income_statement': fetcher.get_income_statement(symbol, period='annual'),
        'balance_sheet': fetcher.get_balance_sheet(symbol, period='annual'),
        'cash_flow': fetcher.get_cash_flow(symbol, period='annual'),
        'ratios': fetcher.get_financial_ratios(symbol, period='annual'),
        'metrics': fetcher.get_key_metrics(symbol, period='annual')
    }

@measure_time('분기별 데이터 조회')
def fetch_quarterly_data(fetcher: FMPFinancialDataFetcher, symbol: str) -> dict:
    """분기별 재무제표 데이터를 조회.
    
    Parameters
    ----------
    fetcher : FMPFinancialDataFetcher
        데이터 조회 객체
    symbol : str
        기업 심볼
        
    Returns
    -------
    dict
        조회된 재무제표 데이터
    """
    print("\n분기별 재무제표 데이터 조회 중...")
    return {
        'income_statement': fetcher.get_income_statement(symbol, period='quarter'),
        'balance_sheet': fetcher.get_balance_sheet(symbol, period='quarter'),
        'cash_flow': fetcher.get_cash_flow(symbol, period='quarter'),
        'ratios': fetcher.get_financial_ratios(symbol, period='quarter'),
        'metrics': fetcher.get_key_metrics(symbol, period='quarter')
    }

@measure_time('LTM 데이터 조회')
def fetch_ltm_data(fetcher: FMPFinancialDataFetcher, symbol: str) -> dict:
    """LTM 재무제표 데이터를 조회.
    
    Parameters
    ----------
    fetcher : FMPFinancialDataFetcher
        데이터 조회 객체
    symbol : str
        기업 심볼
        
    Returns
    -------
    dict
        조회된 재무제표 데이터
    """
    print("\nLTM 데이터 조회 중...")
    return fetcher.get_ltm_data(symbol)

@measure_time('TTM 데이터 조회')
def fetch_ttm_data(fetcher: FMPFinancialDataFetcher, symbol: str) -> dict:
    """TTM 재무제표 데이터를 조회.
    
    Parameters
    ----------
    fetcher : FMPFinancialDataFetcher
        데이터 조회 객체
    symbol : str
        기업 심볼
        
    Returns
    -------
    dict
        조회된 재무제표 데이터
    """
    print("\nTTM 데이터 조회 중...")
    return fetcher.get_ttm_data(symbol)

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
        annual_data = fetch_annual_data(fetcher, args.symbol)
        
        # 2. 분기별 데이터 조회
        quarterly_data = fetch_quarterly_data(fetcher, args.symbol)
        
        # 3. LTM 데이터 조회
        ltm_data = fetch_ltm_data(fetcher, args.symbol)
        
        # 4. TTM 데이터 조회
        ttm_data = fetch_ttm_data(fetcher, args.symbol)
        
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
        timing_stats.print_summary()
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == '__main__':
    main() 