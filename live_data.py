import pandas as pd
import yfinance as yf

KOREA = {
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "Samsung Electronics": "005930.KS",
    "SK Hynix": "000660.KS",
    "Hyundai Motor": "005380.KS",
}
USA = {
    "S&P 500": "^GSPC",
    "Nasdaq 100": "^NDX",
    "VIX": "^VIX",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "JPMorgan": "JPM",
}

def get_market_snapshot(market):
    tickers = KOREA if market == "한국주식" else USA
    rows = []
    for name, ticker in tickers.items():
        try:
            h = yf.Ticker(ticker).history(period="5d", auto_adjust=False)
            if h.empty:
                continue
            last = float(h["Close"].iloc[-1])
            prev = float(h["Close"].iloc[-2]) if len(h) > 1 else last
            rows.append({
                "구분": name,
                "Ticker": ticker,
                "최근값": round(last, 4),
                "일간변화율": round((last/prev-1)*100, 2)
            })
        except Exception:
            continue
    return pd.DataFrame(rows)
