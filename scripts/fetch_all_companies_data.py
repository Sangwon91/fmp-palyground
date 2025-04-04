#!/usr/bin/env python
"""
모든 기업의 재무제표 데이터를 수집하는 스크립트.

이 스크립트는 다음과 같은 특징을 가집니다:
1. 병렬 처리를 통한 빠른 데이터 수집
2. 이미 수집된 기업 데이터는 건너뛰기
3. 국가별로 균형있게 데이터 수집
4. API 호출 제한 고려 (300회/분)

Example
-------
$ python scripts/fetch_all_companies_data.py --workers 3
"""

import os
import random
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Set
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

from fmp_playground.fetch_financial_data import (
    load_companies
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('fetch_all_companies.log')
    ]
)
logger = logging.getLogger(__name__)

def setup_argparser() -> argparse.ArgumentParser:
    """커맨드라인 인자 파서를 설정.
    
    Returns
    -------
    argparse.ArgumentParser
        설정된 인자 파서
    """
    parser = argparse.ArgumentParser(description='모든 기업의 재무제표 데이터를 수집')
    parser.add_argument('--workers', type=int, default=3,
                       help='동시 실행할 워커 수 (기본값: 3)')
    return parser

def get_processed_companies() -> Set[str]:
    """이미 처리된 기업 목록을 가져옵니다.
    
    Returns
    -------
    Set[str]
        처리된 기업의 심볼 집합
    """
    processed = set()
    data_dir = Path('data/financial_statements')
    
    if not data_dir.exists():
        return processed
        
    for file in data_dir.glob('*_*.json'):
        # timestamp를 제외한 파일 이름에서 심볼 추출
        symbol = file.name.split('_')[0].replace('_', '.')
        processed.add(symbol)
        
    return processed

def distribute_companies(companies: List[Dict], processed: Set[str]) -> List[Dict]:
    """국가별로 균형있게 기업을 분배합니다.
    
    Parameters
    ----------
    companies : List[Dict]
        전체 기업 목록
    processed : Set[str]
        이미 처리된 기업 심볼 집합
        
    Returns
    -------
    List[Dict]
        처리할 기업 목록 (국가별로 분배됨)
    """
    # 국가별로 기업 분류
    companies_by_country = {}
    for company in companies:
        if company['symbol'] in processed:
            continue
        country = company.get('country', 'Unknown')
        if country not in companies_by_country:
            companies_by_country[country] = []
        companies_by_country[country].append(company)
    
    # 각 국가의 기업을 섞음
    for country in companies_by_country:
        random.shuffle(companies_by_country[country])
    
    # 국가별로 번갈아가며 기업을 선택
    distributed = []
    while any(companies_by_country.values()):
        for country in list(companies_by_country.keys()):
            if companies_by_country[country]:
                distributed.append(companies_by_country[country].pop())
            else:
                del companies_by_country[country]
    
    return distributed

def fetch_company_data(company: Dict, api_key: str) -> bool:
    """단일 기업의 재무제표 데이터를 수집합니다.
    
    Parameters
    ----------
    company : Dict
        기업 정보
    api_key : str
        FMP API 키
        
    Returns
    -------
    bool
        성공 여부
    """
    symbol = company['symbol']
    name = company['name']
    country = company.get('country', 'Unknown')
    
    try:
        logger.info(f"데이터 수집 시작: {name} ({symbol}, {country})")
        
        # 스크립트 실행
        cmd = f"python scripts/fetch_financial_data.py --symbol {symbol}"
        result = os.system(cmd)
        
        if result == 0:
            logger.info(f"데이터 수집 완료: {name} ({symbol}, {country})")
            return True
        else:
            logger.error(f"데이터 수집 실패: {name} ({symbol}, {country})")
            return False
            
    except Exception as e:
        logger.error(f"오류 발생 ({symbol}): {str(e)}")
        return False

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
    
    # 이미 처리된 기업 목록 가져오기
    processed = get_processed_companies()
    logger.info(f"이미 처리된 기업 수: {len(processed)}")
    
    # 전체 기업 목록 로드
    companies = load_companies()
    logger.info(f"전체 기업 수: {len(companies)}")
    
    # 국가별로 균형있게 기업 분배
    companies_to_process = distribute_companies(companies, processed)
    logger.info(f"처리할 기업 수: {len(companies_to_process)}")
    
    # 병렬 처리
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for company in companies_to_process:
            future = executor.submit(fetch_company_data, company, api_key)
            futures.append((future, company))
        
        # 결과 처리
        success = 0
        failure = 0
        for future, company in futures:
            try:
                if future.result():
                    success += 1
                else:
                    failure += 1
            except Exception as e:
                logger.error(f"작업 실패 ({company['symbol']}): {str(e)}")
                failure += 1
            
            # 진행 상황 출력
            total = success + failure
            if total % 10 == 0:
                logger.info(f"진행 상황: {total}/{len(companies_to_process)} "
                          f"(성공: {success}, 실패: {failure})")
    
    logger.info("\n처리 완료:")
    logger.info(f"- 성공: {success}")
    logger.info(f"- 실패: {failure}")
    logger.info(f"- 전체: {success + failure}")

if __name__ == '__main__':
    main() 