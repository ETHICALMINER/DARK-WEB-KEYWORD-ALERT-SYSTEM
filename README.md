# Dark Web Keyword Alert System (OSINT)

A lightweight defensive OSINT tool that searches the Ahmia dark web search
index for keywords tied to data leaks (e.g. "leaked database", "admin
credentials") and shows the findings in a local dashboard for early detection.

> **Disclaimer:** For defensive security research and education only.
> Monitor threats against your own organization or with authorization.
> This tool only queries a search index. It does not crawl, download, or
> access content on the hidden services themselves. Do not open suspicious
> .onion links outside an isolated environment.

## Features
- Dual-core failover: tries the Ahmia `.onion` service over Tor first, then falls back to the clearnet mirror.
- Configurable keyword list.
- SQLite storage with automatic de-duplication.
- Flask dashboard (auto-refresh) showing keyword, URL, snippet, source mode, timestamp.
- Onion URLs are displayed as plain text (not clickable) for safety.

## Architecture
```
config.py --> scanner.py --> alerts.db --> dashboard.py (http://127.0.0.1:5000)
              1. Tor (.onion)
              2. Clearnet mirror (failover)
```

## Installation
```bash
git clone https://github.com/<your-username>/darkweb-keyword-alert.git
cd darkweb-keyword-alert
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Tor (Debian/Kali/Ubuntu)
sudo apt install tor
sudo service tor start
```

## Usage
```bash
python3 scanner.py      # run a scan
python3 dashboard.py    # open http://127.0.0.1:5000
```

Schedule scans with cron (every 6 hours):
```bash
0 */6 * * * cd /path/to/darkweb-keyword-alert && venv/bin/python scanner.py
```

## Configuration
Edit `config.py`:
- `KEYWORDS`: terms to monitor (add your company/domain names)
- `TOR_PROXY`: default `socks5h://127.0.0.1:9050`
- `ONION_URL` / `MIRROR_URL`: search endpoints

## Troubleshooting
| Problem | Fix |
|---|---|
| Tor circuit fails | `sudo service tor restart`, then test with `curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org` |
| No results | Try broader keywords; check that ahmia.fi is reachable |
| Dashboard empty | Run `scanner.py` first |
| 0 results parsed | Ahmia may have changed its HTML; update selectors in `scanner.py` |

## Roadmap
- [ ] Email / Telegram alerts
- [ ] Threat scoring
- [ ] CSV / JSON export
- [ ] Docker support

## License
MIT