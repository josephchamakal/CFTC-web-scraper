import scrapy


class COTItem(scrapy.Item):
    asset = scrapy.Field()
    code = scrapy.Field()
    open_interest = scrapy.Field()

    non_commercial_long = scrapy.Field()
    non_commercial_short = scrapy.Field()
    non_commercial_spread = scrapy.Field()
    commercial_long = scrapy.Field()
    commercial_short = scrapy.Field()
    total_long = scrapy.Field()
    total_short = scrapy.Field()
    nonreportable_long = scrapy.Field()
    nonreportable_short = scrapy.Field()

    ch_non_commercial_long = scrapy.Field()
    ch_non_commercial_short = scrapy.Field()
    ch_non_commercial_spread = scrapy.Field()
    ch_commercial_long = scrapy.Field()
    ch_commercial_short = scrapy.Field()
    ch_total_long = scrapy.Field()
    ch_total_short = scrapy.Field()
    ch_nonreportable_long = scrapy.Field()
    ch_nonreportable_short = scrapy.Field()
