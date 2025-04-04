import os
from dotenv import load_dotenv
import requests
from typing import List

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

def get_all_countries() -> List[str]:
    """
    FMP API를 통해 지원되는 모든 국가 리스트를 조회합니다.
    
    Returns:
        List[str]: 지원되는 국가 리스트
    """
    # API 키는 환경 변수에서 가져옵니다
    api_key = os.getenv('FMP_API_KEY')
    if not api_key:
        raise ValueError("FMP_API_KEY 환경 변수가 설정되지 않았습니다.")
    
    # API 엔드포인트
    url = f"https://financialmodelingprep.com/api/v3/get-all-countries?apikey={api_key}"
    
    try:
        # API 요청
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 체크
        
        # 응답 데이터 반환
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")
        return []

if __name__ == "__main__":
    countries = get_all_countries()
    if countries:
        print("지원되는 국가 리스트:")
        for country in countries:
            print(f"- {country}")
    else:
        print("국가 리스트를 가져오는데 실패했습니다.") 