# Company Screener

Company Screener is a backend service built with FastAPI for screening and analyzing companies using advanced language models (LLMs) and data pipelines. It integrates with OpenAI and LangChain to process data, aggregate information from various sources, and generate detailed company reports.

## Features
- FastAPI-based REST API for company screening
- Integration with OpenAI LLMs via LangChain
- Modular architecture for data aggregation, processing, and report generation
- Pydantic-based data validation and configuration

## Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd company-screener
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Set up environment variables as needed (see `.env.example` if available).
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Access the API documentation at `http://localhost:8000/docs`.

## Dependencies
- fastapi
- uvicorn
- langchain
- openai
- pydantic
- python-dotenv
- httpx

## License
Specify your license here.

## Contact
Add contact or maintainer information here.
