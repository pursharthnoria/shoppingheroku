from flask import Flask, request, jsonify, render_template, redirect, session, flash
from flask_session import Session
from backend import database
from datetime import date

db = database()
db.createTables()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login',methods=['POST'])
def login():
    email = request.form.get('email')
    passowrd = request.form.get('password')
    result = db.login(email,passowrd)
    print(result)
    if result==False:
        return redirect("/")
    else:
        role = result[0]
        details = result[1]
        if role == "admin":
            session['name'] = "admin"
            return redirect("/adminDashboard")
        elif role == "buyer":
            session["userid"] = details["userid"]
            session["email"] = details['email']
            session["firstName"] = details["firstName"]
            session["lastName"] = details["lastName"]
            session["defaultProfile"] = details["defaultProfile"]
            session["telegramID"] = details["telegramID"]
            session["whatsappNumber"] = details["whatsappNumber"]
            session["alternateNumber"] = details["alternateNumber"] 
            session["paytmNumber"] = details["paytmNumber"]
            session["gpayNumber"] = details["gpayNumber"]
            session["UPI"] = details["UPI"]
            session["bankname"] = details["bankname"]
            session["accountNumber"] = details["accountNumber"]
            session["ifsc"] = details["ifsc"]
            session["password"] = details["password"] 
            session["emailVerified"] = details['emailVerified']
            session["profilePic"] = details['profilePic']
            session["whatsappVerified"] = details['whatsappVerified']
            if session['emailVerified'] == "yes" or session['emailVerified']=="yes":
                return redirect("/buyerDashboard")
            else:
                otp = db.generateOTP()
                db.sendOTPemail(email,otp)
                session['otp'] = otp
                return redirect("/pleaseVerify")
        elif role == "manager":
            session["userid"] = details["userid"]
            session["firstName"] = details["firstName"]
            session["lastName"] = details["lastName"]
            session["defaultProfile"] = details["defaultProfile"]
            session["telegramID"] = details["telegramID"]
            session["whatsappNumber"] = details["whatsappNumber"]
            session["alternateNumber"] = details["alternateNumber"] 
            session["paytmNumber"] = details["paytmNumber"]
            session["gpayNumber"] = details["gpayNumber"]
            session["UPI"] = details["UPI"]
            session["bankname"] = details["bankname"]
            session["accountNumber"] = details["accountNumber"]
            session["ifsc"] = details["ifsc"]
            session["password"] = details["password"] 
            return redirect("/managerDashboard")
        elif role=="seller":
            session["userid"] = details["userid"]
            session["name"] = details["name"]
            session["profile"] = details["profile"]
            session["email"] = details["email"]
            session["whatsapp"] = details["whatsapp"]
            session["contact"] = details["contact"]
            session["cashback"] = details["cashback"]
            return redirect("/sellerDashboard")


@app.route("/register", methods=['POST'])
def register():
    firstName = request.form.get("first_name")
    lastName = request.form.get("last_name")
    profile = request.form.get("profile")
    password = request.form.get("password")
    email = request.form.get("email",default="No email input")
    telegram = request.form.get("telegram",default="None")
    whatsapp = request.form.get("whatsapp")
    alternate = request.form.get("alternate",default="None")
    paytm = request.form.get('paytm')
    gpay = request.form.get("gpay",default="None")
    upi = request.form.get("upi",default="None")
    account = request.form.get("account",default="None")
    ifsc = request.form.get("ifsc",default="None")
    userid = db.generateBuyerId()
    try:
        db.insertIntoBuyer(userid, firstName, lastName, profile, email, password, whatsapp, telegramID = telegram, alternateNumber = alternate, paytmNumber=paytm, gpayNumber=gpay, UPI=upi, bankname="None", accountNumber=account, ifsc=ifsc,emailVerified="no")
        session["userid"] = userid
        session["firstName"] = firstName
        session["lastName"] = lastName
        session["defaultProfile"] = profile
        session["telegramID"] = telegram
        session['email'] = email
        session["whatsappNumber"] = whatsapp
        session["alternateNumber"] = alternate
        session["paytmNumber"] = paytm
        session["gpayNumber"] = gpay
        session["UPI"] = upi
        session["bankname"] = "None"
        session["accountNumber"] = account
        session["ifsc"] = ifsc
        session["password"] = password
        otp = db.generateOTP()
        db.sendOTPemail(email,otp)
        session['otp'] = otp
        return redirect("/pleaseVerify")
    except Exception as e:
        print(e)
        return redirect("/")


@app.route('/buyerDashboard')
def buyerDashboard():
    if session.get("userid"):
        return render_template("user_dashboard.html",name = session['firstName'])


@app.route('/applyForManager')
def applyForManager():
    if session.get("userid"):
        return render_template("applyForManager.html",name = session['firstName'])


@app.route('/applyManager',methods=['POST'])
def applyManager():
    if session.get("userid"):
        pancard = request.form.get("pan card")
        adharcard = request.form.get("adhar card")
        db.insertIntoManager(session.get("userid"), 
        session.get("firstName"), 
        session.get("lastName"), 
        session.get("defaultProfile"), 
        session.get("email"),
        session.get("password"), 
        session.get("whatsappNumber"), 
        adharcard, 
        pancard, 
        "True", 
        telegramID = session.get("telegramID"), 
        alternateNumber = session.get("alternateNumber"), 
        paytmNumber=session.get("paytmNumber"), 
        gpayNumber=session.get("gpayNumber"), 
        UPI=session.get("UPI"), 
        bankname=session.get("bankname"), 
        accountNumber=session.get("accountNumber"), 
        ifsc=session.get("ifsc"),
        approved="no")
        return render_template("applyForManager.html",name = session['firstName'])


@app.route('/activeCampaigns')
def activeCampaigns():
    if session.get("userid"):
        camps = db.getAllCampaigns()
        return render_template("activeCampaigns.html",name = session['firstName'],camps=camps)


# @app.route('/campaignForm/<campID>')
# def campaignForm(campID):
#     if session.get("userid"):
#         alls = db.getAllById(campID)
#         camps = db.getCampById(campID)
#         prods = db.getProdsByCampId(campID)
#         print(prods)
#         brand = db.getBrandName(camps[0]['brand'])
#         manNames = []
#         for all in alls:
#             manNames.append((all['manager'],db.getManagerName(all['manager'])))
#         return render_template("form.html",name = session['firstName'],manNames = manNames,brand = brand, today = date.today(),products = prods,campID = campID)



@app.route("/managerApplications")
def managerApplications():
    if session.get("name"):
        managersApps = db.getNonApprovedApps()
        return render_template("managerApplications.html",managers=managersApps)


@app.route("/approveManager/<userid>")
def approveManager(userid):
    if session.get("name"):
        db.removeUser(userid)
        db.updateManagerApproval(userid)
        return render_template("managerApplications.html")

@app.route("/rejectManager/<userid>")
def rejectManager(userid):
    if session.get("name"):
        db.removeManager(userid)
        return render_template("managerApplications.html")

@app.route('/sellerDashboard')
def sellerDashboard():
    if session.get("userid"):
        return render_template("seller_dashboard.html",name = session['name'])


@app.route('/adminDashboard')
def adminDashboard():
    if session.get("name"):
        return render_template("admin_dashboard.html")


@app.route("/viewAdmins")
def viewAdmins():
    if session.get("name"):
        admins = db.getAllAdmins()
        return render_template("admin_list.html",admins=admins)


@app.route("/viewManagers")
def viewManagers():
    if session.get("name"):
        managers = db.getAllManagers()
        return render_template("manager_list.html",managers = managers)


@app.route("/getSellerBrands")
def getSellerBrands():
    if session.get("userid"):
        managers = db.getBrandBySeller(session.get('userid')) 
        return render_template("sellerBrands.html",brands = managers)


@app.route("/getSellerProducts")
def getSellerProducts():
    if session.get("userid"):
        products = db.getProductBySeller(session.get("userid"))
        return render_template("sellerProducts.html",products=products)


@app.route("/getSellerCampaigns")
def getSellerCampaigns():
    if session.get("userid"):
        camps = db.getAllCampaigns()
        return render_template("sellerCampsList.html",camps=camps)


@app.route("/viewSellers")
def viewSellers():
    if session.get("name"):
        sellers = db.getAllSellers()
        return render_template("seller_list.html",sellers=sellers)


@app.route("/viewBrands")
def viewBrands():
    if session.get("name"):
        brands = db.getAllBrands()
        return render_template("brand_list.html", brands=brands)


@app.route("/viewProducts")
def viewProducts():
    if session.get("name"):
        products = db.getAllProducts()
        return render_template("product_list.html",products=products)


@app.route("/viewCampaigns")
def viewCampaigns():
    if session.get("name"):
        camps = db.getAllCampaigns()
        return render_template("campaign_list.html",camps=camps)


@app.route("/view_manager/<campaignID>")
def viewAllMan(campaignID):
    if session.get("name"):
        allocations = db.getManagerAllocations(campaignID)
        return render_template("view_manager.html",allocations=allocations)


@app.route("/view_products/<campaignID>")
def view_products(campaignID):
    if session.get("name"):
        allocations = db.getAllocateProducts(campaignID)
        return render_template("view_products.html",allocations=allocations)


@app.route("/firstForm")
def firstForm():
    if session.get("userid"):
        activeCamps = db.getActiveCampaigns()
        print(activeCamps)
        return render_template("firstForm.html",camps=activeCamps)


@app.route("/parttwo",methods=['POST'])
def parttwo():
    if session.get("userid"):
        campID = request.form.get("camp")
        campDetails = db.getCampById(campID)
        products = db.getAllocateProductsByCampId(campID)
        managers = db.getAllocatedManagers(campID)
        print(managers)
        mans = []
        prods = []
        for val in products:
            product = db.getProductById(val['productID'])
            prods.append((val['productID'],product[0]['name']))
        print(prods)
        for val in managers:
            man = db.getManById(val['managerID'])
            print(man)
            mans.append((val['managerID'],man[0]['firstname'] + " " + man[0]['lastname']))
        print(mans)
        return render_template("firstFormPartTwo.html",campID=campID,campDetails=campDetails,prods = prods,mans=mans,today = date.today())


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/addAdmin")
def addAdmin():
    if session.get("name"):
        return render_template("admin_add.html")


@app.route("/addAdminButton",methods=['POST'])
def addAdminButton():
    if session.get("name"):
        adminID = request.form.get("adminID")
        password = request.form.get("password")
        try:
            db.insertIntoAdmin(adminID,password)
        except Exception as e:
            print(e)
        return redirect("/viewAdmins")


@app.route("/addManager")
def addManager():
    if session.get("name"):
        return render_template("manager_add.html")


@app.route("/addManagerButton",methods=['POST'])
def addManagerButton():
    if session.get("name"):
        firstName = request.form.get("FirstName")
        lastName = request.form.get("LastName")
        profile = request.form.get("profile")
        password = request.form.get("password")
        email = request.form.get("email",default="No email input")
        telegram = request.form.get("telegram",default="None")
        whatsapp = request.form.get("whatsapp")
        alternate = request.form.get("alternate",default="None")
        paytm = request.form.get('paytm')
        gpay = request.form.get("gpay",default="None")
        upi = request.form.get("upi",default="None")
        account = request.form.get("account",default="None")
        ifsc = request.form.get("ifsc",default="None")
        userid = db.generateManUserID()
        adharcard = request.form.get("adhar")
        pan = request.form.get("pan")
        try:
            db.insertIntoManager(userid, firstName, lastName, profile, email, password, whatsapp, adharcard, pan, "True", telegramID = telegram, alternateNumber = alternate, paytmNumber=paytm, gpayNumber=gpay, UPI=upi, bankname="None", accountNumber=account, ifsc=ifsc)
        except Exception as e:
            print(e)
        return redirect("/viewManagers")


@app.route("/addSeller")
def addSeller():
    if session.get("name"):
        return render_template("seller_add.html")


@app.route("/addSellerButton",methods=["POST"])
def addSellerButton():
    if session.get("name"):
        name = request.form.get("name")
        profile = request.form.get("profile")
        email = request.form.get("email")
        whatsapp = request.form.get("whatsapp")
        contact = request.form.get("contact")
        cashback = request.form.get("cashback")
        password = request.form.get("password")
        userid = db.generateSellerUserID()
        try:
            db.insertIntoSeller(userid, name, profile, email, whatsapp, contact, cashback, password)
        except Exception as e:
            print(e)
        return redirect("/viewSellers")


@app.route("/addBrand")
def addBrand():
    if session.get("name"):
        sellers = db.getAllSellers()
        names = []
        for seller in sellers:
            names.append(seller['name'])
        return render_template("brand_add.html",sellers=names)


@app.route("/addBrandButton",methods=["POST"])
def addBrandButton():
    if session.get("name"):
        name = request.form.get("name")
        platform = request.form.get("platform")
        seller = request.form.get("seller")
        sellerid = db.getSellerID(seller)
        bndID= db.generateBrandId()
        try:
            db.insertIntoBrand(bndID,sellerid,name,platform)
        except Exception as e:
            print(e)
        return redirect("/viewBrands")


@app.route("/addProduct")
def addProduct():
    if session.get("name"):
        brands = db.getAllBrands()
        names = []
        for brand in brands:
            names.append(brand['name'])
        return render_template("product_add.html",names=names)


@app.route("/addProductButton",methods=["POST"])
def addProductButton():
    if session.get("name"):
        brandname = request.form.get("brandname")
        bndID = db.getBrandID(brandname)
        productname = request.form.get("productname")
        quantity = request.form.get("quantity")
        amount = request.form.get("amount")
        commission = request.form.get("commission")
        gst = request.form.get("gst")
        prdID= db.generatePrdId()
        try:
            if bndID!="None":
                db.insertIntoProduct(bndID,prdID,productname,quantity,amount,commission,gst)
            else:
                pass
        except Exception as e:
            print(e)
        return redirect("/viewProducts")


@app.route("/addCampaign")
def addCampaign():
    if session.get("name"):
        brands = db.getAllBrands()
        products = db.getAllProducts()
        brandnames = []
        productnames = []
        for brand in brands:
            brandnames.append(brand['name'])
        for product in products:
            productnames.append(product['name'])
        return render_template("campaign_add.html",brandnames=brandnames,productnames=productnames)


@app.route("/addCampaignButton",methods=["POST"])
def addCampaignButton():
    if session.get("name"):
        name = request.form.get("name")
        brandname = request.form.get("brandname")
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        campID= db.generateCampId()
        brandId = db.getBrandID(brandname)
        try:
            db.insertIntoCampaign(campID, name, brandId, startdate, enddate)
        except Exception as e:
            print(e)
        return redirect("/viewCampaigns")


@app.route("/sign")
def sign():
    return render_template("sign.html")


@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgot.html")


@app.route("/pleaseVerify")
def verify():
    if session.get("userid"):
        return render_template("pleaseVerify.html")


@app.route("/verify",methods=['POST'])
def verifyOTP():
    if session.get("userid"):
        otp = request.form.get("otp")
        if otp == session.get("otp"):
            db.updateBuyerGmailVerification(session.get("userid"))
            return redirect("/buyerDashboard")
        else:
            return redirect("/pleaseVerify")


@app.route("/selectmanager/<campId>")
def selectmanagers(campId):
    if session.get("name"):
        managers = db.getAllManagers()
        return render_template('select_manager.html',managers=managers,campID = campId)


@app.route("/select_product/<campId>/<brandname>")
def select_product(campId,brandname):
    if session.get("name"):
        brandID = db.getBrandID(brandname)
        products = db.getProductByBrand(brandID)
        return render_template('select_products.html',products=products,campID = campId)


@app.route("/allocateProducts",methods=['POST'])
def allocateProducts():
    if session.get("name"):
        products = request.form.getlist("products")
        quantities = request.form.getlist("quantity")
        # amounts = request.form.getlist("amount")
        campId = request.form.get("campId")
        prodList = []
        for i in range(len(products)):
            temp = []
            temp.append(products[i])
            temp.append(quantities[i])
            # temp.append(amounts[i])
            prodList.append(temp)
        for prod in prodList:
            db.insertIntoAllocateProducts(campId, prod[0], prod[1])
        return redirect("/viewCampaigns")


@app.route("/allocatemanagers",methods=['POST'])
def allocate():
    if session.get("name"):
        managers = request.form.getlist("managers")
        slots = request.form.getlist("slots")
        print(managers)
        campId = request.form.get("campId")
        finalList = []
        for i in range(len(managers)):
            managers[i] = managers[i].split(" ")
            finalList.append((managers[i][0],slots[i]))
        print(managers)
        print(finalList)
        for man in finalList:
            db.insertIntoAllocateManagers(campId,man[0],man[1])
        return redirect("/viewCampaigns")


@app.route("/submitOrder",methods=["POST"])
def submitOrder():
    if session.get("userid"):
        campID = request.form.get("campID")
        manID = request.form.get("manager")
        affiliate_name = request.form.get("affiliate_name")
        brand = request.form.get("brand")
        productID = request.form.get("product")
        # for i in range(len(managers)):
        #     if "(" in managers[i]:
        #         managers[i] = managers[i].replace("(","")
        #     if ")" in managers[i]:
        #         managers[i] = managers[i].replace(")","")
        # managerid = managers[0]
        # print(manager)
        order_date = request.form.get("order_date")
        order_id = request.form.get("order_id")
        order_screenshot = request.form.get("order_screenshot")
        order_amount = request.form.get("order_amount")
        refund_amount = request.form.get("refund_amount")
        brandID = db.getBrandID(brand)
        ordID= db.generateOrdId()
        uid = session.get("userid")
        campid = request.form.get("campID")
        try:
            db.insertIntoOrder(uid,campid,ordID,affiliate_name,productID,manID,order_date,order_id,order_screenshot,order_amount,refund_amount,brandID,"Pending")
        except Exception as e:
            print(e)
        return redirect("/buyerDashboard")

@app.route("/submitOrderDetails",methods=["POST"])
def submitOrderDetails():
    if session.get("userid"):
        ss1 = request.form.get("ss1",default=None)
        ss2 = request.form.get("ss2",default=None)
        link = request.form.get("link",default=None)
        returnExp = request.form.get("returnExp",default=None)
        orderDel = request.form.get("orderDel",default=None)
        ordID = request.form.get("ordID",default=None)
        print(ordID)
        campid = request.form.get("campid",default=None )
        print(campid)
        db.insertIntoAdditionalOrderInfo(session.get('userid'),campid,ordID,ss1,ss2,link,returnExp,orderDel)
        return redirect("/buyerDashboard")


@app.route("/submittedForms")
def submittedForms():
    if session.get("userid"):
        forms = db.getFormByUserId(session.get("userid"))
        for i in range(len(forms)):
            forms[i]['username'] = db.getUserByUserId(forms[i]['userid'])
        return render_template("submitted_forms.html",forms=forms)

@app.route("/submittedUserFroms")
def submittedUserFroms():
    if session.get("name"):
        forms = db.getAllOrders()
        for i in range(len(forms)):
            forms[i]['username'] = db.getUserByUserId(forms[i]['userid'])
        return render_template("submittedUserForms.html",forms=forms)

@app.route("/approvedForms")
def approvedForms():
    if session.get("name"):
        forms = db.getApprovedOrders()
        for i in range(len(forms)):
            forms[i]['username'] = db.getUserByUserId(forms[i]['userid'])
        return render_template("approvedForms.html",forms=forms)

@app.route("/rejectedForms")
def rejectedForms():
    if session.get("name"):
        forms = db.getRejectedOrders()
        for i in range(len(forms)):
            forms[i]['username'] = db.getUserByUserId(forms[i]['userid'])
        return render_template("rejectedForms.html",forms=forms)

@app.route("/approveOrderAdmin/<userid>/<campaignID>")
def approveOrderAdmin(userid,campaignID):
    if session.get("name"):
        forms = db.approveOrderAdmin(userid,campaignID)
        return redirect("/submittedUserFroms")

@app.route("/rejectOrderAdmin/<userid>/<campaignID>")
def rejectOrderAdmin(userid,campaignID):
    if session.get("name"):
        forms = db.rejectOrderAdmin(userid,campaignID)
        return redirect("/submittedUserFroms")

if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)