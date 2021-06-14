from django.test import TestCase
from substitution.search_engine import Substitutes
from decouple import config
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from substitution.constants import NO_PROD_FOUND, WAIT_TIME
import time


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
        """test the replace_spec_characs function of search_engine.py"""
        normalized_string = self.substitute.replace_spec_characs(
            "àaéeèe' ùu")
        self.assertEqual(normalized_string, self.specific_charac_string)

    def test_isolate_words(self):
        """test the isolate_words function of search_engine.py"""
        test_words_list = self.substitute.isolate_words(
            "a DU saucisson Nutella 42")
        self.assertEqual(test_words_list, self.assertion_list)

    def test_trim(self):
        """test the trim function of search_engine.py"""
        trimmed_words_list = self.substitute.trim(self.assertion_list)
        self.assertEqual(trimmed_words_list, self.assertion_trimmed_words_list)

    def test_find_prod_Nutella(self):
        """test the find_prod function of
        search_engine.py with "Nutella" input"""
        self.substitute.find_prod(self.assertion_trimmed_words_list)
        prod_id_1 = self.substitute.searched_product_id
        is_prod_found_1 = self.substitute.result_found
        self.assertEqual(prod_id_1, 127)
        self.assertEqual(is_prod_found_1, True)

    def test_find_prod_Abricot(self):
        """test the replace_spec_characs function with "Abricot" input"""
        self.substitute.find_prod(self.assertion_trimmed_words_list_2)
        prod_id_2 = self.substitute.searched_product_id
        is_prod_found_2 = self.substitute.result_found
        self.assertEqual(prod_id_2, 105)
        self.assertEqual(is_prod_found_2, True)

    def test_find_prod_FAIL(self):
        """test the 'no product found' scenario of
        the find_prod function of search_engine.py"""
        self.substitute.find_prod(self.assertion_trimmed_words_list_3)
        prod_id_3 = self.substitute.searched_product_id
        is_prod_found_3 = self.substitute.result_found
        self.assertEqual(prod_id_3, '-1')
        self.assertEqual(is_prod_found_3, False)

    def test_get_prod_infos(self):
        """test the get-prod_infos function of search_engine.py"""
        self.substitute.get_prod_infos(125)
        cat = self.substitute.cat_name
        nutri = self.substitute.nutriscore
        self.assertEqual(cat, 'Snacks')
        self.assertEqual(nutri, 'd')

    def test_get_prod_id_from_cat(self):
        """test the get_prod_id_from_cat
         function of search_engine.py"""
        self.substitute.get_prod_id_from_cat('Snacks')
        ids = self.substitute.ids_prod_from_cat
        self.assertEqual(
            ids, [125, 126, 127, 128, 129, 130, 131, 132, 133, 134])

    def test_get_alt_ids(self):
        """test the get_alt_ids function of search_engine.py"""
        self.substitute.get_alt_ids(
            'd', [125, 126, 127, 128, 129, 130, 131, 132, 133, 134])
        alts = self.substitute.ids_alts
        self.assertEqual(alts, [125, 126, 129, 130, 131, 132])

    def test_global_search_engine(self):
        """test the global 'find_alt' function of search_engine.py"""
        global_alt_ids = self.substitute.find_alt(
            "Un truc avec de l Abricot")
        print("global: {}".format(global_alt_ids))
        self.assertEqual(global_alt_ids, (
                         [105, 106, 109, 110, 112], True))


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['substitution.json', 'users.json', 'favs.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def user_login(self, NO_ALT=False):
        """
        will be used by various tests to mimic the user login

        :Args:
         - NO_ALT: False by default, connects a user WITH
         saved alternative products
         True if we want to connect a user WITHOUT
         alternatives product saved.

        """
        self.selenium.get('{}'.format(self.live_server_url + '/signin'))
        if NO_ALT is False:
            LOGIN = config('USER_LOGIN')
            PWD = config('USER_PWD')
        elif NO_ALT is True:
            LOGIN = config('NO_ALT_USER_LOGIN')
            PWD = config('NO_ALT_USER_PWD')
        username_input = self.selenium.find_elements_by_name("username")[0]
        username_input.send_keys(LOGIN)
        password_input = self.selenium.find_elements_by_name("password")[0]
        password_input.send_keys(PWD)
        password_input.send_keys(Keys.RETURN)

    def user_login_no_alt(self):

        self.selenium.get('{}'.format(self.live_server_url + '/signin'))
        username_input = self.selenium.find_elements_by_name("username")[0]
        username_input.send_keys(config('NO_ALT_USER_LOGIN'))
        password_input = self.selenium.find_elements_by_name("password")[0]
        password_input.send_keys(config('No_ALT_USER_PWD'))
        password_input.send_keys(Keys.RETURN)

    def product_search_successfull(self):
        """will be used by various tests to mimic a successfull
        product search"""
        self.selenium.get('{}'.format(self.live_server_url + '/home'))
        searchbar = self.selenium.find_elements_by_name("searched_product")[1]
        searchbar.send_keys("trucs à l'abricot")
        searchbar.send_keys(Keys.RETURN)

    def test_prod_found(self):
        """tests the two searchbars (header + body) of the homepage
        scenario where a product is found"""
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
                collapsed_navbar_button = (
                    self.selenium.find_element_by_class_name(
                        "navbar-toggler-icon"))
                collapsed_navbar_button.click()
            searchbar = (
                self.selenium.find_elements_by_name("searched_product")
                [both_search_input])
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
        """tests the two searchbars (header + body) of the homepage
        scenario where a product is NOT found"""
        timeout = 2
        searched_prod = "izaubfreub"
        for both_search_input in [0, 1]:
            self.selenium.get('{}'.format(self.live_server_url + '/home'))
            if both_search_input == 0:
                collapsed_navbar_button = (
                    self.selenium.find_element_by_class_name(
                        "navbar-toggler-icon"))
                collapsed_navbar_button.click()
            searchbar = (
                self.selenium.find_elements_by_name("searched_product")[
                    both_search_input])
            searchbar.send_keys(searched_prod)
            searchbar.send_keys(Keys.RETURN)
            WebDriverWait(self.selenium, timeout).until(
                lambda driver: driver.find_element_by_tag_name('body'))
            no_prod_found = False
            time.sleep(WAIT_TIME)
            if NO_PROD_FOUND in self.selenium.page_source:
                no_prod_found = True
            assert no_prod_found is True

    def test_save_alt_anonymous_user(self):
        """tests the alternative product save function
        scenario where user IS NOT logged in and CANNOT
        therefore save alternatives"""
        timeout = 2
        self.product_search_successfull()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        warning = False
        possible_save = False
        warning_message = ("Vous devez vous identifier "
                           "pour pouvoir enregistrer")
        save_link = ">Sauvegarder</span>"
        time.sleep(WAIT_TIME)
        if warning_message in self.selenium.page_source:
            warning = True
            if save_link in self.selenium.page_source:
                possible_save = True
        assert [warning, possible_save] == [True, False]

    def test_save_alt_logged_user(self):
        """tests the alternative product save function
        scenario where user IS logged in and CAN
        therefore save alternatives"""
        timeout = 2
        self.user_login()
        self.product_search_successfull()
        save_prod_button = self.selenium.find_element_by_name(
            "save_prod_button")
        save_prod_button.click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        time.sleep(WAIT_TIME)
        prod_saved = False
        saved_prod_message = "Produit enregistré dans vos favoris"
        if saved_prod_message in self.selenium.page_source:
            prod_saved = True
        assert prod_saved is True

    def test_prod_details_page(self):
        """tests the display of the various informations in the
        product details page"""
        timeout = 2
        self.selenium.get('{}'.format(
            self.live_server_url + '/details/109'))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        searched_prod_displayed = False
        nutriscore_displayed = False
        fat_value_displayed = False
        is_ok = [searched_prod_displayed,
                 nutriscore_displayed,
                 fat_value_displayed]
        to_check = ["Flocons d'avoine compl",
                    "a selected", "gras (g) : 7.1"]
        for elem in to_check:
            if elem in self.selenium.page_source:
                is_ok[to_check.index(elem)] = True
        assert is_ok == [True, True, True]

    def test_link_prod_details_page(self):
        """tests the redirection to an open
        food fact product info page"""
        timeout = 2
        self.selenium.get('{}'.format(self.live_server_url +
                                      '/details/109'))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        OFF_link_button = self.selenium.find_element_by_name(
            "OFF_link_button")
        OFF_link_button.click()
        time.sleep(WAIT_TIME)
        self.selenium.switch_to_window(self.selenium.window_handles[1])
        product_name = "flocons d'avoine - Bjorg - 500g"
        link_OK = False
        if product_name == (
                self.selenium.find_element_by_tag_name('h1').text):
            link_OK = True
        assert link_OK is True

    def test_view_alt_no_alt_saved(self):
        """tests the viewing of saved alts for a user
        that doessn't have any alts"""
        self.user_login(True)
        timeout = 2
        self.selenium.get('{}'.format(self.live_server_url +
                                      '/mesaliments'))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        time.sleep(WAIT_TIME)
        alert_message_displayed = False
        alert_message = "Vous n'avez pas enregistré d'alternative"
        if alert_message in self.selenium.page_source:
            alert_message_displayed = True
        assert alert_message_displayed is True

    def test_view_alt_OK(self):
        """tests the viewing of saved alts for a user
        that have previously saved some"""
        self.user_login()
        timeout = 2
        self.selenium.get('{}'.format(self.live_server_url +
                                      '/mesaliments'))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        time.sleep(WAIT_TIME)
        product_displayed = False
        product_card = self.selenium.find_element_by_name("product_card")
        if product_card is not None:
            product_displayed = True
        assert product_displayed is True

    def test_redirect_home(self):
        """tests the redirection to the homepage from the legal page"""
        self.user_login()
        timeout = 2
        self.selenium.get('{}'.format(self.live_server_url + '/legal'))
        self.selenium.find_element_by_name("name_and_logo").click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        time.sleep(WAIT_TIME)
        redirection = False
        title_homepage = "du gras, oui, mais de qualité!"
        h1 = self.selenium.find_element_by_tag_name('h1').text.lower()
        print("h1: {}".format(h1))
        if h1 == title_homepage:
            redirection = True
        assert redirection is True
