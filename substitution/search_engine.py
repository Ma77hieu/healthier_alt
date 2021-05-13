from models import Product, Categories


class Substitutes():
    def __init__(self):
        #     self.ids = find_alt(user_input)
        pass

    def find_alt(self, searched_product):
        list_searched_words = self.isolate_words(searched_products)
        words_to_compare = self.trim(list_searched_words)
        searched_product_id = self.find_prod(words_to_compare)
        prod_infos = self.get_prod_infos(searched_product_id)
        subs_id = self.get_subs_id(prod_infos.cat_name, prod_infos.nutriscore)
        return subs_id

    def isolate_words(self, input_string):
        """isolate different words from input"""
        self.all_searched_words = input_string.split()
        return self.all_searched_words

    def trim(self, input_words_list):
        """select all words >2 chars, place them in a list"""
        def to_be_trimmed(x):
            if len(x) < 3:
                return False
            else:
                return True
        self.trimmed_words_list = list(filter(to_be_trimmed, input_words_list))
        # print('the filtered words are:')
        # for word in trimmed_words_list:
        #     print(word)
        return self.trimmed_words_list

    def find_prod(self, words_list):
        """compare list of isolated words to each product names in DB,
        return the ID of mathcing product"""
        keep_search = True
        while keep_search:
            for word in words_list:
                match_product = Product.objects.filter(name__contains=word)
                if match_product:
                    self.searched_product_id = match_product.id
                    self.result_found = True
                    keep_search = False
            self.result_found = False
            keep_search = False
        return self.searched_product_id, self.result_found

    def get_prod_infos(self, found_product_id):
        """get category and nutriscore of matching product"""
        category = Categories.objects.filter(product_id=found_product_id)
        self.cat_name = category.name
        self.nutriscore = Product.objects.get(
            pk=found_product_id).values('nutrition_grade')
        return self.cat_name, self.nutriscore

    def get_subs_id(self, cat_name, nutriscore):
        """get IDs of all products from the same category with
        better nutriscore"""
        self.alts_id = Categories.objects.filter(name=cat_name).product_id
        return self.alts_id


if __name__ == "__main__":
    substitute = Substitutes()
    test_words_list = substitute.isolate_words("a DU saucisson Nutella 42")
    trimmed_words_list = substitute.trim(test_words_list)
    found_id = substitute.find_prod(trimmed_words_list).searched_product_id
