# Quick Start Guide

Complete these steps to get your market analysis workflow up and running.

## 5-Minute Setup

### Step 1: Get API Keys (5 minutes)

**NewsAPI Key:**
1. Visit https://newsapi.org
2. Click "Get API Key"
3. Sign up (free tier: 100 requests/day)
4. Copy your API key

**OpenRouter Key:**
1. Visit https://openrouter.ai
2. Sign in with GitHub
3. Go to https://openrouter.ai/keys
4. Copy your API key (free tier available)

**Telegram Bot:**
1. Open Telegram, search: `@BotFather`
2. Send: `/newbot`
3. Follow prompts to create bot
4. Copy the bot token provided
5. Search for your new bot name and send any message
6. Go to https://t.me/userinfobot
7. Send: `/start`
8. Copy your Chat ID

### Step 2: Add Secrets to GitHub (2 minutes)

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:

| Name | Value |
|------|-------|
| `NEWS_API_KEY` | Your NewsAPI key |
| `OPENROUTER_API_KEY` | Your OpenRouter key |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |

### Step 3: Run Your First Report (1 minute)

1. Go to your repository
2. Click **Actions** tab
3. Select **Market Analysis Report**
4. Click **Run workflow** (top right)
5. Enter ticker: `AAPL`
6. Click **Run workflow**
7. Watch the workflow execute in real-time
8. Check your Telegram chat for the report!

## Workflow Features Explained

### On-Demand Triggering
Manually trigger reports anytime via the GitHub Actions UI.

### Stock Price Analysis
- Current market price
- Previous closing price
- 52-week high/low
- Market cap & P/E ratio

### Moving Averages
Compares current price against:
- **Weekly SMA**: Last 5 trading days
- **Monthly SMA**: Last 21 trading days  
- **Quarterly SMA**: Last 63 trading days

### News Integration
- Fetches up to 3 latest articles
- Includes source attribution
- Clickable links in Telegram

### AI Commentary
- Uses OpenRouter free models
- Analyzes price + news sentiment
- Generates actionable insights
- Signals: Bullish/Neutral/Bearish

### Data Logging
- CSV file with complete analysis history
- Auto-committed to repository
- Accessible for further analysis

### Telegram Reporting
- Formatted markdown messages
- Price/SMA comparison chart
- Linked news articles
- AI analysis & recommendation

## Example Report

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
1. [Apple Reports Strong Q4 Earnings](link)
   Source: Financial Times
2. [Analyst Upgrades Apple](link)
   Source: Bloomberg

🤖 AI Analysis
Stock is trading above all major moving averages with 
positive momentum. Recent news sentiment is bullish.
Recommendation: HOLD/BUY on dips.
```

## Customization Examples

### Add More Stocks
Create workflow matrix in `.github/workflows/market-analysis.yml`:
```yaml
strategy:
  matrix:
    ticker: [AAPL, MSFT, GOOGL, TSLA]
```

### Schedule Automatic Reports
Change workflow trigger:
```yaml
on:
  schedule:
    - cron: '0 9 * * MON-FRI'  # Daily at 9 AM
```

### Change Analysis Period
Edit `src/sma_calculator.py` line 65:
```python
self._fetch_historical_data('6mo')  # Changed from '1y'
```

### Use Different AI Model
Edit `src/ai_commentary.py` to use different free model:
```python
'mistralai/mistral-7b-instruct:free'  # Default
'meta-llama/llama-2-7b-chat:free'     # Alternative
'nousresearch/nous-hermes-2-7b:free'  # Another option
```

See https://openrouter.ai/docs#free-models for all options.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Verify secrets are in Settings → Secrets with exact names |
| "Workflow fails" | Check workflow logs for detailed error messages |
| "No Telegram message" | Ensure you messaged the bot first, check Chat ID |
| "Invalid ticker" | Use valid symbols like AAPL, not "Apple" |

## Next Steps

1. ✅ Set up API keys (you did this!)
2. ✅ Add GitHub secrets (you did this!)
3. ✅ Run first report (you did this!)
4. 📝 Monitor CSV logs in `data/market_analysis.csv`
5. 🔧 Customize for your needs
6. 📅 Set up scheduling if desired

## Free Tier Limits

- **GitHub Actions**: 2000 min/month
- **NewsAPI**: 100 requests/day
- **OpenRouter**: Check rate limits
- **Telegram**: Unlimited (recommended <1000/month)

Easily run 20+ analyses daily within free limits!

## Need Help?

1. **Check logs**: Click workflow run → scroll for error details
2. **Verify secrets**: Settings → Secrets - ensure names match exactly
3. **Test APIs**: Run each API independently to verify keys
4. **Review code**: Comments in `src/` explain each module

Happy analyzing! 📊
