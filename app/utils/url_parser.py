"""
Utilities for parsing and extracting information from URLs.
"""
from urllib.parse import urlparse
import re
from typing import Optional


def extract_company_name_from_url(url: str) -> str:
    """
    Extract the company name from a URL.

    Args:
        url: The company URL (e.g., https://lightmatter.co/)

    Returns:
        The extracted company name (e.g., "lightmatter")
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Remove www. if present
    if domain.startswith('www.'):
        domain = domain[4:]

    # Extract the main part of the domain (before the TLD)
    main_domain = domain.split('.')[0]

    # Clean up and normalize the company name
    company_name = main_domain.replace('-', ' ').replace('_', ' ')

    return company_name



def extract_domain_from_url(url: str) -> str:
    """
    Extract the company name from a URL.

    Args:
        url: The company URL (e.g., https://lightmatter.co/)

    Returns:
        The extracted company name (e.g., "lightmatter")
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Remove www. if present
    if domain.startswith('www.'):
        domain = domain[4:]

    return domain


def is_company_website(url: str) -> bool:
    """
    Check if a URL is likely a company website.

    Args:
        url: URL to check

    Returns:
        True if the URL is likely a company website, False otherwise
    """
    parsed_url = urlparse(url)

    # Check if the URL has a valid domain
    if not parsed_url.netloc:
        return False

    # Check if it's not a common non-company platform
    non_company_domains = [
        'facebook.com', 'linkedin.com', 'twitter.com', 'instagram.com',
        'youtube.com', 'medium.com', 'github.com', 'wikipedia.org',
        'google.com', 'amazon.com', 'apple.com', 'microsoft.com'
    ]

    for domain in non_company_domains:
        if domain in parsed_url.netloc:
            return False

    return True
