# Agent Documentation

## Overview
This agent uses a locally deployed Qwen Code API proxy to answer user queries. It is implemented in `agent.py` and communicates with the LLM via an OpenAI-compatible interface.

## LLM Provider
- **Provider**: Custom proxy based on Qwen Code.
- **Model**: `qwen3-coder-plus`
- **API Base URL**: `http://10.93.24.167:42005/v1`
- **API Key**: `queen` (set via environment variable `LLM_API_KEY`)

## How to Run
1. Ensure you have Python 3.8+ and install dependencies:
   ```bash
   pip install openai
