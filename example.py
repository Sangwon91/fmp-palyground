import os
import requests
import pandas as pd
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# FMP API 키 가져오기
FMP_API_KEY = os.getenv('FMP_API_KEY')
if not FMP_API_KEY:
    raise ValueError("FMP_API_KEY 환경 변수가 설정되지 않았습니다.")

def get_financial_statements(
    ticker_code,
    exchange=None,
    period='annual',
    limit=3,
    api_key=None
):
    """
    기업의 재무제표 정보를 FMP API를 통해 가져오는 함수
    
    Parameters
    ----------
    ticker_code : str
        종목코드 (예: '018290' for 위메이드, 'AAPL' for 애플)
    exchange : str, optional
        거래소 코드 (예: 'KQ' for KOSDAQ, 'KS' for KOSPI)
        미국 주식의 경우 None으로 설정
    period : str, optional
        'annual' 또는 'quarter' (기본값: 'annual')
    limit : int, optional
        가져올 재무제표의 수 (기본값: 3)
    api_key : str, optional
        FMP API 키 (기본값: 환경 변수에서 가져옴)
        
    Returns
    -------
    dict
        income_statement: 손익계산서 데이터프레임
        balance_sheet: 대차대조표 데이터프레임
        cash_flow: 현금흐름표 데이터프레임
    """
    # API 키 확인
    if api_key is None:
        api_key = FMP_API_KEY
    
    # 티커 심볼 형식 설정
    if exchange:
        # 한국 주식의 경우 (예: '018290.KQ')
        fmp_ticker = f"{ticker_code}.{exchange}"
        print(f"주의: FMP API의 무료 플랜은 미국 주식만 지원합니다. 한국 주식 데이터를 가져오려면 유료 플랜이 필요합니다.")
    else:
        # 미국 주식의 경우 (예: 'AAPL')
        fmp_ticker = ticker_code
    
    # 결과를 저장할 딕셔너리
    results = {}
    
    try:
        # 손익계산서(Income Statement) 가져오기
        income_url = f"https://financialmodelingprep.com/api/v3/income-statement/{fmp_ticker}?period={period}&limit={limit}&apikey={api_key}"
        income_response = requests.get(income_url)
        income_data = income_response.json()
        
        if isinstance(income_data, list) and len(income_data) > 0:
            income_df = pd.DataFrame(income_data)
            results['income_statement'] = income_df
            print(f"손익계산서 데이터 {len(income_df)}개 가져옴")
        else:
            print(f"손익계산서 데이터를 가져올 수 없습니다: {income_response.text}")
            results['income_statement'] = pd.DataFrame()
        
        # 대차대조표(Balance Sheet) 가져오기
        balance_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{fmp_ticker}?period={period}&limit={limit}&apikey={api_key}"
        balance_response = requests.get(balance_url)
        balance_data = balance_response.json()
        
        if isinstance(balance_data, list) and len(balance_data) > 0:
            balance_df = pd.DataFrame(balance_data)
            results['balance_sheet'] = balance_df
            print(f"대차대조표 데이터 {len(balance_df)}개 가져옴")
        else:
            print(f"대차대조표 데이터를 가져올 수 없습니다: {balance_response.text}")
            results['balance_sheet'] = pd.DataFrame()
        
        # 현금흐름표(Cash Flow Statement) 가져오기
        cash_flow_url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{fmp_ticker}?period={period}&limit={limit}&apikey={api_key}"
        cash_flow_response = requests.get(cash_flow_url)
        cash_flow_data = cash_flow_response.json()
        
        if isinstance(cash_flow_data, list) and len(cash_flow_data) > 0:
            cash_flow_df = pd.DataFrame(cash_flow_data)
            results['cash_flow'] = cash_flow_df
            print(f"현금흐름표 데이터 {len(cash_flow_df)}개 가져옴")
        else:
            print(f"현금흐름표 데이터를 가져올 수 없습니다: {cash_flow_response.text}")
            results['cash_flow'] = pd.DataFrame()
        
        return results
    
    except Exception as e:
        raise Exception(f"재무제표 데이터를 가져오는 중 오류 발생: {str(e)}")

def extract_financial_metrics(financial_data):
    """
    재무제표 데이터에서 주요 재무 지표를 추출하는 함수
    
    Parameters
    ----------
    financial_data : dict
        get_financial_statements 함수에서 반환된 딕셔너리
        
    Returns
    -------
    pandas.DataFrame
        주요 재무 지표가 포함된 데이터프레임
    """
    # 결과를 저장할 리스트
    results = []
    
    # 손익계산서 데이터 확인
    income_df = financial_data.get('income_statement', pd.DataFrame())
    balance_df = financial_data.get('balance_sheet', pd.DataFrame())
    cash_flow_df = financial_data.get('cash_flow', pd.DataFrame())
    
    # 데이터가 없는 경우 빈 데이터프레임 반환
    if income_df.empty and balance_df.empty and cash_flow_df.empty:
        return pd.DataFrame()
    
    # 손익계산서에서 날짜 정보 가져오기
    if not income_df.empty and 'date' in income_df.columns:
        dates = income_df['date'].tolist()
    elif not balance_df.empty and 'date' in balance_df.columns:
        dates = balance_df['date'].tolist()
    elif not cash_flow_df.empty and 'date' in cash_flow_df.columns:
        dates = cash_flow_df['date'].tolist()
    else:
        return pd.DataFrame()
    
    # 각 날짜별로 재무 지표 추출
    for date in dates:
        # 해당 날짜의 데이터 필터링
        income_row = income_df[income_df['date'] == date] if not income_df.empty else pd.DataFrame()
        balance_row = balance_df[balance_df['date'] == date] if not balance_df.empty else pd.DataFrame()
        cash_flow_row = cash_flow_df[cash_flow_df['date'] == date] if not cash_flow_df.empty else pd.DataFrame()
        
        # 재무 지표 추출
        metrics = {
            'Date': date,
            # 손익계산서 지표
            'Revenue': income_row['revenue'].values[0] if not income_row.empty and 'revenue' in income_row.columns else None,
            'Operating_Income': income_row['operatingIncome'].values[0] if not income_row.empty and 'operatingIncome' in income_row.columns else None,
            'Net_Income': income_row['netIncome'].values[0] if not income_row.empty and 'netIncome' in income_row.columns else None,
            'Gross_Profit': income_row['grossProfit'].values[0] if not income_row.empty and 'grossProfit' in income_row.columns else None,
            'COGS': income_row['costOfRevenue'].values[0] if not income_row.empty and 'costOfRevenue' in income_row.columns else None,
            'SG&A': income_row['sellingGeneralAndAdministrativeExpenses'].values[0] if not income_row.empty and 'sellingGeneralAndAdministrativeExpenses' in income_row.columns else None,
            
            # 현금흐름표 지표
            'Operating_Cash_Flow': cash_flow_row['operatingCashFlow'].values[0] if not cash_flow_row.empty and 'operatingCashFlow' in cash_flow_row.columns else None,
            
            # 대차대조표 지표
            'Total_Assets': balance_row['totalAssets'].values[0] if not balance_row.empty and 'totalAssets' in balance_row.columns else None,
            'Total_Liabilities': balance_row['totalLiabilities'].values[0] if not balance_row.empty and 'totalLiabilities' in balance_row.columns else None,
            'Total_Equity': balance_row['totalStockholdersEquity'].values[0] if not balance_row.empty and 'totalStockholdersEquity' in balance_row.columns else None,
        }
        
        results.append(metrics)
    
    # 데이터프레임 생성 및 정렬
    df = pd.DataFrame(results)
    if not df.empty:
        df.sort_values('Date', inplace=True)
        # 십억 단위로 변환 (FMP API는 기본적으로 USD 단위로 제공)
        for col in df.columns:
            if col != 'Date' and df[col].dtype == 'float64':
                df[col] = df[col] / 1e9  # 십억 단위로 변환
    
    return df

if __name__ == "__main__":
    print("FMP API를 사용한 재무제표 데이터 가져오기 예제")
    print("=" * 50)
    
    # 한국 주식 예시 (유료 플랜 필요)
    print("\n1. 한국 주식 예시 (위메이드, 018290.KQ)")
    print("주의: FMP API의 무료 플랜은 미국 주식만 지원합니다.")
    print("한국 주식 데이터를 가져오려면 유료 플랜이 필요합니다.")
    ticker_code = "018290"
    exchange = "KQ"  # KOSDAQ
    
    try:
        print(f"\n{ticker_code}.{exchange} 재무제표 데이터 가져오는 중...")
        financial_data = get_financial_statements(ticker_code, exchange, period='quarter', limit=3)
        
        # 주요 재무 지표 추출
        financial_metrics = extract_financial_metrics(financial_data)
        
        # 결과 출력
        if not financial_metrics.empty:
            print("\n주요 재무 지표 (십억원 단위):")
            print(financial_metrics)
        else:
            print("재무 지표를 추출할 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    
    # 미국 주식 예시 (무료 플랜에서 지원)
    print("\n2. 미국 주식 예시 (애플, AAPL)")
    ticker_code = "AAPL"
    exchange = None  # 미국 주식
    
    try:
        print(f"\n{ticker_code} 재무제표 데이터 가져오는 중...")
        financial_data = get_financial_statements(ticker_code, exchange, period='quarter', limit=3)
        
        # 주요 재무 지표 추출
        financial_metrics = extract_financial_metrics(financial_data)
        
        # 결과 출력
        if not financial_metrics.empty:
            print("\n주요 재무 지표 (십억 달러 단위):")
            print(financial_metrics)
        else:
            print("재무 지표를 추출할 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {str(e)}") 