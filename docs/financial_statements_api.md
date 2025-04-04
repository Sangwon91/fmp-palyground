# FMP 재무제표 데이터 조회 가이드

이 문서는 Financial Modeling Prep (FMP) API를 사용하여 기업의 재무제표 데이터를 조회하는 방법을 설명합니다.

## 기본 정보

- 모든 API 요청에는 API 키가 필요합니다
- URL 끝에 `?apikey=YOUR_API_KEY` 를 추가해야 합니다
- 다른 파라미터가 있는 경우 `&apikey=YOUR_API_KEY` 를 사용합니다

## 재무제표 데이터 조회

### 1. 손익계산서 (Income Statement)

```
# 연간 데이터
https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&limit=5

# 분기 데이터
https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=quarter&limit=20

# LTM(Last Twelve Months) 데이터
https://financialmodelingprep.com/api/v3/income-statement-ltm/{symbol}
```

### 2. 재무상태표 (Balance Sheet)

```
# 연간 데이터
https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?period=annual&limit=5

# 분기 데이터
https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?period=quarter&limit=20

# LTM 데이터
https://financialmodelingprep.com/api/v3/balance-sheet-statement-ltm/{symbol}
```

### 3. 현금흐름표 (Cash Flow Statement)

```
# 연간 데이터
https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?period=annual&limit=5

# 분기 데이터
https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?period=quarter&limit=20

# LTM 데이터
https://financialmodelingprep.com/api/v3/cash-flow-statement-ltm/{symbol}
```

### 4. 주요 재무비율 (Financial Ratios)

```
# 연간 데이터
https://financialmodelingprep.com/api/v3/ratios/{symbol}?period=annual&limit=5

# 분기 데이터
https://financialmodelingprep.com/api/v3/ratios/{symbol}?period=quarter&limit=20

# TTM 데이터
https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}
```

### 5. 주요 메트릭스 (Key Metrics)

```
# 연간 데이터
https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?period=annual&limit=5

# 분기 데이터
https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?period=quarter&limit=20

# TTM 데이터
https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}
```

### 6. 성장지표 (Growth Indicators)

```
# 재무 성장 지표
https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?period=annual&limit=5

# 손익계산서 성장 지표
https://financialmodelingprep.com/api/v3/income-statement-growth/{symbol}?period=annual&limit=5

# 재무상태표 성장 지표
https://financialmodelingprep.com/api/v3/balance-sheet-statement-growth/{symbol}?period=annual&limit=5

# 현금흐름표 성장 지표
https://financialmodelingprep.com/api/v3/cash-flow-statement-growth/{symbol}?period=annual&limit=5
```

### 7. 기업가치평가 지표 (Enterprise Values)

```
# 연간 데이터
https://financialmodelingprep.com/api/v3/enterprise-values/{symbol}?period=annual&limit=5

# 분기 데이터
https://financialmodelingprep.com/api/v3/enterprise-values/{symbol}?period=quarter&limit=20
```

## 참고사항

1. `{symbol}` 부분에는 실제 기업의 티커 심볼을 입력해야 합니다 (예: AAPL, MSFT)
2. `limit` 파라미터:
   - 연간 데이터의 경우 5로 설정하면 최근 5개년 데이터
   - 분기 데이터의 경우 20으로 설정하면 최근 5년치 분기 데이터
3. LTM/TTM 데이터는 최근 12개월 데이터를 의미하며, 가장 최신의 데이터를 제공
4. 일부 데이터는 기업이나 구독 플랜에 따라 제공되지 않을 수 있음

## 데이터 업데이트 주기

- 분기 데이터: 기업의 실적 발표 후 업데이트
- 연간 데이터: 연간 보고서 발표 후 업데이트
- LTM/TTM 데이터: 가장 최근 분기 실적 발표 후 업데이트 