from django.test import TestCase
# from substitution.models import User, Categories, Product
from substitution.search_engine import Substitutes
# from decouple import config
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from substitution.constants import NO_PROD_FOUND, WAIT_TIME
import time
# from mock import Mock

# Create your tests here.


class searchEngineTests(TestCase):
    fixtures = ['substitution.json']
    substitute = Substitutes()
    specific_charac_string = "aaeeee  uu"
    assertion_list = ['a', 'DU', 'saucisson', 'Nutella', '42']
    assertion_trimmed_words_list = [
        'saucisson', 'Nutella']
    assertion_trimmed_words_list_2 = [
        'iubiube', 'Abricot']
    assertion_trimmed_words_list_3 = [
        'iubiube', 'iqzerubgilteub', 'haej', 'k,ufipoaqerg']

    def test_replace_spec_characs(self):
        normalized_string = self.substitute.replace_spec_characs(
            "àaéeèe' ùu")
        self.assertEqual(normalized_string, self.specific_charac_string)

    def test_isolate_words(self):
        test_words_list = self.substitute.isolate_words(
            "a DU saucisson Nutella 42")
        self.assertEqual(test_words_list, self.assertion_list)

    def test_trim(self):
        trimmed_words_list = self.substitute.trim(self.assertion_list)
        self.assertEqual(trimmed_words_list, self.assertion_trimmed_words_list)

    def test_find_prod_Nutella(self):
        self.substitute.find_prod(self.assertion_trimmed_words_list)
        prod_id_1 = self.substitute.searched_product_id
        is_prod_found_1 = self.substitute.result_found
        self.assertEqual(prod_id_1, 127)
        self.assertEqual(is_prod_found_1, True)

    def test_find_prod_Abricot(self):
        self.substitute.find_prod(self.assertion_trimmed_words_list_2)
        prod_id_2 = self.substitute.searched_product_id
        is_prod_found_2 = self.substitute.result_found
        self.assertEqual(prod_id_2, 105)
        self.assertEqual(is_prod_found_2, True)

    def test_find_prod_FAIL(self):
        self.substitute.find_prod(self.assertion_trimmed_words_list_3)
        prod_id_3 = self.substitute.searched_product_id
        is_prod_found_3 = self.substitute.result_found
        self.assertEqual(prod_id_3, '-1')
        self.assertEqual(is_prod_found_3, False)

    def test_get_prod_infos(self):
        self.substitute.get_prod_infos(125)
        cat = self.substitute.cat_name
        nutri = self.substitute.nutriscore
        self.assertEqual(cat, 'Snacks')
        self.assertEqual(nutri, 'd')

    def test_get_prod_id_from_cat(self):
        self.substitute.get_prod_id_from_cat('Snacks')
        ids = self.substitute.ids_prod_from_cat
        self.assertEqual(
            ids, [125, 126, 127, 128, 129, 130, 131, 132, 133, 134])

    def test_get_alt_ids(self):
        self.substitute.get_alt_ids(
            'd', [125, 126, 127, 128, 129, 130, 131, 132, 133, 134])
        alts = self.substitute.ids_alts
        self.assertEqual(alts, [125, 126, 129, 130, 131, 132])

    def test_global_search_engine(self):
        global_alt_ids = self.substitute.find_alt(
            "Un truc avec de l Abricot")
        print("global: {}".format(global_alt_ids))
        self.assertEqual(global_alt_ids, (
                         [105, 106, 109, 110, 112], True))


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['substitution.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_prod_found(self):
        timeout = 2
        searched_prod_displayed = False
        name_of_match_prod_displayed = False
        is_product_card = False
        is_ok = [searched_prod_displayed,
                 name_of_match_prod_displayed,
                 is_product_card]
        to_check = ["trucs à l'abricot",
                    "Muesli Raisin, Figue, Abricot", "nutriscore"]
        for both_search_input in [0, 1]:
            self.selenium.get('{}'.format(self.live_server_url + '/home'))
            if both_search_input == 0:
                collapsed_navbar_button = self.selenium.find_element_by_class_name(
                    "navbar-toggler-icon")
                collapsed_navbar_button.click()
            searchbar = self.selenium.find_elements_by_name("searched_product")[
                both_search_input]
            searchbar.send_keys("trucs à l'abricot")
            searchbar.send_keys(Keys.RETURN)
            WebDriverWait(self.selenium, timeout).until(
                lambda driver: driver.find_element_by_tag_name('body'))
            time.sleep(WAIT_TIME)
            for elem in to_check:
                if elem in self.selenium.page_source:
                    is_ok[to_check.index(elem)] = True
            assert is_ok == [True, True, True]

    def test_prod_NOT_found(self):
        timeout = 2
        searched_prod = "izaubfreub"
        for both_search_input in [0, 1]:
            self.selenium.get('{}'.format(self.live_server_url + '/home'))
            if both_search_input == 0:
                collapsed_navbar_button = self.selenium.find_element_by_class_name(
                    "navbar-toggler-icon")
                collapsed_navbar_button.click()
            searchbar = self.selenium.find_elements_by_name("searched_product")[
                both_search_input]
            searchbar.send_keys(searched_prod)
            searchbar.send_keys(Keys.RETURN)
            WebDriverWait(self.selenium, timeout).until(
                lambda driver: driver.find_element_by_tag_name('body'))
            no_prod_found = False
            time.sleep(WAIT_TIME)
            if NO_PROD_FOUND in self.selenium.page_source:
                no_prod_found = True
            assert no_prod_found is True
