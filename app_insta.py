from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
import wget
import time

driver = webdriver.Chrome()
driver.get('https://www.instagram.com/')

username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'username']"))
    )
password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'password']"))
    )

print("\n---------- WELCOME TO INSTAGRAM FOLLOWER LIST ENGINE ----------")
print("                      by Suren Fernando                             \n")
# print('In order to extract your followers or following list please login. \n')
# print('In order to check one anyone\'s following or followers list you need to login.\n')
print("LOGIN TO INSTAGRAM")
input_username = input("Username: ").strip()
input_password = input("Password: ").strip()

username.clear()
password.clear()
username.send_keys(input_username)
password.send_keys(input_password)

# CLICK LOGIN - AFTER THE CREDENTIALS ARE ENTERED
log_in = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type = 'submit']"))
    )
log_in.click()

# POP UP RESPONSE TO NOT SAVE PASSWORD
not_now = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
    )
not_now.click()

# POP UP RESPONSE TO NOT SEND NOTIFICATION
not_now2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
    )
not_now2.click()

# Ask user option, Personal data or Custom search a user.
goAgain = True
while goAgain:
    print("\nWould you like a third party account's following data or your personal data?")
    search_option = input("Choose an option:  (A) Thirdparty Account        (B) Personal Account \n")

    following_list = []
    followers_list = []
    if search_option.lower() == 'b':
        # # Go to host account, profile page directly.
        driver.get(f'https://www.instagram.com/{input_username}/')

        # Extract follower and following count (used for loop to pick users)
        following_count = int(WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{input_username}/following/']/span"))
        ).text.replace(',', ''))

        followers_count = int(WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{input_username}/followers/']/span"))
        ).text.replace(',', ''))

        print('Connecting to designated user data...')
        # Search the FOLLOWING element using XPATH
        following = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{input_username}/following/']"))
        )
        following.click()

        following_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']"))
        )
        # Extract the list of Following while scrolling till the end of file.

        for x in range(1, following_count+1):
            try:
                if x % 10 == 0:
                    driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", following_div
                    )

                person = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[@class='PZuss']/li[{x}]"))
                    ).text
                person = person.split('\n')[0]
                following_list.append(person)
            except TimeoutException:
                # print(f"We had to stop at {x}, list so far:")
                break

        print("Extraction of Following data is done. ")

        close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='WaOAr']//button[@type='button']"))
            )
        close_button.click()

        # CHECK THE FOLLOWERS
        follower = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{input_username}/followers/']"))
        )
        follower.click()

        follower_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']"))
        )

        # Extract the list of Followers while scrolling till the end of file.
        for x in range(1, followers_count+1):
            if x == followers_count//2:
                print('A few more minutes...')
            try:
                if x % 10 == 0:
                    driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", follower_div
                    )

                person = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@class='PZuss']/li[{x}]"))
                ).text
                person = person.split('\n')[0]
                followers_list.append(person)
            except TimeoutException:
                # print(f"We had to stop at {x}, list so far:")
                break

    elif search_option.lower() == 'a':
        third_party_username = input("Input the account name you want to search: ").strip()
        # Go to third party account, profile page directly.
        driver.get(f'https://www.instagram.com/{third_party_username}/')

        # Extract follower and following count (used for loop to pick users)
        following_count = int(WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{third_party_username}/following/']/span"))
        ).text.replace(',', ''))

        followers_count = int(WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{third_party_username}/followers/']/span"))
        ).text.replace(',', ''))

        # Search the FOLLOWING element using XPATH
        following = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{third_party_username}/following/']"))
        )
        following.click()

        print('Connecting to designated user data...')
        following_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']"))
        )

        # Extract the list of Following while scrolling till the end of file.
        for x in range(1, following_count + 1):
            try:
                if x % 10 == 0:
                    driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", following_div
                    )

                person = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@class='PZuss']/li[{x}]"))
                ).text
                person = person.split('\n')[0]
                following_list.append(person)
            except TimeoutException:
                # print(f"We had to stop at {x}, list so far:")
                break

        print("Extraction of Following data is done. ")

        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='WaOAr']//button[@type='button']"))
        )
        close_button.click()

        # CHECK THE FOLLOWERS
        follower = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{third_party_username}/followers/']"))
        )
        follower.click()

        follower_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']"))
        )

        # Extract the list of Followers while scrolling till the end of file.

        for x in range(1, followers_count + 1):
            if x == followers_count // 2:
                print('A few more minutes...')
            try:
                if x % 10 == 0:
                    driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", follower_div
                    )

                person = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@class='PZuss']/li[{x}]"))
                ).text
                person = person.split('\n')[0]
                followers_list.append(person)
            except TimeoutException:
                # print(f"We had to stop at {x}, list so far:")
                break

    not_following_back = []
    for user in following_list:
        if user not in followers_list:
            not_following_back.append(user)

    not_following_count = len(not_following_back)

    # OUTPUT DATA
    print('--------------------- STATISTICS ---------------------')
    print(f'The account is following {following_count} accounts')
    print(f'The account has {followers_count} followers')
    print(f'\n{not_following_count} accounts are not following you back')
    print(f'Feel free to unfollow these peasants:\n')
    for peasant in not_following_back:
        print(peasant)

    retry = input(f'\nWould you like to try a different search option? Y/N')
    if retry.lower() != 'y':
        time.sleep(2)
        driver.quit()
        goAgain = False



