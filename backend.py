import random
import psycopg2
from email.message import EmailMessage
import ssl
import smtplib

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
        cur.execute("CREATE TABLE IF NOT EXISTS Buyer(userid text PRIMARY KEY, firstName text, lastName text, defaultProfile text, email text, telegramID text, whatsappNumber text, alternateNumber text, paytmNumber text, gpayNumber text, UPI text, bankname text, accountNumber text, ifsc text, password text,verified text)")
        cur.execute("CREATE TABLE IF NOT EXISTS ManagerChecker(userid text PRIMARY KEY, firstName text, lastName text, defaultProfile text, email text, telegramID text, whatsappNumber text, alternateNumber text, paytmNumber text, gpayNumber text, UPI text, bankname text, accountNumber text, ifsc text, password text, adharCard BYTEA, pancard BYTEA, termsCond boolean, role text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Seller(userid text PRIMARY KEY, name text, profile text, email text, whatsappNumber text, contactNumber text, cashbackPercent text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Admin (adminID text, password text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Brand (brandID text PRIMARY KEY, brandName text, platformName text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Product (brandID text, productID text PRIMARY KEY, name text, quantity text, amount text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Campaign (campaignID text, brandname text, productname text, startdate DATE, enddate DATE, quantity text)")
        cur.execute("CREATE TABLE IF NOT EXISTS Allocate (campaignID text, manager text, quantity text)")
        self.con.commit()
        self.con.close()
    
    def getAllCampaigns(self):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Campaign")
        users = cur.fetchall()
        d = []
        for user in users:
            temp = {}
            temp['campaignID'] = user[0]
            temp['brand'] = user[1]
            temp['product'] = user[2]
            temp['start_date'] = user[3]
            temp['end_date'] = user[4]
            temp['quantity'] = user[5]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d

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
        cur.execute("SELECT * FROM ManagerChecker where role=%s",("Manager",))
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
        d = []
        for user in users:
            temp = {}
            temp['id'] = user[0]
            temp['name'] = user[1]
            temp['platform'] = user[2]
            d.append(temp)
        self.con.commit()
        self.con.close()
        return d
    
    def getBrandName(self,bndID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Brand where brandID=%s",(bndID,))
        users = cur.fetchall()
        self.con.commit()
        self.con.close()
        return users[0][1]

    def getAllocations(self,campID):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Allocate where campaignID=%s",(campID,))
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

    def insertIntoBuyer(self,userid, firstName, lastName, defaultProfile, email, password, whatsappNumber, telegramID = "None", alternateNumber = "None", paytmNumber="None", gpayNumber="None", UPI="None", bankname="None", accountNumber="None", ifsc="None",verified = "no"):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Buyer (userid, firstName, lastName, defaultProfile, email, telegramID, whatsappNumber, alternateNumber, paytmNumber, gpayNumber, UPI, bankname, accountNumber, ifsc, password, verified) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid, firstName, lastName, defaultProfile, email, telegramID, whatsappNumber, alternateNumber, paytmNumber, gpayNumber, UPI, bankname, accountNumber, ifsc, password, verified))
        self.con.commit()
        self.con.close()
    
    def updateBuyerVerification(self,userid):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("UPDATE Buyer set verified='yes' where userid=%s",(userid,))
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

    def insertIntoManagerChecker(self,userid, firstName, lastName, defaultProfile, email, password, whatsappNumber, adharCard, pancard, termsCond, role, telegramID = "None", alternateNumber = "None", paytmNumber="None", gpayNumber="None", UPI="None", bankname="None", accountNumber="None", ifsc="None"):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO ManagerChecker (userid, firstName, lastName, defaultProfile, email, telegramID, whatsappNumber, alternateNumber, paytmNumber, gpayNumber, UPI, bankname, accountNumber, ifsc, password, adharCard, pancard, termsCond, role) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid, firstName, lastName, defaultProfile, email, telegramID, whatsappNumber, alternateNumber, paytmNumber, gpayNumber, UPI, bankname, accountNumber, ifsc, password, adharCard, pancard, termsCond, role))
        self.con.commit()
        self.con.close()
    
    def insertIntoSeller(self,userid, Name, profile, email, whatsappNumber, contactNumber, cashbackPercent):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Seller (userid, name, profile, email, whatsappNumber, contactNumber, cashbackPercent) VALUES (%s,%s,%s,%s,%s,%s,%s)",(userid, Name, profile, email, whatsappNumber, contactNumber, cashbackPercent))
        self.con.commit()
        self.con.close()
    
    def insertIntoAdmin(self,adminID,password):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Admin (adminID, password) VALUES (%s,%s)",(adminID,password))
        self.con.commit()
        self.con.close()

    def insertIntoBrand(self,brandID, brandName, platformName):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Brand (brandID, brandName, platformName) VALUES (%s,%s,%s)",(brandID, brandName, platformName))
        self.con.commit()
        self.con.close()
    
    def insertIntoProduct(self, brandID, productID, name, quantity,amount):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Product (brandID, productID, name, quantity,amount) VALUES (%s,%s,%s,%s,%s)",(brandID, productID, name, quantity, amount))
        self.con.commit()
        self.con.close()

    def insertIntoCampaign(self, campaignID, brandname, productname, startdate, enddate, quantity):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Campaign (campaignID, brandname, productname, startdate, enddate, quantity) VALUES (%s,%s,%s,%s,%s,%s)",(campaignID, brandname, productname, startdate, enddate, quantity))
        self.con.commit()
        self.con.close()

    def insertIntoAllocate(self,campaignID, manager, quantity):
        self.con = psycopg2.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Allocate (campaignID, manager, quantity) VALUES (%s,%s,%s)",(campaignID, manager, quantity))
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
        cur.execute("SELECT * FROM ManagerChecker WHERE email=%s and password=%s and role=%s",(email,password,"Manager"))
        managers = cur.fetchall()
        # cur.execute("SELECT * FROM Seller WHERE email=%s and password=%s",(email,password))
        # sellers = cur.fetchall()
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
            "password":buyers[0][14]
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

    def generateOTP(self):
        return str(random.randint(1000,9999))

db = database()
db.createTables()