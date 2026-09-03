# Price Monitoring & Web Scraping

Comprehensive guide for building robust web scrapers with anti-bot evasion, proxy management, and price monitoring systems.

## Triggers

Use this skill when the user mentions:
- "price monitoring"
- "web scraping"
- "scrape website"
- "anti-bot bypass"
- "playwright scraping"
- "proxy rotation"
- "CAPTCHA handling"
- "price tracker"
- "product monitoring"

## Overview

This skill provides battle-tested patterns for web scraping with focus on anti-bot evasion, reliability, and scalability. Based on real-world price monitoring implementations.

## Architecture Patterns

### Pattern 1: Fallback Chain Strategy

**Progressive enhancement approach:**
```
HTTP Request → Browser (Playwright) → Undetected Browser → FlareSolverr → Manual Review
```

Each method has trade-offs:
- **HTTP**: Fast, cheap, but easily blocked
- **Browser**: Handles JS, moderate detection
- **Undetected**: Stealth mode, harder to detect
- **FlareSolverr**: Cloudflare bypass, slow
- **Manual**: Last resort for complex CAPTCHAs

### Pattern 2: Scraper Registry

**Centralized scraper management:**
```typescript
interface Scraper {
  name: string;
  domains: string[];
  method: "http" | "browser" | "api";
  selectors: Record<string, string>;
  rateLimit: { requests: number; windowMs: number };
}

const scrapers: Scraper[] = [
  {
    name: "amazon",
    domains: ["amazon.com", "amazon.co.uk"],
    method: "browser",
    selectors: {
      title: "#productTitle",
      price: ".a-price-whole",
      availability: "#availability span"
    },
    rateLimit: { requests: 10, windowMs: 60000 }
  }
];
```

## Workflow

### 1. Planning Phase

**Define scraping requirements:**
- Target websites and data points
- Update frequency (real-time vs periodic)
- Scale (pages per day)
- Anti-bot measures on target sites
- Budget for proxies/services

### 2. HTTP Scraping (Simple Sites)

**Basic HTTP scraper:**
```python
import httpx
from selectolax.parser import HTMLParser

async def scrape_http(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        tree = HTMLParser(response.text)
        
        return {
            "title": tree.css_first("h1.product-title").text(),
            "price": tree.css_first("span.price").text(),
            "url": url
        }
```

### 3. Browser Scraping (JS-Heavy Sites)

**Playwright with stealth:**
```python
from playwright.async_api import async_playwright

async def scrape_browser(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )
        
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            locale="en-US",
        )
        
        # Stealth mode
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for content
            await page.wait_for_selector("h1.product-title", timeout=10000)
            
            # Extract data
            title = await page.locator("h1.product-title").text_content()
            price = await page.locator("span.price").text_content()
            
            return {"title": title, "price": price, "url": url}
        finally:
            await browser.close()
```

### 4. Proxy Integration

**Rotating proxy pool:**
```python
import random
from typing import List

class ProxyPool:
    def __init__(self, proxies: List[str]):
        self.proxies = proxies
        self.failed = set()
    
    def get_proxy(self) -> str | None:
        available = [p for p in self.proxies if p not in self.failed]
        if not available:
            return None
        return random.choice(available)
    
    def mark_failed(self, proxy: str):
        self.failed.add(proxy)
    
    def reset_failures(self):
        self.failed.clear()

# Usage
proxy_pool = ProxyPool([
    "http://proxy1.com:8080",
    "http://proxy2.com:8080",
    "http://proxy3.com:8080",
])

async def scrape_with_proxy(url: str) -> dict:
    proxy = proxy_pool.get_proxy()
    if not proxy:
        raise Exception("No proxies available")
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                proxy={"server": proxy}
            )
            # ... scraping logic
    except Exception as e:
        proxy_pool.mark_failed(proxy)
        raise
```

### 5. CAPTCHA Handling

**Detection and graceful degradation:**
```python
async def detect_captcha(page) -> bool:
    # Check for common CAPTCHA indicators
    captcha_selectors = [
        "iframe[src*='recaptcha']",
        "iframe[src*='hcaptcha']",
        ".g-recaptcha",
        "#challenge-form",  # Cloudflare
    ]
    
    for selector in captcha_selectors:
        if await page.locator(selector).count() > 0:
            return True
    
    return False

async def scrape_with_captcha_handling(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(url)
        
        if await detect_captcha(page):
            # Log for manual review
            await page.screenshot(path=f"captcha_{int(time.time())}.png")
            raise CaptchaDetectedError("CAPTCHA detected, manual intervention needed")
        
        # Continue scraping
        return await extract_data(page)
```

### 6. FlareSolverr Integration

**Cloudflare bypass:**
```python
import httpx

async def solve_cloudflare(url: str) -> str:
    """Use FlareSolverr to bypass Cloudflare protection"""
    flaresolverr_url = "http://localhost:8191/v1"
    
    payload = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(flaresolverr_url, json=payload, timeout=120)
        result = response.json()
        
        if result["status"] == "ok":
            return result["solution"]["response"]
        else:
            raise Exception(f"FlareSolverr failed: {result.get('message')}")

# Usage in fallback chain
async def scrape_with_fallback(url: str) -> dict:
    try:
        return await scrape_http(url)
    except Exception:
        try:
            return await scrape_browser(url)
        except Exception:
            html = await solve_cloudflare(url)
            return parse_html(html)
```

### 7. Rate Limiting

**Respect site limits:**
```python
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    async def acquire(self, domain: str, max_requests: int, window_seconds: int):
        now = datetime.now()
        cutoff = now - timedelta(seconds=window_seconds)
        
        # Clean old requests
        self.requests[domain] = [
            ts for ts in self.requests[domain] if ts > cutoff
        ]
        
        if len(self.requests[domain]) >= max_requests:
            # Calculate wait time
            oldest = self.requests[domain][0]
            wait_seconds = (oldest + timedelta(seconds=window_seconds) - now).total_seconds()
            await asyncio.sleep(max(0, wait_seconds))
        
        self.requests[domain].append(now)

rate_limiter = RateLimiter()

async def scrape_with_rate_limit(url: str) -> dict:
    domain = urlparse(url).netloc
    await rate_limiter.acquire(domain, max_requests=10, window_seconds=60)
    return await scrape(url)
```

### 8. Data Extraction Patterns

**Robust selector strategies:**
```python
async def extract_with_fallback(page, selectors: List[str]) -> str | None:
    """Try multiple selectors until one works"""
    for selector in selectors:
        try:
            element = page.locator(selector).first
            if await element.count() > 0:
                return await element.text_content()
        except Exception:
            continue
    return None

# Usage
price = await extract_with_fallback(page, [
    "span.price-current",
    ".product-price",
    "[data-price]",
    "meta[property='product:price:amount']"
])
```

### 9. Change Detection

**Monitor for price changes:**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PriceSnapshot:
    url: str
    price: float
    timestamp: datetime
    availability: str

class PriceMonitor:
    def __init__(self):
        self.history: dict[str, list[PriceSnapshot]] = {}
    
    def add_snapshot(self, snapshot: PriceSnapshot):
        if snapshot.url not in self.history:
            self.history[snapshot.url] = []
        self.history[snapshot.url].append(snapshot)
    
    def detect_changes(self, url: str) -> dict | None:
        snapshots = self.history.get(url, [])
        if len(snapshots) < 2:
            return None
        
        current = snapshots[-1]
        previous = snapshots[-2]
        
        changes = {}
        if current.price != previous.price:
            changes["price"] = {
                "old": previous.price,
                "new": current.price,
                "change_pct": ((current.price - previous.price) / previous.price) * 100
            }
        
        if current.availability != previous.availability:
            changes["availability"] = {
                "old": previous.availability,
                "new": current.availability
            }
        
        return changes if changes else None

# Usage
monitor = PriceMonitor()

async def check_and_notify(url: str):
    data = await scrape(url)
    snapshot = PriceSnapshot(
        url=url,
        price=parse_price(data["price"]),
        timestamp=datetime.now(),
        availability=data["availability"]
    )
    
    monitor.add_snapshot(snapshot)
    changes = monitor.detect_changes(url)
    
    if changes:
        await send_notification(url, changes)
```

### 10. Error Recovery

**Retry with exponential backoff:**
```python
import asyncio
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, base_delay=2)
async def scrape_with_retry(url: str) -> dict:
    return await scrape(url)
```

## Configuration Example

**Complete scraper config:**
```python
from pydantic import BaseSettings

class ScraperConfig(BaseSettings):
    # Proxy settings
    proxy_enabled: bool = True
    proxy_list: str = "proxies.txt"
    proxy_rotation: str = "round-robin"  # or "random"
    
    # Rate limiting
    requests_per_minute: int = 10
    concurrent_requests: int = 3
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 2
    
    # Browser settings
    headless: bool = True
    browser_timeout: int = 30000
    
    # Fallback chain
    fallback_order: str = "http,browser,flaresolverr"
    
    # CAPTCHA handling
    captcha_screenshot_dir: str = "./captcha-screenshots"
    captcha_timeout: int = 120
    
    # Monitoring
    check_interval: int = 300  # 5 minutes
    alert_on_price_drop: bool = True
    alert_threshold_pct: float = 5.0
    
    class Config:
        env_prefix = "SCRAPER_"
        env_file = ".env"
```

## Best Practices

1. **Start Simple** - Begin with HTTP, add complexity only when needed
2. **Respect robots.txt** - Check site policies
3. **Rate Limit Aggressively** - Better slow than blocked
4. **Rotate User Agents** - Vary browser fingerprints
5. **Use Proxies** - Distribute requests across IPs
6. **Handle Failures Gracefully** - Log, retry, alert
7. **Monitor Success Rates** - Track scraper health
8. **Cache Responses** - Avoid redundant requests
9. **Validate Data** - Check extracted data quality
10. **Legal Compliance** - Ensure scraping is permitted

## Common Anti-Bot Measures

### Detection Method 1: Browser Fingerprinting
**Countermeasure:** Randomize viewport, user agent, timezone, language

### Detection Method 2: Behavioral Analysis
**Countermeasure:** Add random delays, mouse movements, scroll patterns

### Detection Method 3: IP Reputation
**Countermeasure:** Use residential proxies, rotate IPs

### Detection Method 4: CAPTCHA Challenges
**Countermeasure:** FlareSolverr, CAPTCHA solving services, manual review

### Detection Method 5: Rate Limiting
**Countermeasure:** Respect limits, use multiple IPs, slow down

## Tools to Use

- `bash` - Run scraper processes
- `write` - Create scraper files
- `read` - Read existing scrapers
- `edit` - Update configurations
- `grep` - Search for patterns in scraped data

## Example Session

```
User: "Build a price monitor for Amazon products"

Agent:
1. Creates scraper with fallback chain (HTTP → Browser → FlareSolverr)
2. Implements proxy rotation
3. Adds CAPTCHA detection and screenshot capture
4. Sets up rate limiting (10 req/min)
5. Creates price change detection
6. Adds Discord notifications for price drops
7. Implements error recovery with retries
8. Provides Docker setup for deployment

User: "Add support for eBay"

Agent:
1. Adds eBay scraper to registry
2. Configures eBay-specific selectors
3. Implements eBay API fallback
4. Adjusts rate limits for eBay
5. Tests scraper on sample products
6. Updates documentation
```

## Deployment Considerations

1. **Docker** - Containerize for consistent environment
2. **Scheduling** - Use cron or task scheduler
3. **Monitoring** - Track success rates, errors, latency
4. **Alerting** - Notify on failures or price changes
5. **Logging** - Structured logs for debugging
6. **Scaling** - Horizontal scaling with queue system
7. **Cost** - Monitor proxy/service costs

## Legal & Ethical

- Check website Terms of Service
- Respect robots.txt
- Don't overload servers
- Don't scrape personal data without consent
- Consider API alternatives first
- Be transparent about scraping purpose

## References

- [Playwright Documentation](https://playwright.dev/)
- [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr)
- [Scrapy Best Practices](https://docs.scrapy.org/en/latest/topics/practices.html)

## Notes

- Always test scrapers in development first
- Keep scraper code modular and maintainable
- Document selector strategies for each site
- Monitor for site structure changes
- Have fallback plans for critical scrapers