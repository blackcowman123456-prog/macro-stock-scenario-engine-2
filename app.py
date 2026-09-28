import os
import streamlit as st
import pandas as pd
from common.live_data import get_market_snapshot
from common.engine import scenario_from_inputs

st.set_page_config(page_title="Macro → Stock Scenario Engine", page_icon="📈", layout="wide")

st.title("📈 Macro → Stock Scenario Engine")
st.caption("한국주식과 미국주식을 독립된 데이터·모델 파이프라인으로 분석")

st.warning(
    "면책: 본 서비스는 투자 자문이 아닌 분석/교육용 도구입니다. "
    "예측 확률과 수익률 구간은 미래 결과를 보장하지 않습니다."
)

market = st.sidebar.radio("시장", ["한국주식", "미국주식"])
horizon = st.sidebar.selectbox("예측 기간", ["3개월", "6개월", "12개월"])

st.sidebar.markdown("### 데이터")
live = st.sidebar.checkbox("현재 시장가격 자동 조회", value=True)

st.sidebar.markdown("### 시나리오 입력")
rate = st.sidebar.slider("정책금리 변화 (bp)", -200, 200, 0, 10)
infl = st.sidebar.slider("인플레이션 변화 (%p)", -3.0, 3.0, 0.0, 0.1)
growth = st.sidebar.slider("성장률 변화 (%p)", -4.0, 4.0, 0.0, 0.1)
momentum = st.sidebar.slider("시장 모멘텀 (z)", -3.0, 3.0, 0.0, 0.1)

snapshot = get_market_snapshot(market) if live else pd.DataFrame()

if not snapshot.empty:
    st.subheader("현재 시장 데이터")
    st.dataframe(snapshot, use_container_width=True, hide_index=True)
else:
    st.info("현재 시장가격 자동 조회 결과가 없습니다. 시뮬레이션 입력값으로 분석합니다.")

result = scenario_from_inputs(
    market, horizon, rate, infl, growth, momentum, snapshot
)

c1,c2,c3,c4 = st.columns(4)
c1.metric("현재 Regime", result["regime"])
c2.metric("가장 높은 시나리오", result["base"])
c3.metric("모델 확률 집중도", f'{result["confidence"]:.0%}')
c4.metric("불확실성", result["uncertainty"])

st.subheader("경제 시나리오")
st.bar_chart(pd.Series(result["probabilities"], name="확률"))

st.subheader("시나리오 정의")
st.dataframe(pd.DataFrame(result["scenario_detail"]), use_container_width=True, hide_index=True)

st.subheader("시장별 주요 종목/ETF 예시")
st.dataframe(pd.DataFrame(result["stocks"]), use_container_width=True, hide_index=True)

st.subheader("모델이 확인해야 할 리스크")
for r in result["risks"]:
    st.write("•", r)

with st.expander("실전 모델의 현재 구현 상태"):
    st.markdown("""
- 가격/지수: 공개 데이터 자동 조회 계층
- 한국 매크로: ECOS/KOSIS API 연결 인터페이스
- 미국 매크로: FRED API 연결 인터페이스
- Regime: Markov/VAR/XGBoost를 연결할 수 있는 구조
- Stock Impact: Factor + Event Study 구조
- Backtest: Walk-forward 구조로 확장 예정
- Point-in-Time / vintage: 실전 학습 데이터에는 필수
""")
