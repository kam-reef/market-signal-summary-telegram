# Market Analysis Workflow

A GitHub Actions workflow that analyzes stock market data and generates automated investment reports with AI commentary.

## Features

✨ **Core Capabilities:**
- 📊 Fetch real-time stock data via Yahoo Finance API
- 📈 Calculate simple moving averages (weekly, monthly, quarterly)
- 📰 Aggregate relevant news from NewsAPI
- 🤖 Generate AI commentary using OpenRouter (free tier)
- 📝 Log all results to CSV for historical tracking
- 🤖 Post formatted reports to Telegram
- ⏰ Triggered on-demand via GitHub Actions UI

## Setup Instructions

### 1. Prerequisites

- GitHub repository with Actions enabled
- Python 3.11+
- API Keys (free tiers available for all):
  - NewsAPI: https://newsapi.org (free tier: 100 requests/day)
  - OpenRouter: https://openrouter.ai (free tier available)
  - Telegram Bot Token: https://t.me/BotFather
  - Yahoo Finance: Uses free endpoint (no key required)

### 2. Configure GitHub Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
YAHOO_FINANCE_API_KEY      (optional)
NEWS_API_KEY               (required)
OPENROUTER_API_KEY         (required)
TELEGRAM_BOT_TOKEN         (required)
TELEGRAM_CHAT_ID           (optional - can be provided at runtime)
```

**How to get each key:**

**NewsAPI:**
1. Go to https://newsapi.org
2. Sign up for free account
3. Copy API key from dashboard

**OpenRouter:**
1. Go to https://openrouter.ai
2. Sign up with GitHub or email
3. Go to https://openrouter.ai/keys
4. Copy your API key (free tier available)

**Telegram:**
1. Open Telegram and search for @BotFather
2. Create new bot with `/newbot`
3. Copy the bot token
4. Chat with your new bot (send any message)
5. Go to https://t.me/userinfobot to get your Chat ID

### 3. Directory Structure

```
.
├── .github/workflows/
│   └── market-analysis.yml      # GitHub Actions workflow
├── src/
│   ├── main.py                  # Orchestrator script
│   ├── ticker_fetcher.py        # Yahoo Finance data fetching
│   ├── sma_calculator.py        # SMA calculations
│   ├── news_fetcher.py          # NewsAPI integration
│   ├── ai_commentary.py         # OpenRouter AI integration
│   ├── csv_logger.py            # CSV logging
│   └── telegram_reporter.py     # Telegram integration
├── data/
│   └── market_analysis.csv      # Historical analysis logs
├── logs/
│   └── market_analysis.log      # Detailed execution logs
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Usage

### Run the Workflow

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **Market Analysis Report** workflow
4. Click **Run workflow**
5. Enter stock ticker (e.g., `AAPL`, `MSFT`, `GOOGL`)
6. Optionally specify Telegram chat ID
7. Click **Run workflow**

### Example Usage

**Input:**
- Ticker: `AAPL`
- Telegram Chat ID: `123456789` (optional)

**Output:**
- Real-time price data
- SMA comparison analysis
- Latest news articles
- AI-generated investment commentary
- CSV log entry
- Telegram message (if configured)

## Report Format

The report includes:

```
📈 Market Analysis Report 📈

Ticker: AAPL

💰 Price Data
• Current: $153.50
• Closing: $152.80
• P/E Ratio: 28.5

📊 Simple Moving Averages (SMA)
• Weekly (5d): $151.20 (+1.52%)
• Monthly (21d): $150.50 (+1.99%)
• Quarterly (63d): $148.00 (+3.65%)

📰 Latest News
1. [Apple Reports Strong Q4 Earnings](https://...)
   Source: Financial Times
2. [Analyst Upgrades Apple to Buy](https://...)
   Source: Bloomberg

🤖 AI Analysis
Stock is trading above all major moving averages, showing strong 
uptrend momentum. Positive news sentiment supports bullish outlook. 
Recommendation: HOLD/BUY on dips.
```

## CSV Log Format

Results are logged to `data/market_analysis.csv`:

| Timestamp | Ticker | Current_Price | SMA_Weekly | vs_Weekly_Percent | AI_Commentary | Status |
|-----------|--------|---------------|------------|-------------------|---------------|--------|
| 2024-01-15T10:30:00 | AAPL | 153.50 | 151.20 | 1.52 | Stock is in uptrend... | Success |

## API Rate Limits

- **NewsAPI**: 100 requests/day (free tier)
- **OpenRouter**: Rate limited per free tier (check docs)
- **Yahoo Finance**: No rate limit on free endpoint
- **Telegram**: ~30 messages/second

## Customization

### Change Analysis Period

Edit `src/sma_calculator.py`:
```python
# Line ~65
'1y'  # Change to: '6mo', '3mo', '2y', etc.
```

### Modify Report Format

Edit `src/telegram_reporter.py` → `format_report()` method to customize the message layout.

### Change AI Model

Edit `src/ai_commentary.py`:
```python
self.model = 'mistralai/mistral-7b-instruct:free'  # Change to other free models
```

Available free models on OpenRouter: https://openrouter.ai/docs#free-models

## Troubleshooting

### "API key not found"
- Check GitHub Secrets configuration
- Ensure secrets are named exactly as shown above

### "News fetch failed"
- Check if NewsAPI key is valid
- Verify rate limit not exceeded
- Check internet connectivity in GitHub Actions

### "Telegram message not sent"
- Verify bot token is correct
- Ensure you've messaged the bot first
- Check Chat ID format (should be numeric)

### "Empty analysis results"
- Verify ticker symbol is valid (e.g., `AAPL` not `Apple`)
- Check API keys are active
- Review workflow logs for detailed errors

## Performance

- **Typical execution time**: 30-60 seconds
- **CSV log**: ~5KB per entry
- **Workflow runs**: Limited by GitHub Actions free tier (~2000 minutes/month)

## Cost Analysis

✅ **Completely Free:**
- GitHub Actions (2000 min/month free)
- NewsAPI (100 req/day free)
- OpenRouter (free tier models)
- Telegram Bot API
- Yahoo Finance (free endpoint)

**Estimated monthly cost**: $0 (using all free tiers)

## Advanced Usage

### Run Multiple Tickers

Create a workflow that loops through tickers:

```yaml
strategy:
  matrix:
    ticker: [AAPL, MSFT, GOOGL, TSLA, AMZN]
```

### Schedule Reports

Replace `on: workflow_dispatch` with:

```yaml
on:
  schedule:
    - cron: '0 9 * * MON-FRI'  # 9 AM weekdays
```

### Post to Multiple Chats

Set up different workflows for different chat IDs or modify the script to loop through a list.

## Support

For issues, questions, or feature requests:
1. Check the Troubleshooting section
2. Review workflow logs in GitHub Actions
3. Check API documentation:
   - NewsAPI: https://newsapi.org/docs
   - OpenRouter: https://openrouter.ai/docs
   - Telegram Bot API: https://core.telegram.org/bots/api

## Documentation

- **QUICKSTART.md** - 5-minute quick start guide
- **CONFIGURATION.md** - Advanced configuration options

## License

MIT License - Feel free to use and modify!

## Disclaimer

This tool is for informational purposes only. It does not provide financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.
