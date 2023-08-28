import time

from behave import *
from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.utilities.XLUtils import *
from features.pages.amazonPage import WebElements
from features.pages.config import EnvSettings
from features.pages.string_config import String
from features.utilities.screenshot import Screenshots

print("Hello...")
@given('Open URL : www.amazon.in')
def open_amazon_site(context):
    context.driver.get(EnvSettings.Amazon_page)
    context.driver.maximize_window()
    context.driver.implicitly_wait(40)


@when('Click on Signin')
def signin_to_site(context):
    message = WebElements.signin_button
    wait = WebDriverWait(context.driver, 10)
    url_check = wait.until(EC.visibility_of_element_located(message))
    assert String.signin_message == url_check.text, String.invalid_homepage_error_message


@then('I login with my Amazon credentials')
def sign_in_with_credentials(context):
    path = EnvSettings.Login_credential_file
    username = readData(path, EnvSettings.read_data_active_sheet, EnvSettings.read_row_no,
                        EnvSettings.read_column_no_one)
    password = readData(path, EnvSettings.read_data_active_sheet, EnvSettings.read_row_no,
                        EnvSettings.read_column_no_two)

    WebDriverWait(context.driver, 20).until(EC.element_to_be_clickable(WebElements.signin_field_one))
    signin_field = context.driver.find_element(By.ID, WebElements.signin_field_one[1])
    signin_field.click()

    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.username_field_one))
    username_field = context.driver.find_element(By.ID, WebElements.username_field_one[1])
    username_field.clear()
    username_field.send_keys(username)

    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.continue_button_one))
    continue_button = context.driver.find_element(By.ID, WebElements.continue_button_one[1])
    continue_button.click()

    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.password_field_one))
    password_field = context.driver.find_element(By.ID, WebElements.password_field_one[1])
    password_field.clear()
    password_field.send_keys(password)

    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.submit_button_one))
    submit_button = context.driver.find_element(By.ID, WebElements.submit_button_one[1])
    submit_button.click()


@then('I should be on the homepage')
def logged_in_successfully(context):
    message = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located(WebElements.welcome_message))

    message_one = String.greeting_message
    if message_one == message.text:
        writeData(EnvSettings.write_data, EnvSettings.write_to_sheet, String.summary_one, String.result_pass)
    else:
        writeData(EnvSettings.write_data, EnvSettings.write_to_sheet, String.summary_one, String.result_fail)

    assert message_one == message.text, String.login_success_message
    sc = Screenshots()
    sc.capture_screenshot(context.driver, EnvSettings.screenshot_path, name=String.screenshot_homepage)


@then('I click on the All icon in the middle of the web page with the search box')
def click_on_all_icon(context):
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located(WebElements.all_icon_one))
    all_icon = context.driver.find_element(By.CSS_SELECTOR, WebElements.all_icon_one[1])
    all_icon.click()


@then('I enter product name into the search box')
def step_impl_enter_text_into_search_box(context):
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located(WebElements.search_field))
    context.driver.find_element(By.CSS_SELECTOR, WebElements.search_field[1]).send_keys(EnvSettings.search_product)
    WebDriverWait(context.driver, 100).until(EC.visibility_of_all_elements_located(WebElements.click_item))
    products = context.driver.find_elements(By.CSS_SELECTOR, WebElements.click_item[1])
    for product in products:
        if product.text == EnvSettings.search_product:
            product.click()
            break
    else:
        assert False, String.assert_message_product_not_found


@then('I select required brand under the Brands section on the left scroll bar tab')
def step_impl_select_brand(context):
    WebDriverWait(context.driver, 10).until(EC.presence_of_all_elements_located(WebElements.Check_box))
    checkboxes = context.driver.find_elements(By.CSS_SELECTOR, WebElements.Check_box[1])
    brand_found = False
    for check in checkboxes:
        brand_name_element = check.find_element(By.XPATH, WebElements.product_name[1].format(EnvSettings.brand_name))
        if brand_name_element.text == EnvSettings.brand_name:
            brand_name_element.click()
            brand_found = True
            break
    assert brand_found, String.assert_message_brand_not_found


@then('I select the third product from the search results')
def select_third_product(context):
    WebDriverWait(context.driver, 60).until(EC.presence_of_all_elements_located(WebElements.select_product))

    search_results = context.driver.find_elements(By.CSS_SELECTOR, WebElements.select_product[1])
    if len(search_results) >= 3:
        try:
            product_to_select = search_results[2]
            context.product_identifier = product_to_select.get_attribute(WebElements.product_id)

            product_to_select.find_element(By.CSS_SELECTOR, WebElements.product_image[1]).click()
            context.open_window = context.driver.window_handles
            context.driver.switch_to.window(context.open_window[1])

        except ElementClickInterceptedException:
            print("Element click intercepted. Trying again...")

    else:
        raise Exception("Less than 3 search results found.")


@then('I ensure that the same product is not already added in the cart')
def verify_cart_impl(context):
    product_identifier = context.product_identifier
    WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable(WebElements.cart_icon_one))
    cart_icon = context.driver.find_element(By.ID, WebElements.cart_icon_one[1])
    cart_icon.click()
    cart_count = context.driver.find_element(By.ID, WebElements.cart_count_one[1])
    count = int(cart_count.text)

    if count == 0:
        context.product_check_flag = True

    elif count > 0:
        WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.cart_items_one))

        cart_items = context.driver.find_elements(By.XPATH, WebElements.cart_items_one[1])

        for item in cart_items:
            item_identifier = item.get_attribute(WebElements.product_id)
            if item_identifier == product_identifier:

                try:
                    quantity_dropdown = item.find_element(By.XPATH, WebElements.drop_down[1])
                    current_quantity = int(quantity_dropdown.text)

                    if current_quantity > 1:
                        dropdown = Select(item.find_element(By.ID, WebElements.drop_down_quantity[1]))
                        dropdown.select_by_visible_text("1")
                        context.product_check_flag = False
                        current_quantity = 1
                    elif current_quantity == 1:
                        context.product_check_flag = False
                        current_quantity = 1
                    context.quantity = current_quantity
                except Exception as e:
                    print("Could not update the quantity or remove the duplicate product from the cart:", repr(e))
            else:
                context.product_check_flag = True
                context.quantity = 1
                break


@then('I click on "Add to Cart"')
def add_to_cart(context):
    if context.product_check_flag:

        product_identifier = context.product_identifier

        try:
            cart_count_element = WebDriverWait(context.driver, 30).until(
                EC.visibility_of_element_located(WebElements.cart_count_one))
            initial_cart_count = int(cart_count_element.text)
            print(initial_cart_count)
            context.driver.back()
            add_to_cart_button = WebDriverWait(context.driver, 20).until(
                EC.element_to_be_clickable(WebElements.cart_button))

            add_to_cart_button.click()
            view_cart_button = WebDriverWait(context.driver, 60).until(EC.element_to_be_clickable(
                WebElements.view_cart))
            view_cart_button.click()

            updated_cart_count_element = context.driver.find_element(By.ID, WebElements.cart_count_one[1])
            updated_cart_count = int(updated_cart_count_element.text)
            print("updated cart count:", updated_cart_count)
            if updated_cart_count > initial_cart_count:
                context.product_added_to_cart = True
                context.quantity = 1
            else:
                print("Expected cart count:", initial_cart_count + 1)
                print("Actual cart count:", updated_cart_count)
                context.product_added_to_cart = False
        except Exception as e:
            print(repr(e))
    else:
        print("There is error in adding product not entering to if  ")


@then('only a single product should be added to the cart')
def verify_single_product_added(context):
    if context.quantity == 1:
        context.product_added_to_cart = True
    else:
        try:
            verify_cart_impl(context)
            context.product_added_to_cart = True
        except:
            raise Exception("multiple products in cart verify cart functionality is not working correctly")


@then('I click on "Proceed to Checkout"')
def proceed_to_checkout(context):
    if context.product_added_to_cart:

        WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.cart_items_one))

        product_identifier = context.product_identifier
        cart_items = context.driver.find_elements(By.XPATH, WebElements.cart_items_one[1])

        items_to_remove = []

        for item in cart_items:
            item_identifier = item.get_attribute(WebElements.product_id)
            if item_identifier != product_identifier:
                items_to_remove.append(item_identifier)
            else:
                pass
        print(items_to_remove)

        for item_identifier in items_to_remove:
            try:
                delete_button_locator = (By.XPATH, WebElements.delete_button_xpath.format(item_identifier))
                delete_button = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable(delete_button_locator))
                delete_button.click()

                context.driver.refresh()
            except NoSuchElementException:
                print("This is the product we want to keep:", item_identifier)
                context.driver.refresh()

        WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.cart_items_one))
        context.driver.refresh()
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located(WebElements.checkout_one))
        checkout = context.driver.find_element(By.CSS_SELECTOR, WebElements.checkout_one[1])
        checkout.click()


    else:
        raise Exception("It is not entering to if block")

    sc = Screenshots()
    sc.capture_screenshot(context.driver, EnvSettings.screenshot_path, name=String.screenshot_after_checkout)


@then('I should be taken to the checkout page for further steps in the purchase process')
def further_steps(context):
    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located(WebElements.place_order))
    address = context.driver.find_element(By.CSS_SELECTOR, WebElements.place_order[1])
    address.click()
    sc = Screenshots()
    sc.capture_screenshot(context.driver, EnvSettings.screenshot_path, name=String.screenshot_before_payment)
