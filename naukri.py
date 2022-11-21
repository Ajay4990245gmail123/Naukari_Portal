from flask import Flask,render_template,request #import flask
from bs4 import BeautifulSoup as Beauti          # import bs4
from selenium import webdriver             # import selinium webdriver
import time                                   #import time module
from flask_cors import CORS,cross_origin


app=Flask(__name__)
@app.route("/",methods=["GET"])
@cross_origin()
def naukri():  # create interface of searching page
    return render_template("naukri.html")
@app.route("/naukri",methods=["GET","POST"])
@cross_origin()
def vacences(): #
    if request.method=="POST":  # this is condition of methods
        try:
            searching=request.form["text"].replace(" ","-") #searching user
            link = "https://www.naukri.com/"+searching+"-jobs" #  create link of user searching content
            driver = webdriver.Chrome("D:/Naukari/Browsers/chromedriver.exe") # using chrome webdriver
            driver.get(link)
            time.sleep(2)  # web driver sleeping purpose
            Job_read=Beauti(driver.page_source, "html.parser") #convert html code more readble purpose
            naukri=Job_read.find_all("article", class_="jobTuple bgWhite br4 mb-8")  #find all naukri content
            driver.close() # webdriver close
            Jobs=[]   #create empty list
            for jobs in naukri:   # using for loop
                # using  try, except  in case any issue in the code
                try:
                    # get  the job role
                    jobRole = jobs.div.div.a.text
                except:
                    jobRole=" job role not defind"
                try:
                    # get    company name
                    companyName = jobs.div.div.div.a.text
                except:
                    companyName=" company not mentioned"
                try:
                    #get comany  rating
                    companyRating = jobs.div.div.div.span.text
                except:
                    companyRating = " rating not mentiond"
                try:
                    # get job role experiance
                    Experiance = jobs.find_all("span", class_="ellipsis fleft fs12 lh16 expwdth")[0].text
                except:
                    Experiance=" experiance not mentioned in this job"
                try:
                     # get  company location
                    Location = jobs.find_all("span", class_="ellipsis fleft fs12 lh16 locWdth")[0].text
                except:
                    Location=" location is not mentioned in this job"
                try:
                    # get  job main skills
                    mainSkils = jobs.find_all("ul", class_="tags has-description")[0].li.text
                except:
                    mainSkils = " main skills not mentioned"
                try:
                    # get job salary
                    Salary = jobs.find_all("li", class_="fleft grey-text br2 placeHolderLi salary")[0].text
                except:
                    Salary=" salary not mentioned in this job"
                try:
                    # get job  posting date
                    PostDate = jobs.find_all("span", class_="fleft fw500")[0].text
                except:
                    PostDate= " posting date is not available in this page"
                # all information  save in dictionary formate
                myjobs={"jobRole":jobRole,"companyName":companyName,"companyRating":companyRating,"Experiance":Experiance,"Location":Location,"mainSkils":mainSkils,"Salary":Salary,"PostDate":PostDate}
                # all information append jobs variable
                Jobs.append(myjobs)
                print(len(Jobs))
                #using flask templates
            return render_template("naukriresult.html",job_details=Jobs[0:len(Jobs)-1])

        except:
            return "something"
if __name__=="__main__":
    app.run(debug=True)
