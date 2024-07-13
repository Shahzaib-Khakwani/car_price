import scrapy
# from playwright.sync_api import sync_playwright
import json
from ..items import VechileItem


class UsedcarSpider(scrapy.Spider):
    name = "usedCar"
    allowed_domains = ["www.pakwheels.com"]
    start_urls = ["https://www.pakwheels.com/used-cars/"]
    base_url = "https://www.pakwheels.com"

    def start_requests(self):
        url = "https://www.pakwheels.com/used-cars/"
        yield scrapy.Request(
            url=url,
            meta={
                "playwright": True
            }
        )

    def parse(self, response):
        cities = response.css("ul#browse-by-city-car li a::attr(href)")
        base_url = "https://www.pakwheels.com"

        for city in cities[1:]:
            city_url = city.get()
            new_url = base_url + city_url
            yield response.follow(new_url, callback= self.parseCityPage)




    def parseCityPage(self, response):
        lists = response.css("ul.search-results-mid")

        for car_list in lists:
            car_cards = car_list.css("div.col-md-9")
            for car_card in car_cards:
                car_url = car_card.css("div.search-title a::attr(href)").get()
                new_url = self.base_url + car_url
                yield response.follow(new_url, callback = self.parseCarPage)
    


        next_url = response.xpath("//a[@rel='next']/@href").get()
        if next_url is not None:
            next_url_complete = self.base_url+next_url

            yield response.follow(next_url_complete, callback = self.parseCityPage)



    def parseCarPage(self, response):
        try:
            script = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/script/text()").get()
            data = json.loads(script)
        except:
            script = response.xpath("/html/body/div[6]/div/div[1]/div[7]/ul/li[1]/a/script/text()").get()
            data = json.loads(script)


        if data:
            vechile = VechileItem()

            try:
                vechile["askingDate"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul/li[12]/text()").get().split(',')[1].strip()
            except:
                vechile["askingDate"] = None

            try:
                vechile["price"] = data["offers"]["price"]
            except:
                vechile["price"] = None


            try:
                vechile["city"] = data["name"].split("in")[1].strip()
            except:
                vechile["city"] = None

            try:
                vechile["company"] = data["brand"]["name"]
            except:
                vechile["company"] = data["name"].split(" ")[0].strip()
            
            try:
                vechile["model"] = data["model"]
            except:
                if data["description"]:
                    vechile["model"] = data["description"].split("for")[0].replace(data["brand"]["name"],"").replace(data["modelDate"],"")
                    

            
            try:
                vechile["version"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/h1/text()").get().replace(data['model'],'').replace(data['brand']['name'],'').replace(str(data['modelDate']),"").strip()
            except:
                vechile["version"] = None
            
            try:
                vechile["body_type"] = data["bodyType"]
            except:
                vechile["body_type"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul/li[10]/a/text()").get()
            

            try:
                vechile["model_year"] = data["modelDate"]
            except:
                vechile["model_year"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/table/tbody/tr/td[1]/p/text()").get().replace("\n","")

            try:
                vechile["engine_capacity"] = data["vehicleEngine"]["engineDisplacement"]
            except:
                vechile["engine_capacity"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul/li[8]/text()").get().replace(" ","")

            try:
                vechile["engine_type"] = data["fuelType"]
            except:
                vechile["engine_type"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/table/tbody/tr/td[3]/p/a/text()").get()

            try:
                vechile["mileage"] = data["mileageFromOdometer"]
            except:
                vechile["mileage"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/table/tbody/tr/td[2]/p/text()").get()

            try:
                vechile["transmission"] = data["vehicleTransmission"]
            except:
                vechile["transmission"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/table/tbody/tr/td[4]/p/text()").get()

            try: 
                vechile["exterior_color"] = data["color"]
            except:
                vechile["exterior_color"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul/li[4]/text()").get()


            
            vechile["registration_city"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[1]/li[2]/text()").get().strip()
            vechile["assembly"] = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[1]/li[6]/text()").get().strip()
            


            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[3]/text()").get():
                vechile["air_bags"] = True 
            else:
                vechile["air_bags"] = False 
            
            
            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[4]/text()").get():
                vechile["air_conditioning"] = True

            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[15]/text()").get():
                vechile["power_windows"] = True
            else:
                vechile["power_windows"] = False

            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[12]/text()").get():
                vechile["power_locks"] = True
            else:
                vechile["power_locks"] = False

            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[10]/text()").get():
                vechile["keyless_entry"] = True
            else:
                vechile["keyless_entry"] = False

            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[13]/text()").get():
                vechile["power_mirrors"] = True
            else:
                vechile["power_mirrors"] = False

            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[7]/text()").get():
                vechile["cruise_control"] = True
            else:
                vechile["cruise_control"] = False

            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[1]/text()").get():
                vechile["abs_brakes"] = True
            else:
                vechile["abs_brakes"] = False

            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[11]/text()").get():
                vechile["navigation_system"] = True
            else:
                vechile["navigation_system"] = False

            if response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/ul[2]/li[5]/text()").get():
                vechile["alloy_rims"] = True
            else:
                vechile["alloy_rims"] = False

            Exterior_Body_Rating = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/div[3]/ul/li[1]/div[1]/text()").get()
            if Exterior_Body_Rating:
                vechile["Exterior_Body_Rating"] = Exterior_Body_Rating.replace("\n","").strip()
            else:
                vechile["Exterior_Body_Rating"] = Exterior_Body_Rating

            Suspension_Steering_Rating = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/div[3]/ul/li[3]/div[1]/text()").get()
            if Suspension_Steering_Rating:
                vechile["Suspension_Steering_Rating"] = Suspension_Steering_Rating.replace("\n","").strip()
            else:
                vechile["Suspension_Steering_Rating"] = Suspension_Steering_Rating


            Engine_Transmission_Clutch_Rating = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/div[3]/ul/li[2]/div[1]/text()").get()
            if Engine_Transmission_Clutch_Rating:
                vechile["Engine_Transmission_Clutch_Rating"] = Engine_Transmission_Clutch_Rating.replace("\n","").strip()
            else:
                vechile["Engine_Transmission_Clutch_Rating"] = Engine_Transmission_Clutch_Rating

            Interior_Rating = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/div[3]/ul/li[4]/div[1]/text()").get()
            if Interior_Rating:
                vechile["Interior_Rating"] = Interior_Rating.replace("\n","").strip()
            else:
                vechile["Interior_Rating"] = Interior_Rating


            AC_HeaterRating = response.xpath("/html/body/div[6]/div/div[1]/div[2]/div[1]/div/div[3]/ul/li[5]/div[1]/text()").get()
            if AC_HeaterRating:
                vechile["AC_HeaterRating"] = AC_HeaterRating.replace("\n","").strip()
            else:
                vechile["AC_HeaterRating"] = AC_HeaterRating

            
            
            yield vechile  



            









































