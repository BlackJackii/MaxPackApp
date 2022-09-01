import json


class Package:
    def __init__(self):
        self.p_width = 0
        self.p_height = 0
        self.p_bottom = 0
        self.roll_format = 0
        self.sleeve_length = 0
        self.squaring = 0
        self.handle = 0
        self.first_layer = 0
        self.second_layer = 0
        self.third_layer = 0
        self.raw_paper_cost = 0
        self.raw_paper_cost_after_counting = 0
        self.weight_first_layer = 0
        self.weight_second_layer = 0
        self.weight_third_layer = 0
        self.cost_first_layer_raw = 0
        self.cost_second_layer_raw = 0
        self.cost_third_layer_raw = 0
        self.bottom_squaring = 0
        self.bottom_raw_gram = 0
        self.bottom_weight = 0
        self.bottom_cost = 0
        self.exchange_rate_eur = 33
        self.exchange_rate_usd = 28
        self.margin = 45
        self.self_cost_package = 1
        self.margin_sum = 0
        self.cost_for_customer = 0
        self.shading_percentages = 0
        self.paint_spend = 0
        self.paint_cost = 0
        self.paint_cost_one_gram = 0
        self.painting_cost = 0
        self.workpiece_area = 0
        self.paint_cost_eur = 0
        self.paint_cost_uah = 0
        self.raw_package_cost_after_counting = 0
        self.currency = "UAH"
        self.order_price = 0
        self.order_amount = 1

    def roll_format_func(self):
        self.roll_format = (self.p_width * 2 + self.p_bottom * 2) + 20
        return self.roll_format

    def sleeve_length_func(self):
        self.sleeve_length = self.p_height + (self.p_bottom / 2) + 20
        return self.sleeve_length

    def squaring_func(self):
        self.squaring = self.roll_format * self.sleeve_length / 1000000
        return self.squaring

    def weight_first_layer_func(self):
        self.weight_first_layer = self.squaring * self.first_layer / 1000
        return self.weight_first_layer

    def weight_second_layer_func(self):
        self.weight_second_layer = self.squaring * self.second_layer / 1000
        return self.weight_second_layer

    def weight_third_layer_func(self):
        self.weight_third_layer = self.squaring * self.third_layer / 1000
        return self.weight_third_layer

    def cost_first_layer_raw_func(self):
        self.cost_first_layer_raw = self.raw_paper_cost_after_counting * self.squaring * self.first_layer / 1000 / 1000
        return self.cost_first_layer_raw

    def cost_second_layer_raw_func(self):
        self.cost_second_layer_raw = self.raw_paper_cost_after_counting * self.weight_second_layer / 1000
        return self.cost_second_layer_raw

    def cost_third_layer_raw_func(self):
        self.cost_third_layer_raw = self.raw_paper_cost_after_counting * self.weight_third_layer / 1000
        return self.cost_third_layer_raw

    def bottom_squaring_func(self):
        self.bottom_squaring = (self.p_width - 10) * (self.p_bottom - 10) / 1000000
        return self.bottom_squaring

    def bottom_weight_func(self):
        self.bottom_weight = self.bottom_squaring * self.bottom_raw_gram / 1000
        return self.bottom_weight

    def bottom_cost_func(self):
        self.bottom_cost = self.raw_paper_cost * self.bottom_weight / 1000
        return self.bottom_cost

    def raw_package_cost_after_counting_func(self):
        self.raw_paper_cost_after_counting = self.cost_first_layer_raw + self.cost_second_layer_raw \
                                             + self.cost_third_layer_raw + self.paint_cost_uah
        return self.raw_paper_cost_after_counting

    def cost_for_customer_func(self):
        self.cost_for_customer = self.self_cost_package + self.margin_sum
        return self.cost_for_customer

    def paint_cost_one_gram_func(self):
        self.paint_cost_one_gram = self.paint_cost / 1000
        return self.paint_cost_one_gram

    def painting_cost_func(self):
        self.painting_cost = self.paint_spend * self.paint_cost / 1000
        return self.painting_cost

    def workpiece_area_func(self):
        self.workpiece_area = self.squaring * self.shading_percentages / 100
        return self.workpiece_area

    def paint_cost_eur_func(self):
        self.paint_cost_eur = self.workpiece_area * self.painting_cost
        return self.paint_cost_eur

    def paint_cost_uah_func(self):
        self.paint_cost_uah = (self.paint_cost_eur * self.exchange_rate_eur).__round__(3)
        return self.paint_cost_uah

    def self_cost_package_func(self):
        self.self_cost_package = self.paint_cost_uah + self.cost_first_layer_raw + self.cost_second_layer_raw + \
                                 self.cost_third_layer_raw + self.handle + self.bottom_cost
        return self.self_cost_package

    def margin_sum_func(self):
        self.margin_sum = self.self_cost_package * (self.margin / 100)
        return self.margin_sum

    def order_price_func(self):
        self.order_price = self.cost_for_customer * self.order_amount
        return self.order_price

    def currency_func(self):
        if self.currency == "UAH":
            self.raw_paper_cost_after_counting = self.raw_paper_cost
            return self.raw_paper_cost_after_counting
        elif self.currency == "USD":
            self.raw_paper_cost_after_counting = self.raw_paper_cost * self.exchange_rate_usd
            return self.raw_paper_cost_after_counting
        elif self.currency == "EUR":
            self.raw_paper_cost_after_counting = self.raw_paper_cost * self.exchange_rate_eur
            return self.raw_paper_cost_after_counting

    def reload_variables(self):
        self.currency_func()
        self.roll_format_func()
        self.sleeve_length_func()
        self.squaring_func()
        self.weight_first_layer_func()
        self.weight_second_layer_func()
        self.weight_third_layer_func()
        self.cost_first_layer_raw_func()
        self.cost_second_layer_raw_func()
        self.cost_third_layer_raw_func()
        self.bottom_squaring_func()
        self.bottom_weight_func()
        self.bottom_cost_func()
        self.raw_package_cost_after_counting_func()
        self.paint_cost_one_gram_func()
        self.painting_cost_func()
        self.workpiece_area_func()
        self.paint_cost_eur_func()
        self.paint_cost_uah_func()
        self.self_cost_package_func()
        self.margin_sum_func()
        self.cost_for_customer_func()
        self.order_price_func()

    def reset_func(self):
        lbl_text = {"name": "",
                    "width": ["Ширина", str(self.p_width), "мм"],
                    "height": ["Высота", str(self.p_height), "мм"],
                    "bottom": ["Дно", str(self.p_bottom), "мм"],
                    "roll_format": ["Формат рулона", str(self.roll_format), "мм"],
                    "sleeve_length": ["Длина рукава", str(int(self.sleeve_length)), "мм"],
                    "squaring": ["Квадратура", str(self.squaring.__round__(3)), "м2"],
                    "handle": ["Ручка", str(self.handle), "грн"],
                    "first_layer": ["Первый слой", str(self.first_layer), "г/м2"],
                    "second_layer": ["Второй слой", str(self.second_layer), "г/м2"],
                    "third_layer": ["Третий слой", str(self.third_layer), "г/м2"],
                    "weight_first_layer": ["Вес первого слоя", str(self.weight_first_layer.__round__(3)), "гр"],
                    "weight_second_layer": ["Вес второго слоя", str(self.weight_second_layer.__round__(3)), "гр"],
                    "weight_third_layer": ["Вес третьего слоя", str(self.weight_third_layer.__round__(3)), "гр"],
                    "bottom_squaring": ["Квадратура дна", str(self.bottom_squaring), "м2"],
                    "bottom_raw_gram": ["Граматура дна", str(self.bottom_raw_gram), "гр/м2"],
                    "bottom_weight": ["Вес дна", str(self.bottom_weight.__round__(3)), "гр"],
                    "raw_paper_cost": ["Стоимость сырья", str(self.raw_paper_cost), str(self.currency)],
                    "bottom_cost": ["Стоимость дна", str(self.bottom_cost), "грн"],
                    "exchange_rate_eur": ["Курс евро", str(self.exchange_rate_eur), "грн"],
                    "exchange_rate_usd": ["Курс доллар", str(self.exchange_rate_usd), "грн"],
                    "self_cost_package": ["Себестоимость пакета", str(self.self_cost_package), "грн"],
                    "margin": ["Наценка", str(self.margin), "%"],
                    "margin_sum": ["Сумма наценки", str(self.margin_sum), "грн"],
                    "cost_for_customer": ["Цена", str(self.cost_for_customer), "грн"],
                    "order_price": ["Сумма заказа", str(self.order_price), "грн"],
                    "order_amount": ["Количество", str(self.order_amount), "шт"],
                    "shading_percentages": ["Процент запечатки", str(self.shading_percentages), "%"],
                    "paint_spend": ["Расход краски", str(self.paint_spend), "гр"],
                    "paint_cost": ["Стоимость краски", str(self.paint_cost), "eur"],
                    "paint_cost_one_gram": ["Стоимость краски за гр", str(self.paint_cost_one_gram), "eur"],
                    "painting_cost": ["Цена печати за 1м2", str(self.painting_cost), "eur"],
                    "workpiece_area": ["Площадь печати", str(self.workpiece_area.__round__(3)), "м2"],
                    "paint_cost_eur": ["Цена печати в ЕВРО", str(self.paint_cost_eur.__round__(3)), "eur"],
                    "paint_cost_uah": ["Цена печати", str(self.paint_cost_uah.__round__(3)), "грн"],
                    "cost_first_layer_raw": ["Себестоимость первого слоя",
                                             str(self.cost_first_layer_raw.__round__(3)), "грн"],
                    "cost_second_layer_raw": ["Себестоимость второго слоя",
                                              str(self.cost_second_layer_raw.__round__(3)), "грн"],
                    "cost_third_layer_raw": ["Себестоимость третьего слоя",
                                             str(self.cost_third_layer_raw.__round__(3)), "грн"],
                    }
        return lbl_text


class MaxPackJson:
    def write(self, new_dict):
        with open("maxpack_db.json", "w", encoding="utf-8") as file:
            json.dump(new_dict, file, ensure_ascii=True, indent=2)

    def read(self):
        with open("maxpack_db.json", "r", encoding="utf-8") as file:
            return json.load(file)
