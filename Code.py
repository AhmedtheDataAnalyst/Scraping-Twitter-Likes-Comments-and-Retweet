import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt 

login_url = 'https://twitter.com/login'

chrome_driver_path = r"C:/Users/MU67197/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

driver.get(login_url)

time.sleep(5)

username = driver.find_element(By.NAME, 'text')
username.send_keys('Your_Username') 

username.send_keys(Keys.RETURN)

time.sleep(3)

password = driver.find_element(By.NAME, 'password')
password.send_keys('Your_Password') 

password.send_keys(Keys.RETURN)

time.sleep(5)

search_box = driver.find_element(By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')
search_query = "Petroleum Development Oman"
search_box.send_keys(search_query)

search_box.send_keys(Keys.RETURN)

time.sleep(5)

def is_numeric(value):
    try:
        int(value.replace(',', ''))
        return True
    except ValueError:
        return False

last_height = driver.execute_script("return document.body.scrollHeight")

total_posts = 0
total_likes = 0
total_retweets = 0
total_comments = 0

while True:
    tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    total_posts += len(tweets)

    for tweet in tweets:
        try:
            spans = tweet.find_elements(By.XPATH, './/span[contains(@class, "r-poiln3")]')

            valid_spans = [span.text for span in spans if is_numeric(span.text)]

            if len(valid_spans) >= 3:
                comments_count = int(valid_spans[0].replace(',', ''))
                retweets_count = int(valid_spans[1].replace(',', ''))
                likes_count = int(valid_spans[2].replace(',', ''))

                total_likes += likes_count
                total_retweets += retweets_count
                total_comments += comments_count
            else:
                print("Not enough valid numeric span elements to extract likes, retweets, and comments.")
        
        except Exception as e:
            print(f"Error processing tweet: {e}")


    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        print("Reached the end of the page.")
        break

    last_height = new_height

print(f"Total Posts: {total_posts}")
print(f"Total Likes: {total_likes}")
print(f"Total Retweets: {total_retweets}")
print(f"Total Comments: {total_comments}")


driver.quit()

categories = ['Total Posts', 'Total Likes', 'Total Retweets', 'Total Comments']
values = [total_posts, total_likes, total_retweets, total_comments]

plt.figure(figsize=(8, 6))
plt.bar(categories, values, color='skyblue')

plt.xlabel('Metrics')
plt.ylabel('Count')
plt.title('Twitter Data for "Petroleum Development Oman"')

plt.show()