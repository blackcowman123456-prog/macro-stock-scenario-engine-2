# Macro → Stock Scenario Engine v2

## 실행
pip install -r requirements.txt
streamlit run app.py

## 배포
Streamlit Community Cloud에서 GitHub repository와 app.py를 연결한다.

## API secrets
실전 매크로 데이터를 연결할 때:
FRED_API_KEY
ECOS_API_KEY
KOSIS_API_KEY

를 Streamlit Secrets에 저장한다. 소스 코드에 키를 넣지 않는다.

## 주의
현재 시나리오 확률과 종목 예상 범위는 프로토타입 표시값이다.
실전 서비스에서는 Point-in-Time 데이터, 실제 학습 모델, walk-forward backtest,
확률 calibration, prediction interval을 연결해야 한다.

본 시스템은 투자 자문이 아니다.
