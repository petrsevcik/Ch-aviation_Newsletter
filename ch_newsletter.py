from flask import Flask
from flask_mail import Mail, Message
from selenium import webdriver

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.seznam.cz' #here you can put your smtp - googlemail.com or yahoo or I use seznam.cz because google is blocking app which he doesnt trust unless you change your setup
app.config['MAIL_PORT'] = 587 #random port
app.config['MAIL_USE_TLS'] = True #not sure for what is this
app.config['MAIL_USERNAME'] = "petrsevcik93@seznam.cz" #your email
#password need to be inserted  app.config['MAIL_PASSWORD'] = "passwd" #your password
mail = Mail(app)
def scrape_news():
    PATH = "./chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.get('https://www.ch-aviation.com/login?od=http%3A%2F%2Fwww.ch-aviation.com%2F')
    #login
    username = driver.find_element_by_id("email")
    password = driver.find_element_by_id("password")
    username.send_keys("slavomir.mucha@kiwi.com")
#password need to be inserted    password.send_keys("passwd")
    submit = driver.find_element_by_xpath('//*[@id="login"]/div[1]/form[1]/div[4]/input')
    submit.click()
    try:
        welcome = driver.find_element_by_xpath('//*[@id="user-sessions"]/form/div[2]/button')
        welcome.click()
    except:
        pass
    #login success
    #go to news
    news = driver.find_element_by_xpath('//*[@id="head__content"]/div[3]/ul[1]/li[1]/a')
    news.click()
    #filter out route news
    search = driver.find_element_by_xpath('//*[@id="search-module"]/form/div[2]/button')
    search.click()
    #scraping news
    body = []
    for n in range(1,10):
        headline = driver.find_element_by_xpath(f'//*[@id="search-module"]/div[1]/div[2]/div/div[{n}]/div/h3/a')
        x = headline.text
        date = driver.find_element_by_xpath(f'//*[@id="search-module"]/div[1]/div[2]/div/div[{n}]/div/span')
        y = date.text
        content = driver.find_element_by_xpath(f'//*[@id="search-module"]/div[1]/div[2]/div/div[{n}]/div/div[2]/div')
        z = content.text
        result = x,y,z
        body.append(list(result))
#in case you want to put it in csv add:
                    #header = ["headline", "date", "content"]
                    #f = open("chaviation_news.csv", "w")
                    #f_writer = csv.writer(f)
                    #f_writer.writerow(header)
                    #f_writer.writerows(body)
                    #f.close()
    driver.close()
    return body


news = scrape_news()

@app.route("/")
def index():
    msg = Message(
        'CH-Aviation 10 latest news',
        sender='petrsevcik93@seznam.cz',
        recipients=['petrsevcik93@gmail.com','petr.sevcik@kiwi.com','jian.liang@kiwi.com' ]
    )
    headers = ""
    for item in news:
        header = item[0]
        headers += header + "\n"
    msg.body = headers
    mail.send(msg)
    return 'Sent'

app.run()