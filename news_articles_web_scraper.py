import os
import time

#SELENIUM IMPORTS
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

#WebDriverWait IMPORTS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#TKINTER IMPORTS
import tkinter as tk    
from tkinter import ttk    
from tkinter import *

def open_article(article_url):
    
    #CREATE WEBDRIVER
    PATH = os.path.dirname(os.path.realpath(__file__)) + '\chromedriver.exe'    #Chrome version 88 ChromeDriver 88.0.4324.96
    driver = webdriver.Chrome(PATH)
    driver.get(article_url) #open browser and tab + visist link

    #ACCEPT COOKIES
    accept_cookies = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(( By.ID, 'didomi-notice-agree-button'))).click()


def search(search_word_input, root):
    #CREATE WEBDRIVER
    PATH = os.path.dirname(os.path.realpath(__file__)) + '\chromedriver.exe'    #Chrome version 88 ChromeDriver 88.0.4324.96
    driver = webdriver.Chrome(PATH)
    driver.set_window_position(-10000,0)   #hide browser window
    driver.get('https://www.hbvl.be/') #open browser and tab + visist link

    #ACCEPT COOKIES
    accept_cookies = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(( By.ID, 'didomi-notice-agree-button'))).click()

    #SEARCHBOX ITEM SELECTEREN & KLIKKEN
    searchbox_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(( By.XPATH, "//*[@class='has-icon-state']"))).click()

    #SEARCHBOX SELECTEREN
    searchbox = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[class='form-input']")))

    #SEARCHBOX INVULLEN
    searchbox.clear() #empty input
    keyword = search_word_input
    searchbox.send_keys(keyword) #text in inputfield

    #CLICK THE SEARCHBUTTON
    searchButton = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[class='button button--alpha']"))).click()
    
    #GET ARTICLES
    driver.execute_script("window.scrollTo(0,4000);") #start scrolling (4 times length of screen )
    
    #GET ARTICLES URL
    articles = driver.find_elements_by_tag_name('a')  #get articles classname
    articles = [article for article in articles if article.get_attribute('data-testid') == "article-teaser"] #so you only get the links of the articles
    articles_url = [article.get_attribute('data-vr-contentbox-url') for article in articles] #get the url

    #GET ARTICLES TITEL
    articles = driver.find_elements_by_tag_name('h1') #get articles classname
    articles_titels = [article.text for article in articles] #turn the article tags into links
    
    #CREATE ARTICLE WINDOW
    article_window = Tk()    
    article_window.title(search_word_input)

    #ICON
    PATH = os.path.dirname(os.path.realpath(__file__)) + '\\newspaper_icon.ico'
    root.iconbitmap(PATH)
    
    #SCROLLBAR
    #CREATE A MAIN FRAME
    main_frame = Frame(article_window)
    main_frame.pack(fill=BOTH, expand=1) #expand frame to size of container

    #CREATE A CANVAS
    my_canvas = Canvas(main_frame) #main_frame in canvas
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    #ADD A SCROLLBAR TOT THE CANVAS
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview) #position scrollbar inside frame but attach to canvas
    my_scrollbar.pack(side=RIGHT, fill=Y)

    #CONFIGURE THE CANVAS
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all"))) #what happens when scrolling

    #CREATE ANOTHER FRAME INSIDE THE CANVAS
    second_frame = Frame(my_canvas)

    #ADD THAT NEW FRAME TO A WINDOW IN THE CANVAS
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    rowcount = 3

    for art in range(0,len(articles_titels)):
        article_button = Button(second_frame, text=articles_titels[art], width=52, anchor='w', command=lambda art=art: open_article(articles_url[art]))
        article_button.pack(expand=YES, pady=2, padx=2)
        rowcount += 1

    #STOPS WEB DRIVER
    driver.quit()

    article_window.mainloop()
    

    
#CREATE WINDOW
root = Tk()    
root.title("News Article Web Scraper")
root.geometry("310x100")

#ICON
PATH = os.path.dirname(os.path.realpath(__file__)) + '\\newspaper_icon.ico'
root.iconbitmap(PATH)

search_word = Label(root, text="Search word:", width=10)
search_word.grid(row=1, column=1, padx=5, pady=10)

input_field = Entry(root, width=30)
input_field.grid(row=1, column=2, padx=5, pady=10)

search_button = Button(root, text="Search", width=41, command=lambda: search(input_field.get(), root))
search_button.grid(row=2, column=1, columnspan=2, padx=5, pady=10)

root.mainloop()
