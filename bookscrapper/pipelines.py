# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()

        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        lowercase_keys = ['category', 'product_type']
        for key in lowercase_keys:
            value = adapter.get(key)
            adapter[key] = value.lower()

        price_keys = ['price_excl_tax', 'price_incl_tax', 'tax', 'price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        availability = adapter.get('availability')
        split_availability = availability.split('(')
        if len(split_availability) < 2:
            adapter['availability'] = 0
        else:
            availability_split_arr = split_availability[1].split(' ')
            adapter['availability'] = int(availability_split_arr[0])

        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        stars_string = adapter.get('stars')
        stars_string_split = stars_string.split(' ')[1].lower()
        if stars_string_split == 'zero':
            adapter['stars'] = 0
        elif stars_string_split == 'one':
            adapter['stars'] = 1
        elif stars_string_split == 'two':
            adapter['stars'] = 2
        elif stars_string_split == 'three':
            adapter['stars'] = 3
        elif stars_string_split == 'four':
            adapter['stars'] = 4
        elif stars_string_split == 'five':
            adapter['stars'] = 5

        return item


class SaveToMySQLPipeline:
    def __init__(self):
        # self.conn = mysql
        pass

    def process_item(self, item, spider):
        pass