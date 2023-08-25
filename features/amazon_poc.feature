Feature: Amazon project

  Scenario:Login to Amazon and purchase product
    Given Open URL : www.amazon.in
    When Click on Signin
    Then I login with my Amazon credentials
    And I should be on the homepage
    And I click on the All icon in the middle of the web page with the search box
    And I enter product name into the search box
    And I select required brand under the Brands section on the left scroll bar tab
    And I select the third product from the search results
    And I ensure that the same product is not already added in the cart
    And I click on "Add to Cart"
    And only a single product should be added to the cart
    And I click on "Proceed to Checkout"
    And I should be taken to the checkout page for further steps in the purchase process
