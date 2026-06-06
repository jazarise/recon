import re
from typing import List

class RegexParsers:
    EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    IPV4_REGEX = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

    @staticmethod
    def extract_emails(text: str) -> List[str]:
        return list(set(RegexParsers.EMAIL_REGEX.findall(text)))

    @staticmethod
    def extract_ipv4(text: str) -> List[str]:
        return list(set(RegexParsers.IPV4_REGEX.findall(text)))
