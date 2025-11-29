import re
from cotScraper.items import COTItem


class CotscraperPipeline:

    # precompiled regex patterns
    header_pattern = re.compile(
        r"^(.+?)\s+-\s+CHICAGO MERCANTILE EXCHANGE\s+(Code-\d{5,6}[A-Za-z+]?)",
        re.MULTILINE
    )

    commitments_pattern = re.compile(
        r"COMMITMENTS\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+"
        r"([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+"
        r"([\d,]+)\s+([\d,]+)",
        re.MULTILINE
    )

    changes_pattern = re.compile(
        r"CHANGES FROM.*?\)\s+"
        r"(-?[\d,]+)\s+(-?[\d,]+)\s+(-?[\d,]+)\s+"
        r"(-?[\d,]+)\s+(-?[\d,]+)\s+(-?[\d,]+)\s+"
        r"(-?[\d,]+)\s+(-?[\d,]+)\s+(-?[\d,]+)",
        re.MULTILINE
    )

    open_interest_pattern = re.compile(
        r"OPEN INTEREST:\s*([\d,]+)"
    )

    def clean_number(self, value):
        return int(value.replace(",", "")) if value else None

    def process_item(self, item, spider):
        text = item["plaintext"]

        # ---------- HEADER ----------
        header = self.header_pattern.search(text)
        if not header:
            spider.logger.warning("Header not found")
            return None

        asset_name = header.group(1).strip()
        code = header.group(2).strip()

        # ---------- OPEN INTEREST ----------
        open_interest = self.open_interest_pattern.search(text)
        open_interest_val = (
            self.clean_number(open_interest.group(1))
            if open_interest else None
        )

        # ---------- COMMITMENTS ----------
        com = self.commitments_pattern.search(text)
        if not com:
            spider.logger.warning("Commitments not found")
            return None

        com = [self.clean_number(x) for x in com.groups()]

        # ---------- CHANGES ----------
        ch = self.changes_pattern.search(text)
        if not ch:
            spider.logger.warning("Changes not found")
            return None

        ch = [self.clean_number(x) for x in ch.groups()]

        return COTItem(
            asset=asset_name,
            code=code,
            open_interest=open_interest_val,

            non_commercial_long=com[0],
            non_commercial_short=com[1],
            non_commercial_spread=com[2],
            commercial_long=com[3],
            commercial_short=com[4],
            total_long=com[5],
            total_short=com[6],
            nonreportable_long=com[7],
            nonreportable_short=com[8],

            ch_non_commercial_long=ch[0],
            ch_non_commercial_short=ch[1],
            ch_non_commercial_spread=ch[2],
            ch_commercial_long=ch[3],
            ch_commercial_short=ch[4],
            ch_total_long=ch[5],
            ch_total_short=ch[6],
            ch_nonreportable_long=ch[7],
            ch_nonreportable_short=ch[8],
        )
