import numpy as np

def scenario_from_inputs(market, horizon, rate, infl, growth, momentum, snapshot):
    score = -0.002*rate - 0.35*infl + 0.45*growth + 0.30*momentum

    if score > 0.65:
        regime = "Risk-on / 경기 개선"
        p = {"Base": .40, "Bull": .48, "Bear": .12}
    elif score < -0.65:
        regime = "Risk-off / 경기 둔화"
        p = {"Base": .42, "Bull": .12, "Bear": .46}
    else:
        regime = "중립 / 전환 국면"
        p = {"Base": .54, "Bull": .27, "Bear": .19}

    base = max(p, key=p.get)
    conf = p[base]
    uncertainty = "높음" if conf < .50 else ("중간" if conf < .65 else "낮음")

    if market == "한국주식":
        stocks = [
            ("005930.KS","삼성전자","상승",.61,"+3% ~ +16%"),
            ("000660.KS","SK하이닉스","상승",.64,"+5% ~ +20%"),
            ("005380.KS","현대차","중립~상승",.55,"+1% ~ +12%"),
        ]
    else:
        stocks = [
            ("MSFT","Microsoft","상승",.60,"+3% ~ +15%"),
            ("NVDA","NVIDIA","상승",.63,"+4% ~ +21%"),
            ("JPM","JPMorgan","중립~상승",.54,"+1% ~ +12%"),
        ]

    return {
        "regime": regime, "base": base, "confidence": conf,
        "uncertainty": uncertainty, "probabilities": p,
        "scenario_detail": [
            {"시나리오":"Base","확률":f"{p['Base']:.0%}","정의":"현재 추세가 대체로 유지"},
            {"시나리오":"Bull","확률":f"{p['Bull']:.0%}","정의":"성장 개선과 위험선호 강화"},
            {"시나리오":"Bear","확률":f"{p['Bear']:.0%}","정의":"성장 둔화와 금융여건 악화"},
        ],
        "stocks": [
            {"Ticker":t,"종목":n,"방향":d,"상승확률(프로토타입)":f"{u:.0%}","예상범위(프로토타입)":b}
            for t,n,d,u,b in stocks
        ],
        "risks": [
            "현재 프로토타입의 시나리오 확률은 학습된 실전 확률이 아닙니다.",
            "공식 매크로 데이터는 release date/vintage를 보존해야 look-ahead bias를 막을 수 있습니다.",
            "실전 수익률 구간은 quantile regression/conformal prediction 등으로 산출해야 합니다.",
            "백테스트에는 거래비용·슬리피지·생존편향·공표시차를 포함해야 합니다.",
        ],
    }
