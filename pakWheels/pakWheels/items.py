# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PakwheelsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class VechileItem(scrapy.Item):
    askingDate = scrapy.Field()
    company = scrapy.Field()
    mileage = scrapy.Field()
    price = scrapy.Field()
    model = scrapy.Field()
    city = scrapy.Field()
    version = scrapy.Field()
    body_type = scrapy.Field()
    model_year = scrapy.Field()
    engine_capacity = scrapy.Field()
    engine_type = scrapy.Field()
    transmission = scrapy.Field()
    exterior_color = scrapy.Field()
    registration_city = scrapy.Field()
    assembly = scrapy.Field()
    air_bags = scrapy.Field()
    air_conditioning = scrapy.Field()
    power_windows = scrapy.Field()
    power_locks = scrapy.Field()
    keyless_entry = scrapy.Field()
    power_mirrors = scrapy.Field()
    cruise_control = scrapy.Field()
    abs_brakes = scrapy.Field()
    navigation_system = scrapy.Field()
    alloy_rims = scrapy.Field()
    Exterior_Body_Rating = scrapy.Field()
    Suspension_Steering_Rating = scrapy.Field()
    Engine_Transmission_Clutch_Rating = scrapy.Field()
    Interior_Rating = scrapy.Field()
    AC_HeaterRating = scrapy.Field()
    
