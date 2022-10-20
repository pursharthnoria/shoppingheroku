import random
import psycopg2
from email.message import EmailMessage
import ssl
import smtplib
from datetime import date


class database:
    def __init__(self):
        self.host="ec2-44-205-64-253.compute-1.amazonaws.com"
        self.user="jjehaahapopvht"
        self.password="cde7a8d70b0f68e702cb50d901f0b3dcaaf7cd848c0a10ca45c3a2c20ae86b39"
        self.database="d8qg79ls9fdk5l"
        self.port="5432"
        self.email_password = "skslpqnnrurcycnt"
        self.email = "mysmmauth@gmail.com"
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
    
    def createTables(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Buyer(userid text PRIMARY KEY, firstName text, lastName text, defaultProfile text, email text, telegramID text, whatsappNumber text, alternateNumber text, paytmNumber text, gpayNumber text, UPI text, bankname text, accountNumber text, ifsc text, password text,emailVerified text,profilepic BYTEA,whatsappVerified text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Manager(userid text PRIMARY KEY, firstName text, lastName text, defaultProfile text, email text, telegramID text, whatsappNumber text, alternateNumber text, paytmNumber text, gpayNumber text, UPI text, bankname text, accountNumber text, ifsc text, password text, adharCard BYTEA, pancard BYTEA, termsCond boolean, approved text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Seller(userid text PRIMARY KEY, name text, profile text, email text, whatsappNumber text, contactNumber text, cashbackPercent text, password text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Admin (adminID text, password text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Brand (brandID text PRIMARY KEY, sellerID text, brandName text, platformName text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Product (brandID text, productID text PRIMARY KEY, name text, quantity text, amount text, commission text, gst text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Campaign (campaignID text, campaignName text, brandID text, startdate DATE, enddate DATE)")
        cur.execute("CREATE TABLE IF NOT EXISTS allocateProductsToCamp (campaignID text, productID text, quantity text)")
        cur.execute("CREATE TABLE IF NOT EXISTS allocateManagersToCamp (campaignID text, managerID text, slots text)")
        # cur.execute("CREATE TABLE IF NOT EXISTS formDetails (campaignID text, ss1 text, ss2 text, link text, returnExp text, orderDel text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Orders (userid text, campaignID text, orderID text, name text, product text, manager text, orderdate DATE, order_ID text, orderss BYTEA, orderAmount text, refund text,brand text)")
        # cur.execute("CREATE TABLE IF NOT EXISTS additionalOrderInfo (userid text, campaignID text, orderID text, ss1 BYTEA, ss2 BYTEA, link TEXT, returnExp BYTEA, orderDel BYTEA)")
        self.con.commit()
        self.con.close()

    def getBrandBySeller(self,sellerID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Brand where sellerID=%s",(sellerID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        print(users)
        d = []
        for user in users:
            temp = {}
            temp['id'] = user[0]
            temp['name'] = user[2]
            temp['platform'] = user[3]
            d.append(temp)
        return d

    def getAllocateProductsByCampId(self,campID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM allocateProductsToCamp where campaignID=%s",(campID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        print(users)
        d = []
        for user in users:
            temp = {}
            temp['id'] = user[0]
            temp['productID'] = user[1]
            temp['quantity'] = user[2]
            d.append(temp)
        return d

    def getFormByUserId(self,userID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Orders where userid=%s",(userID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users

    def getUserByUserId(self,userID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Buyer where userid=%s",(userID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users[0][1] + " " + users[0][2]

    def getProductBySeller(self,sellerID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Product where brandID in (SELECT brandID from Brand where sellerID=%s)",(sellerID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        d = []
        for user in users:
            temp = {}
            temp['id'] = user[1]
            temp['brand'] = self.getBrandName(user[0])
            temp['name'] = user[2]
            temp['quantity'] = user[3]
            temp['amount'] = user[4]
            temp['commission'] = user[5]
            temp['gst'] = user[6]
            d.append(temp)
        return d
    
    def getProductById(self,id):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Product where productID=%s",(id,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        d = []
        for user in users:
            temp = {}
            temp['id'] = user[1]
            temp['brand'] = self.getBrandName(user[0])
            temp['name'] = user[2]
            temp['quantity'] = user[3]
            temp['amount'] = user[4]
            temp['commission'] = user[5]
            temp['gst'] = user[6]
            d.append(temp)
        return d

    def getProductByBrand(self,brandID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Product where brandID=%s",(brandID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        d = []
        for user in users:
            temp = {}
            temp['id'] = user[1]
            temp['brand'] = self.getBrandName(user[0])
            temp['name'] = user[2]
            temp['quantity'] = user[3]
            temp['amount'] = user[4]
            temp['commission'] = user[5]
            temp['gst'] = user[6]
            d.append(temp)
        return d

    def getFormDetailsByCampId(self,campID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM formDetails where campaignID=%s",(campID,))
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['campaignID'] = user[0]
            temp['ss1'] = user[1]
            temp['ss2'] = user[2]
            temp['link'] = user[3]
            temp['returnExp'] = user[4]
            temp['orderDel'] = user[5]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d
    
    def getAllFormDetails(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM formDetails")
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['campaignID'] = user[0]
            temp['ss1'] = user[1]
            temp['ss2'] = user[2]
            temp['link'] = user[3]
            temp['ReturnExp'] = user[4]
            temp['orderDel'] = user[5]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d

    def getAllOrders(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Orders")
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['userid'] = user[0]
            temp['campaignID'] = user[1]
            temp['orderID'] = user[2]
            temp['name'] = user[3]
            temp['product'] = user[4]
            temp['manager'] = user[5]
            temp['orderdate'] = user[6]
            temp['order_id'] = user[7]
            temp['orderss'] = user[8]
            temp['orderamount'] = user[9]
            temp['refund'] = user[10]
            temp['brand'] = user[11]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d

    def getAdditionalOrderInfo(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM additionalOrderInfo")
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['userid'] = user[0]
            temp['campaignID'] = user[1]
            temp['orderID'] = user[2]
            temp['ss1'] = user[3]
            temp['ss2'] = user[4]
            temp['link'] = user[5]
            temp['ReturnExp'] = user[6]
            temp['orderDel'] = user[7]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d

    def getAllCampaigns(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Campaign")
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        d = []
        for user in users:
            temp = {}
            temp['campaignID'] = user[0]
            temp['name'] = user[1]
            temp['brandname'] = self.getBrandName(user[2])
            temp['start_date'] = user[3]
            temp['end_date'] = user[4]
            d.append(temp)
        return d

    def getActiveCampaigns(self):
        currentDate = date.today()
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        # cur.execute("SELECT * FROM Campaign where startdate<=%s and enddate>=%s",(currentDate,currentDate))
        cur.execute("SELECT * FROM Campaign")
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        d = []
        for user in users:
            temp = {}
            temp['campaignID'] = user[0]
            temp['name'] = user[1]
            temp['brandname'] = self.getBrandName(user[2])
            temp['start_date'] = user[3]
            temp['end_date'] = user[4]
            d.append(temp)
        return d

    def getAllocatedManagers(self,campID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM allocateManagersToCamp where campaignID=%s",(campID,))
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['campaignID'] = user[0]
            temp['managerID'] = user[1]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d

    def getCampById(self,campID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Campaign where campaignID=%s",(campID,))
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['campaignID'] = user[0]
            temp['name'] = user[1]
            temp['brand'] = user[2]
            temp['start_date'] = user[3]
            temp['end_date'] = user[4]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d

    def getProdsByCampId(self,campId):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM allocateProducts where campaignID=%s",(campId,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        d = []
        for user in users:
            d.append([user[1],self.getProdNameById(user[1])])
        
        return d
    
  
    def getProdNameById(self,id):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Product where productID=%s",(id,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users[0][2]

    def getAllAdmins(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Admin")
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['adminID'] = user[0]
            temp['password'] = user[1]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d
    
    def getAllManagers(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Manager where approved=%s",("yes",))
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['userID'] = user[0]
            temp['firstname'] = user[1]
            temp['lastname'] = user[2]
            temp['email'] = user[4]
            temp['whatsapp'] = user[6]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d
    
    def getManById(self,manID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Manager where userid=%s",(manID,))
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['userID'] = user[0]
            temp['firstname'] = user[1]
            temp['lastname'] = user[2]
            temp['email'] = user[4]
            temp['whatsapp'] = user[6]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d
    
    def getNonApprovedApps(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Manager where approved=%s",("no",))
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['userID'] = user[0]
            temp['firstname'] = user[1]
            temp['lastname'] = user[2]
            temp['defaultProfile'] = user[3]
            temp['email'] = user[4]
            temp['whatsapp'] = user[6]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d
    
    def removeUser(self,userID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("DELETE FROM Buyer where userid=%s",(userID,))
        self.con.commit()
        self.con.close()

    def updateManagerApproval(self,userID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("UPDATE Manager set approved=%s where userid=%s",("yes",userID))
        self.con.commit()
        self.con.close()

    def removeManager(self,userID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("DELETE FROM Manager where userid=%s",(userID,))
        self.con.commit()
        self.con.close()

    def getAllSellers(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Seller")
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['userID'] = user[0]
            temp['name'] = user[1]
            temp['email'] = user[3]
            temp['whatsapp'] = user[4]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d
    
    def getAllBrands(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Brand")
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        d = []
        for user in users:
            temp = {}
            temp['id'] = user[0]
            temp['seller'] = self.getSellerName(user[1])
            temp['name'] = user[2]
            temp['platform'] = user[3]
            d.append(temp)
        return d
    
    def getSellerName(self,sellerID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Seller where userid=%s",(sellerID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users[0][1]


    def getManagerName(self,managerID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Manager where userid=%s",(managerID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users[0][1]

    def getBrandName(self,bndID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Brand where brandID=%s",(bndID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users[0][2]

    def getManagerAllocations(self,campID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM allocateManagersToCamp where campaignID=%s",(campID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users
    
    def getAllocateProducts(self,campID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM allocateProductsToCamp where campaignID=%s",(campID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users

    def getAllProducts(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Product")
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        d = []
        for user in users:
            temp = {}
            temp['id'] = user[1]
            temp['brand'] = self.getBrandName(user[0])
            temp['name'] = user[2]
            temp['quantity'] = user[3]
            temp['amount'] = user[4]
            temp['commission'] = user[5]
            temp['gst'] = user[6]
            d.append(temp)
        return d

    def getBrandID(self,name):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Brand WHERE brandName=%s",(name,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        try:
            return users[0][0]
        except:
            return "None"

    def getSellerID(self,name):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Seller WHERE name=%s",(name,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        try:
            return users[0][0]
        except:
            return "None"

    def insertIntoAllocateProducts(self,campaignID, productId, quantity):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO allocateProductsToCamp (campaignID, productId, quantity) VALUES (%s,%s,%s)",(campaignID, productId, quantity))
        self.con.commit()
        self.con.close()


    def insertIntoBuyer(self,userid, firstName, lastName, defaultProfile, email, password, whatsappNumber, telegramID = "None", alternateNumber = "None", paytmNumber="None", gpayNumber="None", UPI="None", bankname="None", accountNumber="None", ifsc="None",emailVerified = "no",profilepic=None,whatsappVerified="no"):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Buyer (userid, firstName, lastName, defaultProfile, email, telegramID, whatsappNumber, alternateNumber, paytmNumber, gpayNumber, UPI, bankname, accountNumber, ifsc, password,emailVerified,profilepic,whatsappVerified) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid, firstName, lastName, defaultProfile, email, telegramID, whatsappNumber, alternateNumber, paytmNumber, gpayNumber, UPI, bankname, accountNumber, ifsc, password,emailVerified,profilepic,whatsappVerified))
        self.con.commit()
        self.con.close()
    
    def insertIntoOrder(self,userid,campaignID,orderID, name, product, manager, orderdate, order_ID, orderss, orderAmount, refund, brand):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Orders (userid,campaignID,orderID, name, product, manager, orderdate, order_ID, orderss, orderAmount, refund, brand) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid,campaignID,orderID, name, product, manager, orderdate, order_ID, orderss, orderAmount, refund, brand))
        self.con.commit()
        self.con.close()

    def insertIntoAdditionalOrderInfo(self,userid, campaignID, orderID, ss1, ss2, link, returnExp, orderDel):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO additionalOrderInfo (userid, campaignID, orderID, ss1, ss2, link, returnExp, orderDel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(userid, campaignID, orderID, ss1, ss2, link, returnExp, orderDel))
        self.con.commit()
        self.con.close()

    def updateBuyerGmailVerification(self,userid):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("UPDATE Buyer set emailVerified='yes' where userid=%s",(userid,))
        self.con.commit()
        self.con.close()

    def sendOTPemail(self,email,otp):
        em= EmailMessage()
        em['From'] = self.email
        em['to'] = email
        em['subject'] = "Shopping app OTP"
        em.set_content("You OTP for verification is: "+str(otp))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
            smtp.login(self.email,self.email_password)
            smtp.sendmail(self.email,email,em.as_string())
    
    # def sendOTPwhatsapp(self,number,otp):
    #     wa_client = client.Client(self.endpoint,self.token)
    #     temp_params = {"otp":otp}
    #     message = wa_client.send_template(number,)

    def insertIntoManager(self,userid, firstName, lastName, defaultProfile, email, password, whatsappNumber, adharCard, pancard, termsCond, telegramID = "None", alternateNumber = "None", paytmNumber="None", gpayNumber="None", UPI="None", bankname="None", accountNumber="None", ifsc="None",approved="yes"):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Manager (userid, firstName, lastName, defaultProfile, email, telegramID, whatsappNumber, alternateNumber, paytmNumber, gpayNumber, UPI, bankname, accountNumber, ifsc, password, adharCard, pancard, termsCond, approved) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid, firstName, lastName, defaultProfile, email, telegramID, whatsappNumber, alternateNumber, paytmNumber, gpayNumber, UPI, bankname, accountNumber, ifsc, password, adharCard, pancard, termsCond, approved))
        self.con.commit()
        self.con.close()
    
    def insertIntoSeller(self,userid, Name, profile, email, whatsappNumber, contactNumber, cashbackPercent, password):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Seller (userid, name, profile, email, whatsappNumber, contactNumber, cashbackPercent, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(userid, Name, profile, email, whatsappNumber, contactNumber, cashbackPercent,password))
        self.con.commit()
        self.con.close()
    
    def insertIntoAdmin(self,adminID,password):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Admin (adminID, password) VALUES (%s,%s)",(adminID,password))
        self.con.commit()
        self.con.close()

    def insertIntoBrand(self,brandID,sellerid, brandName, platformName):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Brand (brandID,sellerID, brandName, platformName) VALUES (%s,%s,%s,%s)",(brandID, sellerid, brandName, platformName))
        self.con.commit()
        self.con.close()
    
    def insertIntoProduct(self, brandID, productID, name, quantity,amount,comm,gst):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Product (brandID, productID, name, quantity,amount, commission, gst) VALUES (%s,%s,%s,%s,%s,%s,%s)",(brandID, productID, name, quantity, amount, comm, gst))
        self.con.commit()
        self.con.close()

    def insertIntoCampaign(self, campaignID, name, brandID, startdate, enddate):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Campaign (campaignID, campaignName, brandID, startdate, enddate) VALUES (%s,%s,%s,%s,%s)",(campaignID, name, brandID, startdate, enddate))
        self.con.commit()
        self.con.close()

    def insertIntoFormDetails(self, campaignID, ss1, ss2, link, returnExp, orderDel):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO formDetails (campaignID, ss1, ss2, link, returnExp, orderDel) VALUES (%s,%s,%s,%s,%s,%s)",(campaignID, ss1, ss2, link, returnExp, orderDel))
        self.con.commit()
        self.con.close()

    def insertIntoAllocateManagers(self,campaignID, manager,slots):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO allocateManagersToCamp (campaignID, managerID,slots) VALUES (%s,%s,%s)",(campaignID, manager,slots))
        self.con.commit()
        self.con.close()

    def login(self,email,password):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Buyer WHERE email=%s and password=%s",(email,password))
        buyers = cur.fetchall()
        # print(buyers)
        cur.execute("SELECT * FROM Admin WHERE adminID=%s and password=%s",(email,password))
        admins = cur.fetchall()
        cur.execute("SELECT * FROM Manager WHERE email=%s and password=%s",(email,password))
        managers = cur.fetchall()
        cur.execute("SELECT * FROM Seller WHERE email=%s and password=%s",(email,password))
        sellers = cur.fetchall()
        if len(buyers)>0:
            role = "buyer"
            d= {
            "userid":buyers[0][0], 
            "firstName":buyers[0][1], 
            "lastName":buyers[0][2], 
            "defaultProfile":buyers[0][3], 
            "email":buyers[0][4], 
            "telegramID":buyers[0][5], 
            "whatsappNumber":buyers[0][6], 
            "alternateNumber":buyers[0][7], 
            "paytmNumber":buyers[0][8], 
            "gpayNumber":buyers[0][9], 
            "UPI":buyers[0][10], 
            "bankname":buyers[0][11], 
            "accountNumber":buyers[0][12], 
            "ifsc":buyers[0][13], 
            "password":buyers[0][14],
            "emailVerified":buyers[0][15],
            "profilePic":buyers[0][16],
            "whatsappVerified":buyers[0][17]
            }
        elif len(admins)>0:
            role = "admin"
            d = {
                "adminID":admins[0][0],
                "password":admins[0][1]
            }
        elif len(managers)>0:
            role = "manager"
            d= {
            "userid":managers[0][0], 
            "firstName":managers[0][1], 
            "lastName":managers[0][2], 
            "defaultProfile":managers[0][3], 
            "email":managers[0][4], 
            "telegramID":managers[0][5], 
            "whatsappNumber":managers[0][6], 
            "alternateNumber":managers[0][7], 
            "paytmNumber":managers[0][8], 
            "gpayNumber":managers[0][9], 
            "UPI":managers[0][10], 
            "bankname":managers[0][11], 
            "accountNumber":managers[0][12], 
            "ifsc":managers[0][13], 
            "password":managers[0][14]
            }
        elif len(sellers)>0:
            role = "seller"
            d= {
            "userid":sellers[0][0], 
            "name":sellers[0][1], 
            "profile":sellers[0][2], 
            "email":sellers[0][3], 
            "whatsapp":sellers[0][4], 
            "contact":sellers[0][5], 
            "cashback":sellers[0][6],
            "password":sellers[0][7]
            }
        else: 
            return False
        self.con.commit()
        self.con.close()
        return (role,d)

    def generateManUserID(self):
        return "MAN"+str(random.randint(1000,9999))
    
    def generateSellerUserID(self):
        return "SELL"+str(random.randint(1000,9999))
    
    def generateBrandId(self):
        return "BRN"+str(random.randint(1000,9999))

    def generatePrdId(self):
        return "PRD"+str(random.randint(1000,9999))
    
    def generateBuyerId(self):
        return "BYR"+str(random.randint(1000,9999))

    def generateCampId(self):
        return "Cmp"+str(random.randint(1000,9999))

    def generateOrdId(self):
        return "ORD"+str(random.randint(1000,9999))

    def generateOTP(self):
        return str(random.randint(1000,9999))

db = database()
db.createTables()