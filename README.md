# Adaptive Vendor Evaluation Agent

An intelligent agent-based system for evaluating and comparing vendors with dynamic criteria re-weighting based on discovered information.

## Overview

This system goes beyond static comparison matrices by adaptively adjusting evaluation criteria based on discoveries during research. For example:
- Finding a major outage increases weight on uptime history
- Missing SDK support triggers deeper integration effort analysis
- Hidden risks (maintainer departures, pricing patterns) influence recommendations

## Architecture

### Three-Layer Design

1. **Interface Layer** - SOUL.md powered senior tech evaluator/CTO advisor
2. **Logic Layer** - Four specialized components:
   - Candidate Identifier: Discovers vendor candidates
   - Multi-Criteria Researcher: Deep vendor analysis
   - Dynamic Weight Adjuster: Adaptive criteria weighting
   - Recommendation Synthesizer: Final recommendation with reasoning
3. **Integration Layer** - ClawHub web-search for vendor discovery

## Features

- ✅ Autonomous candidate identification
- ✅ Dynamic criteria re-weighting (adaptive evaluation)
- ✅ Deep research (GitHub sentiment, status pages, community health)
- ✅ Context-aware (tech stack, domain, compliance)
- ✅ Hidden risk detection (maintainer churn, pricing patterns)
- ✅ Structured comparison with reasoning chain
- ✅ Telegram bot interface

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key
- Telegram bot token
- ClawHub access

### Installation

1. Clone the repository:
```bash
cd /path/to/openclaw-buildathon
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Edit `.env` file with your credentials:

```env
OPENAI_API_KEY=sk-your-key-here
TELEGRAM_BOT_TOKEN=your-bot-token-here
CLAWHUB_API_URL=https://api.clawhub.com
```

## Usage

### Running the Telegram Bot

```bash
python main.py
```

### Example Evaluation Request

Send to your Telegram bot:
```
/evaluate

Category: Payment Gateway
Requirements:
- Tech Stack: Golang, Python, AWS
- Domain: Fintech (RBI compliance required)
- Priority: Security, uptime, integration ease
```

### Expected Output

The agent will:
1. Identify 3-5 relevant candidates (Stripe, Razorpay, PayPal, etc.)
2. Research each across multiple dimensions
3. Dynamically adjust criteria weights based on findings
4. Produce structured comparison with reasoning chain
5. Recommend best fit with trade-off analysis

## Deployment to Hostinger VPS

### Setup on VPS

```bash
# SSH into your VPS
ssh user@your-hostinger-vps

# Clone repository
git clone <your-repo-url>
cd openclaw-buildathon

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
nano .env
# Add your API keys

# Run with systemd or screen
screen -S vendor-agent
python main.py
```

### Using systemd (recommended)

Create `/etc/systemd/system/vendor-agent.service`:

```ini
[Unit]
Description=Vendor Evaluation Agent
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/openclaw-buildathon
Environment="PATH=/path/to/openclaw-buildathon/venv/bin"
ExecStart=/path/to/openclaw-buildathon/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable vendor-agent
sudo systemctl start vendor-agent
sudo systemctl status vendor-agent
```

## Evaluation Rubric

- **30% Adaptive Evaluation**: Criteria weights change based on discoveries
- **25% Research Depth**: Beyond surface-level information
- **20% Contextual Awareness**: Tech stack, domain, compliance factors
- **15% Recommendation Quality**: Clear reasoning, honest trade-offs
- **10% Reproducibility**: Can re-run with fresh data

## Project Structure

```
openclaw-buildathon/
├── main.py                          # Entry point
├── config.py                        # Configuration management
├── SOUL.md                          # Agent personality definition
├── requirements.txt                 # Dependencies
├── .env                            # Environment configuration
├── agents/
│   ├── __init__.py
│   ├── candidate_identifier.py     # Logic Layer: Candidate discovery
│   ├── researcher.py               # Logic Layer: Multi-criteria research
│   ├── weight_adjuster.py          # Logic Layer: Dynamic weighting
│   └── synthesizer.py              # Logic Layer: Recommendation synthesis
├── integrations/
│   ├── __init__.py
│   ├── clawhub.py                  # ClawHub web-search integration
│   └── openai_client.py            # OpenAI API wrapper
├── interfaces/
│   ├── __init__.py
│   └── telegram_bot.py             # Telegram bot interface
└── utils/
    ├── __init__.py
    ├── logger.py                   # Logging utilities
    └── prompts.py                  # Prompt templates
```

## License

MIT
