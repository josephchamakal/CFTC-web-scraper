import scrapy
import re


class CotSpider(scrapy.Spider):
    name = "cot"
    allowed_domains = ["www.cftc.gov"]
    start_urls = ["https://www.cftc.gov/dea/futures/deacmesf.htm"]
    
    # Bulletproof: Split on ANY "Code-######" line
    block_pattern = re.compile(
        r"(?=^.*Code-\d{5,6}[A-Za-z+]?\b)",
        re.MULTILINE
    )

    def parse(self, response):
        text = "".join(response.css("pre::text").getall()).strip()
        release_date = response.css("p::text")
        blocks = self.block_pattern.split(text)
        
        for block in blocks:
            block = block.strip()
            # Filter noise blocks (header, blanks)
            if len(block) < 100:
                continue

            yield {"plaintext": block}
