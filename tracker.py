from bs4 import BeautifulSoup
import requests
import smtplib
GMAIL_USER = ""
GMAIL_PWD = ""
FROM = GMAIL_USER
TO = "cis@amazon.com"
SUBJECT = "PRICE REDUCTION CLAIM FOR %s"

BASE = "https://www.amazon.com/gp/product/"
PRODUCTS = [('B00KVI76ZS', 150.99, 'kindlebook')]
MARKS = []

def claimCheck():
  for index, ii in enumerate(PRODUCTS):
    getPrice(ii, index)
  while MARKS:
    #Remove everything for which a claim has been submitted
    PRODUCTS.pop(MARKS[0])
  

def getPrice(product, index):
  html = requests.get(BASE + product[0])
  #Parse HTML
  soup = BeautifulSoup(html.text, "html.parser")
  
  #XPATH for car stuff, pet supplies, computers and kitchen ware
  if product[2] == 'other':
    prices = soup.findAll(attrs = {"id" : "priceblock_ourprice"})
  
  #XPATH for kindle books
  elif product[2] == 'kindlebook':
    prices = soup.find_all("span" , class_ = "a-color-price")

  if prices:
    #Check if price has dropped
    if float(prices[0].text[1:]) < float(product[1]):
      print "Reduced Price Found at %s" %prices[0].text[1:]
      if notifyEmail(product[0], product[1], prices[0].text):
        #Mark this product as notified.
        MARKS.append(index)
      
def notifyEmail(product, price_old, price_new):
  message = """
            \From: %s\nTo: %s\nSubject : %s\n
            Hello \n I recently purchased %s from amazon for %s, \n
            and I note that the price has dropped to %s. Can you please
            refund me the difference to match the lowest price?\Thanks
            """ %(FROM, TO , SUBJECT, product, price_old, price_new)
  try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PWD)
    server.sendmail(FROM, TO, message)
    server.close()
    print "Refund Claim Sent"
    return 1
  except:
    print "Failed to send claim"
    return 0
  
def main():
  claimCheck()

if __name__== "__main__":
  main()
