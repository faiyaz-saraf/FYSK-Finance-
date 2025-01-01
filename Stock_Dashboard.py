import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
 

# Configure page settings
st.set_page_config(layout="wide")

# Apply dark theme
st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .sidebar .sidebar-content {
            background-color: #262730;
        }
        .stTextInput>div>div>input {
            background-color: #262730;
            color: #FAFAFA;
        }
        .stDateInput>div>div>input {
            background-color: #262730;
            color: #FAFAFA;
        }
    </style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:

    st.markdown("<h1 style='color: #00b3ff;'>Ticker</h1>", unsafe_allow_html=True)

    ticker = st.text_input('Enter Stock Ticker:', value='AAPL').upper()
    start_date = st.date_input('Start Date:', datetime.now() - timedelta(days=365))
    end_date = st.date_input('End Date:', datetime.now())
    
    if start_date > end_date:
        st.error('Error: End date must be after start date')
        st.stop()

with st.sidebar:
    st.markdown("""

    _______________

    """)
    st.markdown("<h1 style='color: #00b3ff;'>About</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### About Me 👨‍💻
    Hi! I'm Faiyaz. My passion lies at the intersection of investing, programming, and finance. This combination of interests led me to create FYSK Finance, where I could blend my technical skills with my enthusiasm for financial markets.
    
    ### About This Project 🚀
    This Stock Market Dashboard is built using Python and Streamlit. It features real-time stock data visualization, technical analysis, and latest market news. Feel free to mess around with its features!
    
    ### Technologies Used 🛠️
    - Python
    - Streamlit
    - yfinance for stock data
    - Plotly for interactive charts
    - Yahoo Finance API for news
    
    ### Contact 🔗
    - [LinkedIn](https://www.linkedin.com/in/faiyaz--s/)
    - <a href="mailto:faiyaz.saraf@gmail.com">faiyaz.saraf@gmail.com</a>
    
    ### Credits ⭐
    Data provided by Yahoo Finance API
    """,  unsafe_allow_html=True)

# Initialize stock data
@st.cache_data(ttl=3600)
def load_stock_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        info = stock.info
        news = stock.news
        return df, info, news
    except Exception as e:
        st.error(f'Error loading data: {e}')
        return None, None, None

df, info, news = load_stock_data(ticker, start_date, end_date)

st.title('FYSK Finance - Stock Dashboard 📈')
if df is not None:
    # Main content tab
    tab1, tab2, tab3, tab4 = st.tabs(['Chart Analysis 📊', 'Company News 📰', 'Financials 💰', 'Technical Indicators ⚡'])
    
    # Tab 1: Chart Analysis
    with tab1:
        st.subheader(f'{ticker} Chart')

        current_price = df['Close'].iloc[-1]  # Gets the most recent closing price
        tab1.markdown(f"<h3 style='color: #FFFFFF;'>End Date Price: ${current_price:.2f}</h3>", unsafe_allow_html=True)


        # Calculate current price and daily change
        current_price = df['Close'].iloc[-1]
        previous_price = df['Close'].iloc[-2]
        price_change = current_price - previous_price
        price_change_percentage = (price_change / previous_price) * 100

        # Determine color based on price change (green for positive, red for negative)
        color = "#00FF00" if price_change >= 0 else "#FF0000"
        change_symbol = "+" if price_change >= 0 else ""

        # Display current price and change
        tab1.markdown(f"""
        <h4 style='color: {color};'>Daily Change: {change_symbol}${price_change:.2f} ({change_symbol}{price_change_percentage:.2f}%)</h4>
        """, unsafe_allow_html=True)
        
        # Chart type selector
        chart_type = st.selectbox('Select Chart Type:', 
                                ['Line','Candlestick'])
        
        fig = go.Figure()
        
        if chart_type == 'Line':
            
            fig = go.Figure(data=[go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='#00b3ff')
            )])

        elif chart_type == 'Candlestick':
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='OHLC'
            ))
 
        fig.update_layout(
            template='plotly_dark',
            xaxis_rangeslider_visible=True,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

        current_price = df['Close'].iloc[-1]  # Gets the most recent closing price
        
        # Volume chart
        volume_fig = go.Figure()
        volume_fig.add_trace(go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume'
        ))
        volume_fig.update_layout(
            template='plotly_dark',
            title='Trading Volume',
            height=300
        )
        st.plotly_chart(volume_fig, use_container_width=True)

        

    # Tab 2: Company News
    with tab2:
        st.subheader('Latest News')
        for article in news[:10]:  # Display last 10 news items
            
             
            st.markdown(f"### {article['content']['title']}")
            st.write(f"**Source:** {article['content']['provider']['displayName']}")
            st.write(f"**Published:** {article['content']['pubDate']}")
            st.write(article['content']['summary'])
            if article['content'].get('clickThroughUrl'):
                url = article['content']['clickThroughUrl']['url']
            else:
                url = article['content']['canonicalUrl']['url']
            st.markdown(f"[Read more]({url})")
            st.markdown("---")  # Add a divider between articles

    # Tab 3: Financials
    with tab3:
        st.subheader('Financial Information')
        
        # Company profile
        col1, col2 = st.columns(2)
        with col1:
            st.write('**Company Profile**')
            st.write(f"Sector: {info.get('sector', 'N/A')}")
            st.write(f"Industry: {info.get('industry', 'N/A')}")
            st.write(f"Market Cap: ${info.get('marketCap', 0):,.2f}")
            st.write(f"Beta: {info.get('beta', 'N/A')}")
            
        with col2:
            st.write('**Key Statistics**')
            st.write(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
            st.write(f"Forward P/E: {info.get('forwardPE', 'N/A')}")
            st.write(f"Dividend Yield: {info.get('dividendYield', 0):.2%}")
            st.write(f"52 Week High: ${info.get('fiftyTwoWeekHigh', 0):,.2f}")
            st.write(f"52 Week Low: ${info.get('fiftyTwoWeekLow', 0):,.2f}")

    # Tab 4: Technical Indicators
    with tab4:
        st.subheader('Technical Indicators')
        
        # Calculate moving averages
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()
        
        # Technical analysis chart
        tech_fig = go.Figure()
        
        # Price
        tech_fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Close'],
            name='Price',
            line=dict(color='white')
        ))
        
        # Moving averages
        tech_fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MA20'],
            name='20 Day MA',
            line=dict(color='yellow')
        ))
        
        tech_fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MA50'],
            name='50 Day MA',
            line=dict(color='orange')
        ))
        
        tech_fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MA200'],
            name='200 Day MA',
            line=dict(color='red')
        ))
        
        tech_fig.update_layout(
            template='plotly_dark',
            title='Technical Analysis',
            height=600,
            xaxis_rangeslider_visible=False
        )
        
        st.plotly_chart(tech_fig, use_container_width=True)
        
        # RSI calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # RSI chart
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(
            x=df.index,
            y=df['RSI'],
            name='RSI'
        ))
        
        # Add RSI reference lines
        rsi_fig.add_hline(y=70, line_color='red', line_dash='dash')
        rsi_fig.add_hline(y=30, line_color='green', line_dash='dash')
        
        rsi_fig.update_layout(
            template='plotly_dark',
            title='Relative Strength Index (RSI)',
            height=300,
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(rsi_fig, use_container_width=True)

else:
    st.error('Please enter a valid ticker symbol')