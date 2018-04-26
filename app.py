# -*- coding: utf-8 -*-

from datetime import datetime
import time
from flask import jsonify
import sys
from PyQt4 import QtGui, QtCore, QtWebKit
from flask_restful import Resource
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl,QCoreApplication
from PyQt4.QtWebKit import QWebPage
import bs4 as bs
import sip
import pygeolib
from pygeocoder import Geocoder
from flask_limiter import Limiter
from app import limiter
from flask_jwt import jwt_required,current_identity


j=list()
qt=False

class Render(QtWebKit.QWebPage):
  def __init__(self, urls,app, cb):



    QWebPage.__init__(self)

    self.loadFinished.connect(self._loadFinished)

    self.urls = urls

    self.cb = cb

    self.app=app

    self.crawl()

    self.app.exec_()
    print(1)




  def crawl(self):
    if self.urls:

      url = self.urls.pop(0)

      print ('Downloading', url)

      self.mainFrame().load(QUrl(url))

    else:
      self.app.quit()
      print(2)



  def _loadFinished(self, result):
    frame = self.mainFrame()

    url = str(frame.url().toString())

    html = frame.toHtml()

    self.cb(url, html)

    self.crawl()


class King(Resource):

    def main():
        global app
        app=QtGui.QApplication.instance()
        if app is None:
            app = QtGui.QApplication(sys.argv)
        else:
            app=QtGui.QApplication.instance()



        return app

    def scrape(url, html):

        soup=bs.BeautifulSoup(html,'lxml')
        
        js_test = soup.find_all('div',class_='item__flex-column')

        for item in js_test:
            k={}
            try:
                k["Hotel"]=item.find('h3',class_='name__copytext m-0 item__slideout-toggle').text.encode("utf-8")
                k["Hotel"]=k["Hotel"].decode("utf-8")
            except:
                k["Hotel"]=None

            try:
                k["review"]=item.find('div',class_='item__review item__slideout-toggle').text.encode("utf-8")
                k["review"]=k["review"].decode("utf-8")
            except:
                k["review"]=None

            op=item.find('div',class_='item__best-details')
            try:
                k["discount-price"]=op.find('strong',class_='item__best-price mb-gutter-quarter price_min').text.encode('ascii', errors='ignore').decode("utf-8")

            except:
                k["discount-price"]=None


            try:
                k["best-price"]=op.find('strong',class_='item__best-price mb-gutter-half price single').text.encode('ascii', errors='ignore').decode("utf-8")
            except:
                k["best-price"]=None


            try:
                k["features"]=item.find('div',class_='item__dynamic-content').text.encode("utf-8")
                k["features"]=k["features"].decode("utf-8")
            except:
                k["features"]=None

            try:
                k["best-vendor"]=item.find('em',class_='item__deal-best-ota block fs-normal cur-pointer--hover').text.encode("utf-8")
                k["best-vendor"]=k["best-vendor"].decode("utf-8")
            except:
                k["best-vendor"]=None

            k["locality"]=destination+ "," +  state


            try:
                k["other-vendors"]="Agoda.com, makemytrip, yatra, expedia"

            except:
                k["other-vendors"]=None

            try:
                k["food"]="free-breakfast"
            except:
                k["food"]=None

            k["check-in"]=checkIn.replace("-","/")
            k["check-out"]=checkOut.replace("-","/")
            k["latitude"]=lat
            k["longitude"]=log

            j.append(k)





    def get(self,locality,checkin_date,checkout_date):
            global checkIn
            global checkOut
            global destination
            global lat
            global log
            global state
            global qt
            global c
            destination = locality

            checkin_date = datetime.strptime(checkin_date,"%Y-%m-%d")
            checkout_date = datetime.strptime(checkout_date,"%Y-%m-%d")

            checkIn = datetime.strftime(checkin_date,"%Y-%m-%d")
            checkOut = datetime.strftime(checkout_date,"%Y-%m-%d")

            today = datetime.now()

            if today<datetime.strptime(checkIn,"%Y-%m-%d") and datetime.strptime(checkIn,"%Y-%m-%d")<datetime.strptime(checkOut,"%Y-%m-%d"):
                urls=list()
                try:
                    results=Geocoder.geocode(locality)
                    print(results)
                    r=results[0].coordinates,results.state
                    print(r)
                    lat = r[0][0]
                    log = r[0][1]
                    state=r[1]
                except pygeolib.GeocoderError:
                    return{"message":"invalid location, where are you going? try again!"}
                except:
                    time.sleep(2)
                    return{"message":"hushhh! I need some rest can i come with you to {}".format(locality)}

                checkIn = checkin_date.strftime("%Y-%m-%d")
                checkOut = checkout_date.strftime("%Y-%m-%d")
                for page in range(0,1):
                    url = "https://www.trivago.in/?aDateRange[arr]="+checkIn+"&aDateRange[dep]="+checkOut+"&aPriceRange[from]=0&aPriceRange[to]=0&iPathId=8&aGeoCode[lat]="+str(lat)+"&aGeoCode[lng]="+str(log)+"&iOffset="+str(page)
                    urls.append(url)





                #app=King.main()
                global app
                app = QtGui.QApplication.instance()
                if app is None:
                    app = QtGui.QApplication(sys.argv)
                r = Render(urls,app, cb=King.scrape)





                sip.setdestroyonexit(False)




                print(j)





                return {"message":j}



            #checking whether the entered date is already passed
            elif today>datetime.strptime(checkIn,"%Y-%m-%d") or today>datetime.strptime(checkOut,"%Y-%m-%d"):
                return {"message":"Invalid Checkin date: Please enter a valid checkin and checkout dates,entered date is already passed"}

            elif datetime.strptime(checkIn,"%Y-%m-%d")>datetime.strptime(checkOut,"%Y-%m-%d"):
                return {"message":"Invalid Checkin date: CheckIn date must be less than checkOut date"}
