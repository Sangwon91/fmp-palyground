# FMP Playground: Financial Statements Database Builder

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [시스템 요구사항](#시스템-요구사항)
3. [프로젝트 구조](#프로젝트-구조)
4. [설치 및 설정](#설치-및-설정)
5. [주요 기능](#주요-기능)
6. [API 문서](#api-문서)
7. [데이터 모델](#데이터-모델)
8. [사용 예시](#사용-예시)
9. [개발 가이드](#개발-가이드)
10. [문제 해결](#문제-해결)

## 프로젝트 개요

FMP Playground는 다양한 기업의 재무제표(Financial Statements) 데이터베이스를 구축하기 위한 Python 기반 프로젝트입니다. 이 프로젝트는 Financial Modeling Prep(FMP) API를 활용하여 전 세계 기업들의 재무 데이터를 수집하고 관리합니다.

### 주요 특징
- 전 세계 다양한 거래소의 기업 데이터 수집
- 기업별 상세 재무제표 데이터 수집
- 국가별, 거래소별 기업 정보 관리
- 효율적인 데이터 수집 및 저장 시스템
- 확장 가능한 모듈식 구조

## 시스템 요구사항

### 필수 요구사항
- Python 3.10 이상
- 패키지 의존성:
  - pandas >= 2.2.3
  - python-dotenv >= 1.1.0
  - requests >= 2.32.3

### 권장 사항
- 충분한 저장 공간 (수집된 데이터 저장용)
- 안정적인 인터넷 연결
- FMP API 키 (유료/무료)

## 프로젝트 구조

```
fmp-playground/
├── src/
│   └── fmp_playground/
│       ├── __init__.py
│       ├── fetch_financial_data.py
│       └── py.typed
├── scripts/
│   ├── fetch_all_companies_data.py
│   ├── fetch_financial_data.py
│   ├── get_companies_by_country.py
│   ├── get_countries.py
│   └── get_exchanges.py
├── docs/
│   ├── financial_statements_api.md
│   └── supported_countries.md
├── data/
├── assets/
├── pyproject.toml
├── README.md
└── .env
```

### 디렉토리 설명

#### src/fmp_playground/
- 프로젝트의 핵심 소스 코드
- 재무 데이터 수집을 위한 주요 기능 구현
- 타입 힌팅 지원 (py.typed)

#### scripts/
- 데이터 수집 및 관리를 위한 실행 스크립트
- 각 스크립트별 독립적인 기능 수행
- 자동화된 데이터 수집 프로세스

#### docs/
- API 문서 및 지원 국가 목록
- 프로젝트 문서화
- 사용자 가이드

## 설치 및 설정

### 1. 프로젝트 설치
```bash
# 저장소 클론
git clone https://github.com/your-username/fmp-playground.git
cd fmp-playground

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# 의존성 설치
pip install -e .
```

### 2. 환경 설정
1. `.env.example` 파일을 `.env`로 복사
2. FMP API 키 설정:
```
FMP_API_KEY=your_api_key_here
```

## 주요 기능

### 1. 기업 데이터 수집 (fetch_all_companies_data.py)
- 전체 기업 목록 수집
- 기업별 기본 정보 저장
- 증분 업데이트 지원

### 2. 재무제표 데이터 수집 (fetch_financial_data.py)
- 손익계산서
- 재무상태표
- 현금흐름표
- 주요 재무 비율

### 3. 국가별 기업 정보 (get_companies_by_country.py)
- 국가별 기업 목록 조회
- 필터링 및 정렬 기능
- 데이터 내보내기

### 4. 거래소 정보 관리 (get_exchanges.py)
- 전 세계 거래소 목록
- 거래소별 기업 수
- 거래소 상세 정보

## API 문서

### 핵심 클래스 및 함수

#### FinancialDataFetcher
```python
class FinancialDataFetcher:
    """재무 데이터 수집을 위한 주요 클래스"""
    
    def fetch_income_statement(self, symbol: str) -> pd.DataFrame:
        """손익계산서 데이터 수집"""
        
    def fetch_balance_sheet(self, symbol: str) -> pd.DataFrame:
        """재무상태표 데이터 수집"""
        
    def fetch_cash_flow(self, symbol: str) -> pd.DataFrame:
        """현금흐름표 데이터 수집"""
```

#### CompanyDataManager
```python
class CompanyDataManager:
    """기업 정보 관리 클래스"""
    
    def get_companies_list(self) -> List[Dict]:
        """전체 기업 목록 조회"""
        
    def get_company_profile(self, symbol: str) -> Dict:
        """기업 상세 정보 조회"""
```

## 데이터 모델

### 1. 기업 정보 스키마
```python
CompanyInfo = {
    "symbol": str,          # 기업 심볼
    "name": str,           # 기업명
    "exchange": str,       # 상장 거래소
    "country": str,        # 국가
    "industry": str,       # 산업 분류
    "sector": str,         # 섹터
    "marketCap": float,    # 시가총액
    "currency": str        # 통화
}
```

### 2. 재무제표 스키마
```python
FinancialStatement = {
    "date": str,           # 보고서 일자
    "symbol": str,         # 기업 심볼
    "period": str,         # 보고 기간
    "currency": str,       # 통화
    "items": Dict[str, float]  # 재무제표 항목
}
```

## 사용 예시

### 1. 기본 사용법

```python
from fmp_playground import FinancialDataFetcher

# 데이터 수집기 초기화
fetcher = FinancialDataFetcher()

# 특정 기업의 재무제표 수집
symbol = "AAPL"
income_statement = fetcher.fetch_income_statement(symbol)
balance_sheet = fetcher.fetch_balance_sheet(symbol)
cash_flow = fetcher.fetch_cash_flow(symbol)

# 데이터 저장
income_statement.to_csv(f"data/{symbol}_income_statement.csv")
```

### 2. 국가별 기업 조회

```python
from scripts.get_companies_by_country import get_companies

# 한국 기업 목록 조회
korean_companies = get_companies("KR")

# 결과 출력
for company in korean_companies:
    print(f"Symbol: {company['symbol']}, Name: {company['name']}")
```

### 3. 거래소 정보 조회

```python
from scripts.get_exchanges import get_exchange_info

# 전체 거래소 목록
exchanges = get_exchange_info()

# 거래소별 기업 수 출력
for exchange in exchanges:
    print(f"{exchange['name']}: {exchange['company_count']} companies")
```

## 개발 가이드

### 1. 코드 스타일
- PEP 8 준수
- Type hints 사용
- 문서화 문자열(Docstrings) 필수

### 2. 개발 프로세스
1. 기능 개발
2. 테스트 작성
3. 문서화
4. 코드 리뷰
5. 배포

### 3. 확장 가이드
새로운 데이터 소스 추가:
1. `src/fmp_playground/` 에 새로운 모듈 생성
2. 기존 인터페이스 준수
3. 테스트 케이스 작성
4. 문서 업데이트

## 문제 해결

### 일반적인 문제

#### 1. API 호출 실패
- API 키 확인
- 요청 제한 확인
- 네트워크 연결 상태 확인

#### 2. 데이터 불일치
- 원본 데이터 확인
- 변환 프로세스 검증
- 로그 확인

#### 3. 성능 이슈
- 배치 처리 사용
- 캐싱 구현
- 병렬 처리 고려

### 문제 보고
- GitHub Issues 사용
- 상세한 재현 방법 제공
- 로그 및 오류 메시지 첨부

## 라이선스 및 기여

### 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

### 기여 방법
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 업데이트 내역

### v0.1.0
- 초기 버전 릴리스
- 기본 데이터 수집 기능 구현
- 문서화 완료

## 향후 계획

### 단기 목표
- 데이터 검증 시스템 구축
- API 호출 최적화
- 사용자 인터페이스 개선

### 장기 목표
- 실시간 데이터 업데이트
- 머신러닝 모델 통합
- 데이터 시각화 도구 개발

## 참고 자료

### 외부 리소스
- [Financial Modeling Prep API 문서](https://financialmodelingprep.com/developer/docs)
- [Python 재무 데이터 분석 가이드](https://pandas.pydata.org/docs/) 