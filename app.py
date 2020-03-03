from flask import Flask,render_template,url_for,request
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyrebase

app=Flask(__name__)

# Classified info
config={
	# configuration information
}


@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/store',methods=['POST'])
def store():
    if request.method=='POST':
        #initializing database
        firebase=pyrebase.initialize_app(config)
        db=firebase.database()
        # fethcing data
        users=db.child('users').get()
        #getting information
        rn=request.form.get('rollno')
        pwd=request.form.get('password')
        em=request.form.get('email')
        if(users.val()!=None):
            for user in users:
                user=user.val()
                if(rn in user['rollno']):
                    return render_template('status.html',status={'flag':2})
            
        details={'rollno':rn,'password':pwd,'email':em}
        # try:
        #     db.child("users").push(details)
        # except:
        #     return render_template('status.html',status={'flag':3})
        # Email id login and trying to send the mail to the user
        try:
            smtp=smtplib.SMTP('smtp.gmail.com',587)
            smtp.starttls()
            smtp.login(botemailid,botmail password)
            # web scraping
            browser=webdriver.Chrome()
            browser.get('https://erp.cbit.org.in/Login.aspx?ReturnUrl=%2f')
            un=browser.find_element_by_id("txtUserName")
            un.send_keys(rn)
            sub=browser.find_element_by_id("btnNext")
            sub.click()
            pw=browser.find_element_by_id("txtPassword")
            pw.send_keys(pwd)
            sub2=browser.find_element_by_id("btnSubmit")
            sub2.click()
            per=browser.find_element_by_id("ctl00_cpStud_lblTotalPercentage")
            ca=browser.find_element_by_xpath("//*[@id='ctl00_cpStud_grdSubject']/tbody/tr[12]/td[5]")
            tc=browser.find_element_by_xpath("//*[@id='ctl00_cpStud_grdSubject']/tbody/tr[12]/td[4]")
            message="\nYour Attendace :"+per.text+"\n"
            message=message+"Total classes attended :"+ca.text+"\n"
            message=message+"Total classes conducted : "+tc.text+"\n"
            sub3=browser.find_element_by_id("ctl00_cpHeader_ucStud_lnkLogOut")
            sub3.click()
            # print(message)
            # sending the mail
            smtp.sendmail(botmailid,em,message)
            smtp.quit()
             # pushing into database
            db.child("users").push(details)
            browser.quit()
        except:
            return render_template('status.html',status={'flag':3})
        return render_template('status.html',status={'flag':1})

if __name__=="__main__":
    app.run(debug=True)