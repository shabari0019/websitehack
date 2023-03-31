
from flask import Flask, render_template
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#
# Open link in new page
# Make text to link
# Remove Borders
# Add link to skip to particular section
# Login for community

from tkinter import *
import csv
global lan,lat

with open('static/lan-lon.csv', 'r') as fp:
    s = list(csv.reader(fp))


a = {}
for i in s:
    a[i[0]] = [i[1], i[2]]


main = Tk()
main.title("Time crunch")
canvas = Canvas(width=780, height=600, bg="green", highlightthickness=0)
po = PhotoImage(file="static/karnataka-d.png")
kmap = canvas.create_image(390, 300, image=po)
text = canvas.create_text(100, 201, text="kmap")
strvar = StringVar()


'''
def listbox_used(event):
    strvar = listbox.get(listbox.curselection())
    strvar = strvar[4:]
    global lat,lan
    lat = a[strvar][0]
    lan = a[strvar][1]
'''
'''
for item in dis:
    listbox.insert(dis.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
'''

def show():
    label.config(text=clicked.get())
    strvar = clicked.get()
    strvar = strvar[4:]
    global lat, lan
    lat = a[strvar][0]
    lan = a[strvar][1]


listbox = Listbox(height=27)
dis = ["01: Bagalkote", "02: Bangalore Rural", "03: Bangalore Urban", "04: Belagavi", "05: Bellary", "06: Bidar",
          "07: Bijapur", "08: Chamarajanagar", "09: Chikkamagaluru", "10: Chitradurga", "11: Dakshina Kannada",
          "12: Davangere", "13: Dharwad", "14: Gadag", "15: Gulbarga", "16: Hassan", "17: Haveri", "18: Kodagu",
          "19: Kolar", "20: Koppal", "21: Mandya", "22: Mysore", "23: Raichur", "24: Shivmogga", "25: Tumkur",
          "26: Udupi", "27: Uttara Kannada"]

canvas.grid(column=3, row=3)
clicked = StringVar()
clicked.set("Choose one district")
drop = OptionMenu(main, clicked, *dis)
drop.grid(row=0, column=0, sticky=W, pady=2)
button = Button(main, text="Submit", command=show).grid(row=1, column=0, sticky=W, pady=2)
label = Label(main, text=" ")
label.grid(column=2, row=5)
canvas.grid(column=3, row=3)
main.mainloop()

app = Flask(__name__)

@app.route('/')
def hello_world():
    chromepath = "C:\development\chromedriver.exe"

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options = options, executable_path=chromepath)
    driver.get("https://economictimes.indiatimes.com/topic/agriculture-technology")
    items = driver.find_elements(By.CLASS_NAME, "contentD")
    d = {}
    i=0
    for item in items:
        i+=1
        title = item.find_element(By.CSS_SELECTOR, "a").get_attribute("title")
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        d.update({i: [link, title]})
    print(d)


    return render_template('index.html',data = d,le = i)


@app.route("/farmer aid")
def farmer():
    return render_template("farmeraid.html")


@app.route('/farmer aid/weather')
def weather():
    api_endpoint_w = " https://api.ambeedata.com/weather/latest/by-lat-lng"
    api_key = "ee9363b0b9197d12bab864bcc73394ff28a8265a67d499cd80e53c5a7dba045e"
    par = {
        "lat": lat,
        "lng": lan,
        "units":"si"
    }
    h = {
        "x-api-key": api_key
    }

    data = requests.get(api_endpoint_w, params=par, headers=h)
    con = data.json()["data"]
    t = con["temperature"]
    w = con["windSpeed"]

    return render_template("weather.html",temp = t,wind = w)


@app.route("/community")
def community():
    return render_template("community.html")

@app.route("/farmer aid/pest")
def pest():
    return render_template("pestcontrol.html")


@app.route("/farmer aid/alert")
def alert():
    end = "https://api.ambeedata.com/weather/alerts/latest/by-lat-lng"
    api_key = "ee9363b0b9197d12bab864bcc73394ff28a8265a67d499cd80e53c5a7dba045e"
    par = {
        "lat": lat,
        "lng": lan,
        "units": "si"
    }
    h = {
        "x-api-key": api_key
    }
    data = requests.get(end, params=par, headers=h)
    con = data.json()["data"]

    return render_template("alert.html",al = con)

if __name__ == '__main__':
    app.run(debug=True)
