import streamlit as st
import matplotlib.pyplot as plt
from stock_data import get_stock_data
from news import get_news
from portfolio import portfolio
from indicators import calculate_rsi
import plotly.graph_objects as go
from advisor import investment_advice
from comparison import compare_stocks
from gemini_ai import analyze_stock, chat_with_ai
from streamlit_searchbox import st_searchbox
from stock_search import search_stocks
import gemini_ai
from compare_ai import compare_ai
from streamlit_option_menu import option_menu
# st.write(gemini_ai.__file__)
st.markdown("""
<h1 style="
font-size:60px;
font-weight:800;
color:#4CAF50;
margin-bottom:0px;
">
 AI Investment Copilot
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
font-size:22px;
color:#B0B0B0;
margin-top:-15px;
">
Analyze • Compare • Invest with AI
</p>
""", unsafe_allow_html=True)

if "info" not in st.session_state:
    st.session_state.info = None

if "history" not in st.session_state:
    st.session_state.history = None
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/4/4e/Pleiades_large.jpg",
        use_container_width=True
    )

    selected_menu = option_menu(
        menu_title="Navigation",
        options=["Dashboard","Portfolio","Comparison"],
        icons=["bar-chart","wallet2","graph-up-arrow"],
        default_index=0,
    )
period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)
st.sidebar.header("Portfolio")

qty = st.sidebar.number_input(
    "Quantity",
    min_value=1,
    value=10
)

buy_price = st.sidebar.number_input(
    "Buy Price",
    min_value=1.0,
    value=3000.0
)
st.sidebar.markdown("---")

st.sidebar.info("""
 AI Investment Copilot

Version 1.0

Made with using
Python + Streamlit
""")
st.markdown("## 🔍 Search Indian Stocks")
selected = st_searchbox(
    search_function=search_stocks,
    placeholder="Search Company or Symbol...",
    label="🔍 Search Stock"
)

symbol = "TCS.NS"

if selected:
    symbol = selected.split("(")[-1].replace(")", "")





if st.button(" Analyze Stock", use_container_width=True):

    st.session_state.info, st.session_state.history = get_stock_data(symbol, period)

    info = st.session_state.info
    history = st.session_state.history
    
    tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "📈 Technical Analysis",
    "🤖 AI Advisor"
])

    st.subheader(info.get("longName", "N/A"))
    

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Current Price",
            f"₹{info.get('currentPrice','N/A')}"
    )

    with col2:
        st.metric(
            "📈 Day High",
            f"₹{info.get('dayHigh','N/A')}"
    )

    with col3:
        st.metric(
            "📉 Day Low",
            f"₹{info.get('dayLow','N/A')}"
    )

    with col4:
        st.metric(
            "🏢 Market Cap",
            info.get("marketCap","N/A")
    )    
    st.subheader(f"Stock Price ({period})")

    history["MA20"] = history["Close"].rolling(20).mean()
    history["MA50"] = history["Close"].rolling(50).mean()

    history = calculate_rsi(history)   



    st.subheader(" Candlestick Chart")

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=history.index,
            open=history["Open"],
            high=history["High"],
            low=history["Low"],
            close=history["Close"],
            name="Candlestick"
    )
)

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["MA20"],
            mode="lines",
            name="MA20"
    )
)

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["MA50"],
            mode="lines",
            name="MA50"
    )
)

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        height=600
)

    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Portfolio")

    data = portfolio(symbol, qty, buy_price)

    st.metric("Current Price", f"₹{data['current_price']}")
    st.metric("Investment", f"₹{data['investment']:.2f}")
    st.metric("Current Value", f"₹{data['current_value']:.2f}")
    st.metric("Profit / Loss", f"₹{data['profit']:.2f}")
    st.metric("Return %", f"{data['percent']:.2f}%")

    
    trend, advice = investment_advice(history)

    st.subheader("RSI Indicator")
    fig_rsi = go.Figure()

# RSI Line
    fig_rsi.add_trace(
        go.Scatter(
            x=history.index,
            y=history["RSI"],
            mode="lines",
            name="RSI",
            line=dict(width=3)
    )
)

# Overbought Line (70)
    fig_rsi.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="Overbought (70)"
)

# Oversold Line (30)
    fig_rsi.add_hline(
        y=30,
        line_dash="dash",
        annotation_text="Oversold (30)"
)

    fig_rsi.update_layout(
        title="RSI Indicator",
        xaxis_title="Date",
        yaxis_title="RSI",
        yaxis=dict(range=[0, 100]),
        height=400,
        hovermode="x unified"
)

    st.plotly_chart(fig_rsi, use_container_width=True)
    current_rsi = history["RSI"].iloc[-1]

    st.metric("Current RSI", f"{current_rsi:.2f}")

    if current_rsi > 70:

        st.error("🔴 Overbought")

    elif current_rsi < 30:
        st.success("🟢 Oversold")

    else:
        st.info("🟡 Neutral")
     
    st.subheader(" AI Investment Advisor")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Market Trend", trend)

    with col2:
        st.metric("Recommendation", advice)

    st.subheader(" Gemini AI Analysis")

    analysis = analyze_stock(
        info.get("longName", symbol),
        info.get("currentPrice", history["Close"].iloc[-1]),
        current_rsi,
        advice
)

    st.write(analysis)

    st.markdown("---")
    st.subheader("🤖 Ask AI About This Stock")

    question = st.chat_input("Ask anything about this stock...")

    if question:
        with st.spinner("Thinking..."):

            answer = chat_with_ai(
                info.get("longName", symbol),
                info.get("currentPrice", history["Close"].iloc[-1]),
                current_rsi,
                advice,
                question
        )

        st.markdown("### 🤖 AI Answer")
        st.write(answer)

st.subheader("📰 Latest News")

news = get_news(symbol)

if news:

    for item in news[:5]:

        content = item.get("content", {})

        title = content.get("title", "No Title")

        provider = content.get("provider") or {}
        source = provider.get("displayName", "Unknown")

        summary = content.get("summary", "No summary available")
        date = content.get("pubDate", "")

        click_url = content.get("clickThroughUrl") or {}
        link = click_url.get("url", "#")
        with st.container():
            st.markdown(f"### 📰 {title}")
            st.caption(f"🏢 {source} | 📅 {date}")
            st.write(summary)

            st.markdown(f"[🔗 Read Full Article]({link})")

            st.divider()

else:
    st.warning("No news found.")


st.subheader("Stock Comparison")

selected2 = st_searchbox(
    search_function=search_stocks,
    placeholder="Search Second Stock...",
    label="Compare With",
    key="compare_stock"
)

stock2 = ""

if selected2:
    stock2 = selected2.split("(")[-1].replace(")", "")


if stock2:

    history1, history2, info1, info2 = compare_stocks(
        symbol,
        stock2,
        period
)

    history1 = calculate_rsi(history1)
    history2 = calculate_rsi(history2)

    st.write("History1:", len(history1))
    st.write("History2:", len(history2))

    st.write(history1.tail())
    st.write(history2.tail())
 
    history1 = calculate_rsi(history1)
    history2 = calculate_rsi(history2)

# NaN RSI rows hata do
    history1 = history1.dropna(subset=["RSI"])
    history2 = history2.dropna(subset=["RSI"])

    if history1.empty or history2.empty:
        st.error("Not enough data to calculate RSI for comparison.")
        st.stop()

    rsi1 = history1["RSI"].iloc[-1]
    rsi2 = history2["RSI"].iloc[-1]

    st.write("Stock 1:", symbol)
    st.write("Stock 2:", stock2)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history1.index,
            y=history1["Close"],
            mode="lines",
            name=symbol,
            line=dict(width=3)
    )
)

    fig.add_trace(
        go.Scatter(
            x=history2.index,
            y=history2["Close"],
            mode="lines",
            name=stock2,
            line=dict(width=3)
    )
)

    fig.update_layout(
        title=" Stock Performance Comparison",
        xaxis_title="Date",
        yaxis_title="Closing Price (₹)",
        template="plotly_dark",
        hovermode="x unified",
        height=550,
        legend=dict(
            orientation="h",
            y=1.05,
            x=0
    )
)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI Stock Comparison")

    comparison = compare_ai(
        info1,
        info2,
        rsi1,
        rsi2
)

    st.write(comparison)
else:
    st.info("Enter second stock symbol for comparison")

