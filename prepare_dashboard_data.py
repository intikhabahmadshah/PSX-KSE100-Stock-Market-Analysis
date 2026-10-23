import os
import json
import pandas as pd
import numpy as np

dataset_path = 'pak_stock (1).csv' if os.path.exists('pak_stock (1).csv') else r'C:\Users\intik\Documents\PSEB\Pakistan Stock Exchange_DataAnalysis\pak_stock (1).csv'
df = pd.read_csv(dataset_path)

df_cleaned = df.drop_duplicates(subset=['symbol', 'date'], keep='first').copy()
if 'Unnamed: 0' in df_cleaned.columns:
    df_cleaned.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
df_cleaned.columns = df_cleaned.columns.str.strip().str.lower().str.replace(' ', '_')
df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])

df_cleaned['open'] = np.where(df_cleaned['open'] == 0, df_cleaned['close'], df_cleaned['open'])
df_cleaned['high'] = np.where(df_cleaned['high'] == 0, np.maximum(df_cleaned['open'], df_cleaned['close']), df_cleaned['high'])
df_cleaned['low'] = np.where(df_cleaned['low'] == 0, np.minimum(df_cleaned['open'], df_cleaned['close']), df_cleaned['low'])
df_cleaned['high'] = np.maximum(df_cleaned['high'], np.maximum(df_cleaned['open'], df_cleaned['close']))
df_cleaned['low'] = np.minimum(df_cleaned['low'], np.minimum(df_cleaned['open'], df_cleaned['close']))

df_cleaned['symbol'] = df_cleaned['symbol'].astype(str)
df_cleaned['month'] = df_cleaned['month'].astype(str)
df_cleaned['year'] = df_cleaned['year'].astype(int)

df_cleaned.sort_values(by=['symbol', 'date'], inplace=True)
df_cleaned.reset_index(drop=True, inplace=True)

df_cleaned['daily_return'] = df_cleaned.groupby('symbol')['close'].pct_change() * 100
df_cleaned['intraday_volatility'] = ((df_cleaned['high'] - df_cleaned['low']) / df_cleaned['open']) * 100

sector_map = {
    'OGDC': 'Oil & Gas', 'PPL': 'Oil & Gas', 'PSO': 'Oil & Gas', 'MARI': 'Oil & Gas', 'POL': 'Oil & Gas',
    'ENGRO': 'Fertilizer', 'EFERT': 'Fertilizer', 'FFC': 'Fertilizer', 'FATIMA': 'Fertilizer',
    'LUCK': 'Cement', 'DGKC': 'Cement', 'MLCF': 'Cement', 'FCCL': 'Cement',
    'HUBC': 'Power & Utilities', 'KEL': 'Power & Utilities', 'KAPCO': 'Power & Utilities',
    'SYS': 'Technology', 'TRG': 'Technology', 'PTC': 'Telecom',
    'MCB': 'Banking', 'HBL': 'Banking', 'UBL': 'Banking', 'MEBL': 'Banking', 'BAFL': 'Banking', 'FABL': 'Banking', 'AKBL': 'Banking', 'NBP': 'Banking', 'SCBPL': 'Banking',
    'UPFL': 'Consumer / FMCG', 'NESTLE': 'Consumer / FMCG', 'COLG': 'Consumer / FMCG', 'RMPL': 'Consumer / FMCG'
}
df_cleaned['sector'] = df_cleaned['symbol'].map(sector_map).fillna('Other Industrials')

symbol_stats = []
symbols = sorted(df_cleaned['symbol'].unique())
stock_series = {}

for sym in symbols:
    sub = df_cleaned[df_cleaned['symbol'] == sym].sort_values(by='date')
    latest = sub.iloc[-1]
    first = sub.iloc[0]
    total_vol = int(sub['volume'].sum())
    avg_vol = float(sub['volume'].mean())
    curr_price = float(latest['close'])
    first_price = float(first['close'])
    pct_change = float(((curr_price - first_price) / first_price) * 100)
    high_52w = float(sub.tail(252)['high'].max())
    low_52w = float(sub.tail(252)['low'].min())
    sector = latest['sector']
    
    symbol_stats.append({
        'symbol': sym,
        'sector': sector,
        'current_price': round(curr_price, 2),
        'pct_change': round(pct_change, 2),
        'high_52w': round(high_52w, 2),
        'low_52w': round(low_52w, 2),
        'total_volume': total_vol,
        'avg_volume': round(avg_vol, 0),
        'sessions': len(sub),
        'latest_date': str(latest['date'].date())
    })
    
    sub_sample = sub.tail(220)
    stock_series[sym] = {
        'dates': [str(d.date()) for d in sub_sample['date']],
        'open': [round(v, 2) for v in sub_sample['open']],
        'high': [round(v, 2) for v in sub_sample['high']],
        'low': [round(v, 2) for v in sub_sample['low']],
        'close': [round(v, 2) for v in sub_sample['close']],
        'volume': [int(v) for v in sub_sample['volume']]
    }

total_market_vol = float(df_cleaned['volume'].sum())
sector_stats = df_cleaned.groupby('sector').agg(
    total_volume=('volume', 'sum'),
    symbols_count=('symbol', 'nunique'),
    avg_price=('close', 'mean')
).reset_index()

sector_data = []
for _, row in sector_stats.iterrows():
    vol = int(row['total_volume'])
    share = (vol / total_market_vol) * 100
    sec_syms = df_cleaned[df_cleaned['sector'] == row['sector']]['symbol'].unique().tolist()
    sector_data.append({
        'sector': row['sector'],
        'total_volume': vol,
        'volume_billions': round(vol * 1e-9, 2),
        'volume_share_pct': round(share, 1),
        'symbols_count': int(row['symbols_count']),
        'avg_price': round(float(row['avg_price']), 2),
        'leaders': ', '.join(sec_syms[:3])
    })

month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
seasonality_notes = {
    'Jan': 'New Fiscal Year Portfolio Rebalancing & Inflow',
    'Feb': 'Q4 / Annual Corporate Earnings Announcement Season',
    'Mar': 'Quarterly Settlement & Pre-Ramadan Positioning',
    'Apr': 'Ramadan Trading Hours Shortened Sessions',
    'May': 'Federal Budget Positioning & Liquidity Reallocation',
    'Jun': 'Federal Budget Approval & Corporate Fiscal Year-End',
    'Jul': 'New Budget Fiscal Execution & Monetary Policy Review',
    'Aug': 'Corporate Half-Yearly Results & Dividend Ex-Dates',
    'Sep': 'Q3 Window-Dressing & Mutual Fund Reallocation',
    'Oct': 'Nine-Month Corporate Financial Disclosures',
    'Nov': 'Pre-Year-End Institutional Accumulation',
    'Dec': 'Annual Closing, Tax-Loss Selling & Window-Dressing'
}

monthly_stats = []
for m in month_order:
    sub = df_cleaned[df_cleaned['month'] == m]
    m_vol = float(sub['volume'].sum())
    monthly_stats.append({
        'month': m,
        'sessions': len(sub),
        'volume_billions': round(m_vol * 1e-9, 2),
        'avg_session_vol_millions': round((m_vol / len(sub)) * 1e-6, 2),
        'seasonality_driver': seasonality_notes.get(m, 'Regular Clearing Cycle')
    })

close_series = df_cleaned['close']
q1 = float(close_series.quantile(0.25))
q3 = float(close_series.quantile(0.75))
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
lower_bound = max(0, q1 - 1.5 * iqr)
outlier_count = int(((close_series < lower_bound) | (close_series > upper_bound)).sum())

distribution_stats = {
    'raw_skewness': round(float(close_series.skew()), 2),
    'raw_kurtosis': round(float(close_series.kurtosis()), 2),
    'log_skewness': round(float(np.log10(close_series).skew()), 2),
    'log_kurtosis': round(float(np.log10(close_series).kurtosis()), 2),
    'mean_price': round(float(close_series.mean()), 2),
    'median_price': round(float(close_series.median()), 2),
    'min_price': round(float(close_series.min()), 2),
    'max_price': round(float(close_series.max()), 2),
    'q1_25pct': round(q1, 2),
    'q3_75pct': round(q3, 2),
    'iqr': round(iqr, 2),
    'upper_bound': round(upper_bound, 2),
    'total_outliers': outlier_count,
    'outlier_pct': round((outlier_count / len(df_cleaned)) * 100, 2)
}

high_outliers_list = [
    {'symbol': 'UPFL', 'name': 'Unilever Pakistan Foods', 'sector': 'Consumer / FMCG', 'max_price': 34139.55, 'min_price': 19000.0, 'median_price': 23500.0, 'type': 'Authentic Blue-Chip (Low Float, Zero Dilution)'},
    {'symbol': 'RMPL', 'name': 'Rafhan Maize Products', 'sector': 'Consumer / FMCG', 'max_price': 12000.0, 'min_price': 7500.0, 'median_price': 8950.0, 'type': 'High Retained Earnings FMCG Titan'},
    {'symbol': 'NESTLE', 'name': 'Nestle Pakistan Limited', 'sector': 'Consumer / FMCG', 'max_price': 9568.15, 'min_price': 5100.0, 'median_price': 6700.0, 'type': 'Multinational Consumer Staple'},
    {'symbol': 'MARI', 'name': 'Mari Petroleum Company', 'sector': 'Oil & Gas Exploration', 'max_price': 3669.06, 'min_price': 1300.0, 'median_price': 1680.0, 'type': 'Strategic Upstream Energy Asset'},
    {'symbol': 'COLG', 'name': 'Colgate-Palmolive Pakistan', 'sector': 'Consumer / FMCG', 'max_price': 3200.0, 'min_price': 1050.0, 'median_price': 1420.0, 'type': 'High Margin Institutional Counter'},
    {'symbol': 'INDU', 'name': 'Indus Motor Company', 'sector': 'Automobile Assembler', 'max_price': 2317.98, 'min_price': 800.0, 'median_price': 1250.0, 'type': 'Top Tier Auto Manufacturer'},
    {'symbol': 'KEL', 'name': 'K-Electric Limited (Penny Benchmark)', 'sector': 'Power & Utilities', 'max_price': 6.20, 'min_price': 1.57, 'median_price': 2.75, 'type': 'Mega-Volume Retail Penny Stock'}
]

trend_symbols = ['OGDC', 'SYS', 'HUBC', 'LUCK', 'EFERT', 'MCB']
trend_sub = df_cleaned[df_cleaned['symbol'].isin(trend_symbols)].copy()
trend_pivot = trend_sub.pivot(index='date', columns='symbol', values='close').ffill()
rebased_trend = (trend_pivot / trend_pivot.iloc[0]) * 100
rebased_sample = rebased_trend.resample('W').last().dropna()

rebased_data = {
    'dates': [str(d.date()) for d in rebased_sample.index],
    'series': {sym: [round(float(v), 2) for v in rebased_sample[sym]] for sym in trend_symbols}
}

market_vol_weekly = df_cleaned.groupby(pd.Grouper(key='date', freq='W'))['volume'].sum().reindex(rebased_sample.index).fillna(0)
rebased_data['weekly_volume_millions'] = [round(float(v) * 1e-6, 2) for v in market_vol_weekly]

rebased_table = []
for sym in trend_symbols:
    base_p = float(trend_pivot[sym].iloc[0])
    end_p = float(trend_pivot[sym].iloc[-1])
    cum_ret = ((end_p - base_p) / base_p) * 100
    peak_val = float(rebased_trend[sym].max())
    sector = symbol_stats[next(i for i, s in enumerate(symbol_stats) if s['symbol'] == sym)]['sector']
    rebased_table.append({
        'symbol': sym,
        'sector': sector,
        'base_price_2021': round(base_p, 2),
        'terminal_price_2025': round(end_p, 2),
        'cumulative_return_pct': round(cum_ret, 2),
        'peak_rebased_index': round(peak_val, 2)
    })

numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'daily_return', 'intraday_volatility']
corr = df_cleaned[numeric_cols].corr()
corr_data = {
    'columns': numeric_cols,
    'labels': ['Open', 'High', 'Low', 'Close', 'Volume', 'Return %', 'Volatility %'],
    'matrix': [[round(float(val), 3) for val in row] for row in corr.values]
}

dashboard_payload = {
    'metadata': {
        'market': 'Pakistan Stock Exchange (PSX)',
        'index': 'KSE-100 Constituents Benchmark',
        'date_range': [str(df_cleaned['date'].min().date()), str(df_cleaned['date'].max().date())],
        'total_records': len(df_cleaned),
        'total_symbols': df_cleaned['symbol'].nunique(),
        'total_volume_billions': round(float(df_cleaned['volume'].sum()) * 1e-9, 2),
        'mean_price': round(float(df_cleaned['close'].mean()), 2),
        'median_price': round(float(df_cleaned['close'].median()), 2)
    },
    'distribution_stats': distribution_stats,
    'monthly_stats': monthly_stats,
    'top_outliers': high_outliers_list,
    'rebased_table': rebased_table,
    'symbols': symbol_stats,
    'sectors': sector_data,
    'rebased': rebased_data,
    'correlations': corr_data,
    'stock_series': stock_series
}

with open('psx_dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_payload, f)

print(f"Enriched psx_dashboard_data.json created successfully! Size: {os.path.getsize('psx_dashboard_data.json') / 1024:.1f} KB")
