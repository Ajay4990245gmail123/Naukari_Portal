from flask import Flask,render_template,request
from bs4 import BeautifulSoup as Beauti
from selenium import webdriver
import time
from flask_cors import CORS,cross_origin


app=Flask(__name__)
@app.route("/",methods=["GET"])
@cross_origin()
def naukri():
    return render_template("naukri.html")
@app.route("/naukri",methods=["GET","POST"])
@cross_origin()
def vacences():
    if request.method=="POST":
        try:
            searching=request.form["text"].replace(" ","-")
            link = "https://www.naukri.com/"+searching+"-jobs"
            driver = webdriver.Chrome("D:/Naukari/Browsers/chromedriver.exe")
            driver.get(link)
            time.sleep(2)
            Job_read=Beauti(driver.page_source, "html.parser")
            naukri=Job_read.find_all("article", class_="jobTuple bgWhite br4 mb-8")
            driver.close()
            Jobs=[]
            for jobs in naukri:
                try:
                    jobRole = jobs.div.div.a.text
                except:
                    jobRole=" job role not defind"
                try:
                    companyName = jobs.div.div.div.a.text
                except:
                    companyName=" company not mentioned"
                try:
                    companyRating = jobs.div.div.div.span.text
                except:
                    companyRating = " rating not mentiond"
                try:
                    Experiance = jobs.find_all("span", class_="ellipsis fleft fs12 lh16 expwdth")[0].text
                except:
                    Experiance=" experiance not mentioned in this job"
                try:
                    Location = jobs.find_all("span", class_="ellipsis fleft fs12 lh16 locWdth")[0].text
                except:
                    Location=" location is not mentioned in this job"
                try:
                    mainSkils = jobs.find_all("ul", class_="tags has-description")[0].li.text
                except:
                    mainSkils = " main skills not mentioned"
                try:
                    Salary = jobs.find_all("li", class_="fleft grey-text br2 placeHolderLi salary")[0].text
                except:
                    Salary=" salary not mentioned in this job"
                try:
                    PostDate = jobs.find_all("span", class_="fleft fw500")[0].text
                except:
                    PostDate= " posting date is not available in this page"
                myjobs={"jobRole":jobRole,"companyName":companyName,"companyRating":companyRating,"Experiance":Experiance,"Location":Location,"mainSkils":mainSkils,"Salary":Salary,"PostDate":PostDate}
                Jobs.append(myjobs)
                print(Jobs)
            return render_template("naukriresult.html",job_details=Jobs[0:len(Jobs)-1])
        except:
            return "something"
if __name__=="__main__":
    app.run(debug=True)
