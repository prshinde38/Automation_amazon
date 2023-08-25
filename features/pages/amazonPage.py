from selenium.webdriver.common.by import By


class WebElements:
    signin_button = [By.CSS_SELECTOR, '#nav-link-accountList-nav-line-1']
    signin_field_one = [By.ID, 'nav-signin-tooltip']
    username_field_one = [By.ID, 'ap_email']
    continue_button_one = [By.ID, 'continue']
    password_field_one = [By.ID, 'ap_password']
    submit_button_one = [By.ID, 'signInSubmit']
    welcome_message = [By.ID, "nav-link-accountList-nav-line-1"]
    all_icon_one = [By.CSS_SELECTOR, ".nav-search-scope"]
    search_field = [By.CSS_SELECTOR, "#twotabsearchtextbox"]
    click_item = [By.CSS_SELECTOR, ".s-suggestion-container"]
    Check_box = [By.CSS_SELECTOR, ".a-icon"]
    product_name = [By.XPATH, "//span[text()='{}']"]
    submit_button = [By.ID, 'nav-search-submit-button']
    select_product = [By.CSS_SELECTOR, ".s-asin"]
    product_id = "data-asin"
    product_image = [By.CSS_SELECTOR, ".s-image"]
    cart_icon_one = [By.ID, "nav-cart"]
    cart_count_one = [By.ID, "nav-cart-count"]
    cart_items_one = [By.XPATH, "//div[@data-asin]"]
    drop_down = [By.XPATH, ".//span[@class='a-dropdown-prompt']"]
    drop_down_quantity = [By.ID, "quantity"]
    cart_button = [By.ID, "add-to-cart-button"]
    title = "title"
    checkout_one = [By.CSS_SELECTOR, "#desktop-ptc-button-celWidget"]
    delete_button_xpath = "//div[@data-asin='{}']//input[@value='Delete']"
    view_cart = [By.CSS_SELECTOR, "input[aria-labelledby='attach-sidesheet-view-cart-button-announce']"]
    place_order = [By.CSS_SELECTOR, "#orderSummaryPrimaryActionBtn"]

