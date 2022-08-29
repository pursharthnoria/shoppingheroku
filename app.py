from flask import Flask, request, jsonify, render_template, redirect, session, flash
from flask_session import Session
from backend import database

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
            return redirect("/buyerDashboard")
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
        allocations = db.getAllocations(campaignID)
        return render_template("view_manager.html",allocations=allocations)


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
            db.insertIntoManagerChecker(userid, firstName, lastName, profile, email, password, whatsapp, adharcard, pan, "True", "Manager", telegramID = telegram, alternateNumber = alternate, paytmNumber=paytm, gpayNumber=gpay, UPI=upi, bankname="None", accountNumber=account, ifsc=ifsc)
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
        userid = db.generateSellerUserID()
        try:
            db.insertIntoSeller(userid, name, profile, email, whatsapp, contact, cashback)
        except Exception as e:
            print(e)
        return redirect("/viewSellers")


@app.route("/addBrand")
def addBrand():
    if session.get("name"):
        return render_template("brand_add.html")


@app.route("/addBrandButton",methods=["POST"])
def addBrandButton():
    if session.get("name"):
        name = request.form.get("name")
        platform = request.form.get("platform")
        bndID= db.generateBrandId()
        try:
            db.insertIntoBrand(bndID,name,platform)
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
        prdID= db.generatePrdId()
        try:
            if bndID!="None":
                db.insertIntoProduct(bndID,prdID,productname,quantity,amount)
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
        brandname = request.form.get("brandname")
        product = request.form.get("product")
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        quantity = request.form.get("quantity")
        campID= db.generateCampId()
        try:
            db.insertIntoCampaign(campID, brandname, product, startdate, enddate, quantity)
        except Exception as e:
            print(e)
        return redirect("/viewCampaigns")


@app.route("/sign")
def sign():
    return render_template("sign.html")


@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgot.html")


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
        db.insertIntoBuyer(userid, firstName, lastName, profile, email, password, whatsapp, telegramID = telegram, alternateNumber = alternate, paytmNumber=paytm, gpayNumber=gpay, UPI=upi, bankname="None", accountNumber=account, ifsc=ifsc)
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
        return redirect("/buyerDashboard")
    except Exception as e:
        print(e)
        return redirect("/")


@app.route("/selectmanager/<campId>")
def selectmanagers(campId):
    if session.get("name"):
        managers = db.getAllManagers()
        return render_template('select_manager.html',managers=managers,campID = campId)


@app.route("/allocatemanagers",methods=['POST'])
def allocate():
    if session.get("name"):
        managers = request.form.getlist("managers")
        quantities = request.form.getlist("quantity")
        campId = request.form.get("campId")
        for i in range(len(managers)):
            managers[i] = managers[i].split(" ")
            managers[i].append(quantities[i])
        for man in managers:
            db.insertIntoAllocate(campId,man[0],man[3])
        return redirect("/viewCampaigns")


if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)