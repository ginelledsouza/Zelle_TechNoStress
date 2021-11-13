from flask import Flask, render_template, request
import ZelleDatabase as zb
import Visuals as vi
import TechNews

app=Flask(__name__,template_folder='template')

@app.route('/')
@app.route('/Main.html')
def Main():
    Top = vi.Top
    return render_template("Main.html", TopTech = Top)

@app.route('/Computers.html', methods=['GET','POST'])
def Computers():
    
    flag = 0
    laptop = vi.MainLaptop()

    if request.method == 'POST':
       Brand = request.form.getlist('Brand')
       ROM = request.form.getlist('ROM')
       RAM = request.form.getlist('RAM')
        
       laptop, flag = vi.LaptopFilter(Brand,RAM,ROM)

    return render_template("Computers.html", Laptop = laptop, Flag=flag)

@app.route('/Contact.html')
def Contact():
    return render_template("Contact.html")


@app.route('/News.html')
def News():
    
    NewsJson = TechNews.TechnicalNews
    TopNewsJson = TechNews.TopTechnicalNews
    return render_template("News.html", News = NewsJson, TopNews = TopNewsJson)

@app.route('/Phone.html', methods=['GET','POST'])
def Phone():
    
    flag = 0
    phone = vi.MainPhone()

    if request.method == 'POST':
        Brand = request.form.getlist('Brand')
        ROM = request.form.getlist('ROM')
        RAM = request.form.getlist('RAM')

        phone, flag = vi.PhoneFilter(Brand,RAM,ROM)
    
    return render_template("Phone.html", Phone=phone, Flag=flag)

@app.route('/Predictor.html', methods=['GET','POST'])
def Predictor():
    
    if request.method == 'POST':
        Predict = {}
        Device = request.form.getlist('Device')
        Predict['Device'] = Device
        
        Function = request.form.getlist('Function')
        Predict['Function'] = Function
        
        Photograph = request.form.getlist('Photograph')
        Predict['Photograph'] = Photograph
        
        Usage = request.form.getlist('Usage')
        Predict['Usage'] = Usage
        
        Cost = request.form.getlist('Cost')
        Predict['Cost'] = Cost
        
        zb.dataforprediction(Device,Function,Photograph,Usage,Cost)
        usertype,flag = vi.PredictionVisuals(Predict)
        
        if flag != 1:
            return render_template("PredictionResults.html", UserType=usertype)
        else:
            return render_template("Predictor.html", Flag=flag)
        
    return render_template("Predictor.html")

@app.route('/Tablets.html', methods=['GET','POST'])
def Tablets():
    
    flag = 0
    tablet = vi.MainTablet()
    
    if request.method == 'POST':
        Brand = request.form.getlist('Brand')
        ROM = request.form.getlist('ROM')
        RAM = request.form.getlist('RAM')
        
        tablet, flag  = vi.TabletFilter(Brand,RAM,ROM)

    return render_template("Tablets.html", Tablet = tablet, Flag=flag)

@app.route('/Feedback.html', methods=['GET','POST'])
def Feedback():
    if request.method == 'POST':
        Heard = request.form.getlist('Heard')
        Recommendation = request.form.getlist('Recommendation')
        Satisfaction = request.form.getlist('Satisfaction')
        Experience = request.form.getlist('Experience')
        Change = request.form.getlist('Change')
        
        zb.dataforfeedback(Heard,Recommendation,Satisfaction,Experience,Change)

    return render_template("Feedback.html")

@app.route('/Analytics.html')
def Analytics():
    return render_template("Analytics.html")

@app.route('/ThankYou.html', methods=['GET','POST'])
def ThankYou():
    return render_template("ThankYou.html")

if __name__ == "__main__":
    app.run(debug=True)