# Configuration Guide

Detailed configuration options for the market analysis workflow.

## Environment Variables

All configuration is done via environment variables or GitHub Secrets.

### Required Secrets

Add these to GitHub Settings → Secrets and variables → Actions:

```env
# News data source (get free key at https://newsapi.org)
NEWS_API_KEY=your_api_key

# AI model provider (sign up at https://openrouter.ai)
OPENROUTER_API_KEY=your_api_key

# Telegram bot (get from https://t.me/BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token
```

### Optional Secrets

```env
# Default Telegram chat (can override at runtime)
TELEGRAM_CHAT_ID=your_chat_id

# Yahoo Finance API (uses free endpoint by default)
YAHOO_FINANCE_API_KEY=your_api_key
```

## Workflow Parameters

When running the workflow, you can customize:

### Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `ticker` | Yes | - | Stock ticker (e.g., AAPL, MSFT) |
| `telegram_chat_id` | No | From secret | Override Telegram chat ID |

### Example: Run with Custom Chat ID

```bash
# Via GitHub Actions UI:
# 1. Actions tab
# 2. Market Analysis Report
# 3. Run workflow
# 4. ticker: TSLA
# 5. telegram_chat_id: 987654321
# 6. Run workflow
```

## Python Configuration

### Ticker Fetcher (src/ticker_fetcher.py)

Uses free Yahoo Finance endpoint:

```python
# No configuration needed for free tier
# Optional: Set YAHOO_FINANCE_API_KEY for premium endpoints
```

Fetches:
- Current price
- Closing price
- 52-week high/low
- Market cap
- P/E ratio

### SMA Calculator (src/sma_calculator.py)

Adjust analysis period:

```python
# Line ~45
def calculate(self) -> Dict[str, Any]:
    hist_data = self._fetch_historical_data('1y')  # Change period here
    
    # Periods: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'
    # Default '1y' = last year (recommended)
```

Adjust moving average windows:

```python
# Lines ~65-76
sma_weekly = close_prices.rolling(window=5).mean()      # 5 trading days
sma_monthly = close_prices.rolling(window=21).mean()    # 21 trading days
sma_quarterly = close_prices.rolling(window=63).mean()  # 63 trading days

# Customize windows:
# window=10    → 2-week SMA
# window=50    → 10-week SMA
# window=200   → 1-year SMA
```

### News Fetcher (src/news_fetcher.py)

Change number of articles:

```python
# In main.py, line ~35
news_articles = news_fetcher.fetch(limit=3)  # Change to desired count

# Note: NewsAPI free tier: 100 requests/day
# Each fetch uses 1 request regardless of limit
```

Configure news query:

```python
# In news_fetcher.py, line ~41
params = {
    'q': self.ticker,           # Search term
    'sortBy': 'publishedAt',    # Options: relevancy, popularity, publishedAt
    'language': 'en',            # Change language code
    'pageSize': limit * 2,       # Articles fetched before filtering
}
```

### AI Commentary (src/ai_commentary.py)

**Change AI Model:**

```python
# Line ~16
self.model = 'mistralai/mistral-7b-instruct:free'

# Free models available:
# - mistralai/mistral-7b-instruct:free (DEFAULT - recommended)
# - meta-llama/llama-2-7b-chat:free
# - nousresearch/nous-hermes-2-7b:free
# - teknium/openhermes-2.5-mistral-7b:free

# See: https://openrouter.ai/docs#free-models
```

**Adjust AI Behavior:**

```python
# In payload (line ~60)
'temperature': 0.7,      # 0=deterministic, 1=creative
'max_tokens': 500,       # Max response length
```

**Customize Analysis Prompt:**

```python
# Line ~71-95
# Edit _build_prompt() to change what factors AI considers
# Current: price, SMAs, news headlines
# Add more: sentiment analysis, volume, volatility, etc.
```

### CSV Logger (src/csv_logger.py)

Change CSV file location:

```python
# In main.py, line ~40
csv_logger = CSVLogger('data/market_analysis.csv')  # Change path

# Or customize columns in csv_logger.py line ~26
headers = [
    'Timestamp',
    'Ticker',
    # Add/remove columns as needed
]
```

### Telegram Reporter (src/telegram_reporter.py)

**Customize Message Format:**

```python
# Edit format_report() method (line ~57) to change:
# - Emoji used
# - Information displayed
# - Message layout
# - Signal emoji selection
```

**Parse Mode Options:**

```python
# Line ~39 in send_message()
'parse_mode': 'Markdown',  # Options: 'Markdown', 'HTML', None
```

**Send to Multiple Chats:**

```python
# Modify send_message() to loop through chat IDs
for chat_id in ['123456', '789012']:
    self.send_message(message, chat_id)
```

## Workflow File Configuration

### .github/workflows/market-analysis.yml

**Change Python Version:**

```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Change to 3.9, 3.10, 3.12, etc.
```

**Add Scheduled Runs:**

```yaml
on:
  workflow_dispatch:  # Keep manual trigger
  schedule:
    - cron: '0 9 * * MON-FRI'  # 9 AM weekdays (UTC)
    # Cron format: minute hour day-of-month month day-of-week
```

**Run Multiple Stocks:**

```yaml
jobs:
  market-analysis:
    strategy:
      matrix:
        ticker: [AAPL, MSFT, GOOGL, TSLA, AMZN]
```

**Change Artifact Retention:**

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: analysis-logs
    path: |
      data/market_analysis.csv
      logs/
    retention-days: 30  # Change from default (90)
```

**Skip CSV Commit for Forks:**

```yaml
- name: Commit CSV logs
  if: github.event_name == 'workflow_dispatch' && !github.event.pull_request
  run: |
    # ... commit logic
```

## API Integration Guide

### Adding a New Data Source

Example: Adding AlphaVantage for additional indicators

```python
# Create: src/alphavantage_fetcher.py
import os
import requests

class AlphaVantageFetcher:
    def __init__(self, ticker: str):
        self.api_key = os.getenv('ALPHAVANTAGE_API_KEY')
        self.ticker = ticker
    
    def fetch_indicators(self):
        # Fetch RSI, MACD, Bollinger Bands, etc.
        pass
```

Then import in `main.py` and use results.

### Adding a New Report Channel

Example: Post to Discord instead of (or in addition to) Telegram

```python
# Create: src/discord_reporter.py
import os
import requests

class DiscordReporter:
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    def send_report(self, message: str):
        # Send to Discord
        pass
```

Then call in `main.py`.

## Performance Tuning

### Reduce Execution Time

```python
# In sma_calculator.py
# Fetch shorter history
hist_data = self._fetch_historical_data('3mo')  # Instead of '1y'

# In news_fetcher.py
# Fetch fewer articles
news_articles = news_fetcher.fetch(limit=2)  # Instead of 3

# In main.py
# Skip CSV logging if not needed
# (Remove the csv logging section)
```

### Parallel Execution

```python
# Use threading/async for multiple tickers
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(analyze_ticker, ticker)
        for ticker in ['AAPL', 'MSFT', 'GOOGL']
    ]
```

## Error Handling

### Add Retry Logic

```python
# In any fetcher module
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_with_retry(self):
    return requests.get(url)
```

### Add Monitoring/Alerting

```python
# Send alerts on error to Slack, PagerDuty, etc.
if error_occurred:
    requests.post(
        'https://hooks.slack.com/...',
        json={'text': f'Market analysis failed: {error}'}
    )
```

## Security Considerations

✅ **Secure Practices Used:**
- Secrets stored in GitHub (never in code)
- Environment variables passed at runtime
- No credentials in logs

✅ **Additional Security:**
- Review code before running
- Use separate API keys for dev/prod
- Rotate API keys periodically
- Limit GitHub Actions permissions
- Consider IP whitelisting if available

## Rate Limit Management

| Service | Free Limit | Tracking |
|---------|-----------|----------|
| GitHub Actions | 2000 min/month | Via usage page |
| NewsAPI | 100 req/day | Via dashboard |
| OpenRouter | Variable | Check docs |
| Telegram | ~30 msg/sec | N/A |

To stay within limits:
- Run max 2x daily (200 min/month)
- Use 1 ticker per run
- Cache data locally where possible

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export NEWS_API_KEY="your_key"
export OPENROUTER_API_KEY="your_key"
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# Run workflow
cd src
python main.py --ticker AAPL --log-csv
```

## Backup & Recovery

### Back up Analysis Data

```bash
# Regularly commit CSV files
git add data/market_analysis.csv
git commit -m "Analysis backup"
git push
```

### Export CSV to Other Formats

```python
# Convert to Excel
import pandas as pd

df = pd.read_csv('data/market_analysis.csv')
df.to_excel('data/market_analysis.xlsx', index=False)
```

## Troubleshooting Configuration

| Issue | Solution |
|-------|----------|
| Workflow doesn't run | Check workflow syntax, look for `on:` trigger config |
| Missing data in report | Verify all required environment variables |
| API failures | Check API rate limits and key validity |
| Slow execution | Reduce data range, limit number of articles |
| CSV not committed | Check git permissions in workflow |
