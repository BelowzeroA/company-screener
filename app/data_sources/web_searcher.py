import asyncio

from app.core.llm_api_wrapper import LLMAPIWrapper
from app.data_sources.openai_websearch import OpenaiWebSearch
from app.models.job import ScreenerJob


class WebResearcher:
    def __init__(self, llm: LLMAPIWrapper, logger):
        # self.scraper = Scraper(logger)
        self.logger = logger
        # self.serp = SerpAPIWrapper(serpapi_api_key=SERPER_API_KEY)
        self.llm_searcher = OpenaiWebSearch(llm=llm, logger=logger)
        # self.builder = PromptBuilder()

    async def get_company_info(self, job: ScreenerJob) -> dict:
        """
        Get company information using a web search.
        Searches for the following information:
            - The name of the company.
            - The business model of the company.
            - The products and services offered by the company.
            - The market the company works on.
            - The team of the company, including founders.
        Searches only on the company website, so the pages that can be googled with site:website_url.
        Builds prompts for each of the above information and uses the LLM search engine to generate the answers.
        Args:
            job: the job object containing the company URL and other details.

        Returns:
            dict: A dictionary containing the following information.
            - company_name: The name of the company.
            - business_model: The business model of the company.
            - products_services: The products and services offered by the company.
            - market: The market the company works on.
            - team: The team of the company.
        """
        info_topics = {
            "company_name": "What is the name of the company?",
            "business_model": "What is the business model of the company? It can be B2B, B2C, C2C, etc.",
            "products_services": "What products and/or services does the company offer?",
            "market": "What market does the company work in?",
            "team": "Who are the founders and team members of the company?"
        }
        # answer = await self.llm_searcher.search_on_website(info_topics["team"], job.domain)
        async def fetch_info(key, topic):
            try:
                answer = await self.llm_searcher.search_on_website(topic, job.domain)
            except Exception as e:
                self.logger.error(f"Error searching for {key}: {e}")
                answer = "N/A"
            return key, answer

        tasks = [fetch_info(key, topic) for key, topic in info_topics.items()]
        results_list = await asyncio.gather(*tasks)
        results = {key: answer.dict() for key, answer in results_list}
        return results
