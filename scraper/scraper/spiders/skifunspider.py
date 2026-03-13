# cd scraper
# scrapy crawl skifunspider
import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime, timedelta



# Upon visiting a page, wait for 20 seconds for all its offers to load and then start scraping it. 
playwright_meta = {
    "playwright": True,
    "playwright_page_methods": [
        PageMethod("wait_for_timeout", 20000)
    ]
}

date_pattern = r"(\d{1,2}\.\d{1,2}\.)-(\d{1,2}\.\d{1,2}\.\d{4})"


class SkifunspiderSpider(scrapy.Spider):
    name = "skifunspider"
    allowed_domains = ["skifun.eu"]
    custom_settings = {
        'FEEDS': {
            '../scraped_data/original/fra_dec_test.json': {
                'format': 'json',
                'indent': 4,         # For prettier formatting in the resulting JSON file.
                # 'overwrite': True,   # Erase existing JSON data every time the spider is re-run. 
            }
        }
    }

    def start_requests(self):
        start_urls = [
            # 'https://www.skifun.eu/rs/francuska/?d1=01.04.2026&d2=21.04.2026&pr=1&ch=0&a_0=30&z_73=1&&srv_5=1&page=1#results',#najam
            # 'https://www.skifun.eu/rs/francuska/?d1=09.12.2025&d2=15.12.2025&pr=2&ch=0&a_0=30&a_1=30&z_73=1&srv_6=1&page=1#results',#bb   
            # 'https://www.skifun.eu/rs/francuska/?d1=28.02.2026&d2=28.03.2026&pr=2&ch=0&a_0=30&z_73=1&&srv_1=1&page=1#results',#polupansion
            # 'https://www.skifun.eu/rs/francuska/?d1=03.01.2026&d2=04.01.2026&pr=1&ch=0&a_0=30&z_73=1&&srv_2=1&srv_7=1&page=1#results'#punpansion/allinclusive
        ]

        for url in start_urls:
            yield scrapy.Request(
                url=url,
                meta=playwright_meta
            )

    async def parse(self, response):
        # Get HTML of all divs that are direct children of the div with class "availability-results":
        divs_in_offers = response.css('div.availability-results > div')
        divs_in_offers_list = list(divs_in_offers)
        # print(divs_in_offers_list[0])  # prints out the HTML block of the first bundle div
        # print(divs_in_offers_list[2])  # prints out the HTML block of the first bundeunit1  (all_divs_list[1] is the irrelevant 'ajx' div between bundle and bundleunit divs)

        # Get the selected dates: 
        date_from = response.css('input#datepicker-from::attr(value)').get()
        date_to = response.css('input#datepicker-to::attr(value)').get()
        start_date = datetime.strptime(date_from, "%d.%m.%Y")
        end_date = datetime.strptime(date_to, "%d.%m.%Y")
        delta_date = end_date - start_date
        num_of_nights = delta_date.days + 1

        # Extract selected month:
        month = date_from.split('.')[1]
        month_name = month
        match month:
            case "11": month_name = "Nov"
            case "12": month_name = "Dec"
            case "01": month_name = "Jan"
            case "02": month_name = "Feb"
            case "03": month_name = "Mar"
            case "04": month_name = "Apr"

        # Other fields for offers:
        country = ''
        place = ''
        hotel = ''
        stars = ''
        service_type = ''

        # Get the type of offers from the url:
        url = response.url
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        for param in query_params:
            if param.startswith('srv'):
                used_service_checkbox_name = param
                break
        match used_service_checkbox_name:
            case "srv_5": service_type = "najam"
            case "srv_2": service_type = "all inclusive"  # "pun pansion" is considered to be the same as "all inclusive"
            case "srv_7": service_type = "all inclusive"
            case "srv_6": service_type = "nocenje s doruckom"
            case "srv_1": service_type = "polupansion"


        # Process divs:
        for cur_div in divs_in_offers_list:
            div_classes = cur_div.attrib.get('class', '')  # Get the string containing all classes assigned to the current div.

            # Process new hotel: (save its data in temporary variables)
            if div_classes == 'bundle': 
                location = cur_div.css('div.bundlespan font.bundletitle::text').get().strip()
                country = location.split(' ')[0]
                place = ' '.join(location.split(' ')[1:])
                hotel = cur_div.css('div.bundlespan font.bundletitle2::text').get()
                stars_arr = cur_div.css('div.stars span.bundlestars')
                stars = len(stars_arr) if stars_arr else 0
            
            # Process new hotel offer: (save its data together with the above hotel data in a json file as an Offer object)
            elif 'bundleunit1' in div_classes:
                # Price:
                price_texts = cur_div.css('font.pricelabel3 *::text').getall()
                price = ''.join(price_texts).strip()
                if (price == '€' or price == '0€'): continue

                # Set offer dates to searched dates:
                offer_month = month_name
                offer_date = date_from
                offer_nights = num_of_nights
                # Find the actual offer date (if it is displayed):
                offer_date_text = cur_div.css('font.pricelabel4::text').get().strip()
                if offer_date_text:
                    match = re.search(date_pattern, offer_date_text)
                    if match:
                        start_date_str = match.group(1)
                        end_date_str = match.group(2)

                        start_date = datetime.strptime(start_date_str + end_date_str.split('.')[-1], "%d.%m.%Y")
                        end_date = datetime.strptime(end_date_str, "%d.%m.%Y")

                        # Special case when the offer begins in december and ends in january (different years):
                        if end_date < start_date:
                            end_year = int(end_date_str.split('.')[-1])
                            start_date = start_date.replace(year=end_year - 1)

                        # Calculate number of nights:
                        delta_date = end_date - start_date
                        offer_nights = delta_date.days + 1

                # Number of guests:
                offer_title = cur_div.css('font.roomtitle::text').get()
                offer_title_words = offer_title.split(" ")
                num_of_guests = int((offer_title_words[2].split('-'))[0])
                if offer_title_words[3] == 'DO': num_of_guests += '-' + offer_title_words[4]  # Sometimes the title is: SOBA ZA 2 DO 4 OSOBE. 

                # Room size:
                room_size = cur_div.css('div.roombox2 b::text').get().strip() + "2"

                # Return offer data:
                yield {
                    'country': country,
                    'place': place,
                    'hotel': hotel,
                    'stars': stars,
                    'month': offer_month,
                    'date': offer_date,
                    'num_of_nights': offer_nights,
                    'num_of_guests': num_of_guests,
                    'service_type': service_type,
                    'room_size': room_size,
                    'price': price
                }

        # Visit the next results page:
        if response.css("ul.pagination") is not None:  # When there is only one page in total, there is no pagination component on page.
            active_li = response.css("ul.pagination li.active")
            if active_li:
                next_li = active_li.xpath("following-sibling::li[1]").get()
                if next_li:
                    next_pages = active_li.xpath("following-sibling::li")
                    next_page = next_pages[0] if next_pages else None
                    if next_page:
                        # When we are on the last page, the only <li> element right of it is the arrow button and it is also active. That is the condition that needs to be true to end indexing and crawling.
                        next_page_classes = next_page.attrib.get('class', '')
                        if 'active' not in next_page_classes:
                            url_parts = url.split('page=')
                            next_page_num = int((url_parts[1].split('#'))[0]) + 1

                            next_page_url = url_parts[0] + "page=" + str(next_page_num) + '#results'
                            # Upon visiting the next page, wait again for 10s for all offers to load before starting to scrape the page. 
                            yield response.follow(
                                next_page_url,
                                self.parse,
                                meta=playwright_meta
                            )