import scrapy


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["airsoftstation.com"]
    start_urls = ["https://www.airsoftstation.com/airsoft-guns/"]

    def parse(self, response):
        urls=response.xpath('//figure[@class="card-figure"]/a/@href').extract()
        # print(len(urls))
        # print(urls)
        # print(response.status)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.details)
        # next_page = response.xpath('//li[@class="pagination-item pagination-item--next"]/a/@href').get()
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)
    def details(self,response):
        url=response.url
        category=response.xpath('//ol[@class="breadcrumbs"]/li[2]/a[@class="breadcrumb-label"]/span/text()').get()
        title=response.xpath('//div[@class="productView-product"]/h1/text()').get()
        key=response.xpath('//div[@id="stickyadd"]/dt/text()').get()
        value=response.xpath('//div[@id="stickyadd"]/dd/text()').get()
        image_urls = response.xpath(
            '//ul[@class="productView-thumbnails"]/li[@class="productView-thumbnail"]/a/@href').getall()
        None_sale_price = response.xpath(
            '//span[@class="price price--non-sale" and @data-product-non-sale-price-without-tax]/text()').get().strip()
        sale_price = response.xpath(
            '//span[@class="price price--withoutTax" and @data-product-price-without-tax]/text()').get().strip()
        customize_text = response.xpath('//div[@class="dexterproductoptionsheading"]/h4/text()').get()
        description_text = response.xpath('//div[@id="tabs-contents"]/p/text()').getall()
        paragraphs = response.xpath('(//div[@class="tab-content is-active" and @id="tab-description"]/p)//text()').getall()


        paragraph=None
        if paragraphs:
            paragraph =" ".join(paragraphs).replace("Features:","")

        details = {}
        detail_names = response.xpath(
            '//div[@class="tab-content is-active" and @id="tab-description"]//dt[@class="productView-info-name"]/text()').getall()
        detail_values = response.xpath(
            '//div[@class="tab-content is-active" and @id="tab-description"]//dd[@class="productView-info-value"]/text()').getall()
        list_items = response.xpath(
            '//div[@class="tab-content is-active" and @id="tab-description"]//ul/li/text()').getall()

        # for name, value in zip(detail_names, detail_values):
        #     details[name.strip()] = value.strip()
        # Printing the extracted text
        # print(category)
        # print(title)
        # print(key)
        # print(value)
        # print(image_urls)
        # print(None_sale_price)
        # print(sale_price)
        # print("Customize Text:", customize_text)
        # print(paragraph.replace("Features:"," "))
        # print(detail_names)
        # for item in list_items:
        #     print(item.strip())
        product=[]
        for image in image_urls:
            product_info={}
            product_info['url']=url
            product_info['category'] = "{} >".format(category)
            product_info['title'] = title
            product_info['none_sale_price'] = None_sale_price
            product_info['sale_price'] = sale_price
            product_info['customize_text'] = customize_text
            product_info['paragraphs_text'] = paragraphs
            # product_info['details'] = details
            product_info['Features'] = None
            product_info['image_urls'] = image
            # product.append(product_info)
            yield product_info
        for item in list_items:
            product_info = {}
            product_info['url']=url

            product_info['category'] = "{} >".format(category)
            product_info['title'] = title
            product_info['none_sale_price'] = None_sale_price
            product_info['sale_price'] = sale_price
            product_info['customize_text'] = customize_text
            product_info['paragraphs_text'] = paragraphs
            # product_info['details'] = details
            product_info['Features'] = item
            # product.append(product_info)
            yield product_info
        print(product)
        yield product


