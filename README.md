# Airline Assistant Skill (Upgraded)

A demo Rasa skill showing what an airline assistant could do — beyond just linking to the website.

[![Launch on Hello Rasa](https://hello.rasa.io/launch.svg)](https://hello.rasa.io/go?repo=rasahq/airline-assistant-skill)

## Quick Start

```bash
cp .env.example .env
# Add your RASA_PRO_LICENSE and OPENAI_API_KEY

uv sync
uv run rasa train
uv run rasa inspect
```

## What It Does

- **Actually checks upgrade availability** — tells you if there's a Business/Premium upgrade and the price
- **Shows seat availability** — instead of just "go to website"
- **Instant acknowledgment** — no staring at nothing while APIs run
- **Contextual responses** — acknowledges what you asked for, even when it can't help
- **FAQ via RAG** — baggage, Flying Blue, delays, check-in
