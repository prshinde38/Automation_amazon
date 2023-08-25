Feature: Amazon demo project

  Background: Verify Amazon Login
    Given Open URL: www.amazon.in
    When Click on Signin
    Then I login with my Amazon credentials
    And I should be on the homepage

  Scenario: Verify Product Search and Selection

    And I click on the All icon in the middle of the web page with the search box
    And I enter "Headphones wireless" in the search box
    And I select "boAT" under the Brands section in the left scroll bar tab
    And I select the third product from the search results

  Scenario: Verify Adding Product to Cart

    And I click on the All icon in the middle of the web page with the search box
    And I enter "Headphones wireless" in the search box
    And I select "boAT" under the Brands section in the left scroll bar tab
    And I select the third product from the search results
    And I ensure that the same product is not already added in the cart
    And I click on "Add to Cart"
    And only a single product should be added to the cart

  Scenario: Verify Proceed to Checkout

    And I click on "Add to Cart"
    And only a single product should be added to the cart
    And I click on "Proceed to Checkout"
    And I should be taken to the checkout page for further steps in the purchase process
