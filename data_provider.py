import os
class USMacroProvider:
    """
    FRED 공식 매크로 데이터 연결 자리.
    FRED_API_KEY를 환경변수 또는 Streamlit Secrets에 저장한다.
    실전 모델에서는 vintage/realtime date를 보존한다.
    """
    def __init__(self):
        self.fred_key = os.getenv("FRED_API_KEY")

    def available(self):
        return bool(self.fred_key)
