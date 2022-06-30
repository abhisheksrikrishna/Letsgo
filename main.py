import json
from flask import Flask,request,render_template
import requests
app = Flask(__name__)
   
def helper(result,ll,ul,wt):
   sum=0
   sump=0
   sumt=0
   for i in range(ll,ul):
      sum+=(result["overallattperformance"]["overall"][i]["percentage"]+result["overallattperformance"]["overall"][i]["practical"])
      sump+=result["overallattperformance"]["overall"][i]["practical"]
      sumt+=result["overallattperformance"]["overall"][i]["percentage"]
      print(result["overallattperformance"]["overall"][i]["percentage"]+result["overallattperformance"]["overall"][i]["practical"])
   average=sum/(ul-ll+1)
   sumpa=sump/3
   sumta=sumt/5
   final_avg=(sumpa*(6-wt)+sumta*wt)/6
   return final_avg

def llfinder(stuinfo):#used to find the upper limit of the range for subjects
   dep=stuinfo["dept"]
   print(dep)
   year=stuinfo["currentyear"]
   print(year)
   if((dep=="CSE")and(year=='2')):
      limit=9
   elif((dep=="IT")and(year=='2')):
      limit=9
   elif((dep=="CSM")and(year=='2')):
      limit=9
   elif((dep=="CSD")and(year=='2')):
      limit=8
   elif((dep=='CSE')and(year=='3')):
      print("right")
      limit=14
   elif((dep=="IT")and(year=='3')):
      limit=12
   elif((dep=="ECE")and(year=='3')):
      limit=8
   elif((dep=="EIE")and(year=='3')):
      limit=9
   else:
      limit=0
   
   return limit

def ulfinder(stuinfo):#used to find the lower limit of range of subjects
   dep=stuinfo["dept"]
   year=stuinfo["currentyear"]
   if((dep=="CSE" )and(year=='2')):
      limit=15
   elif((dep=="IT")and(year=='2')):
      limit=16
   elif((dep=="CSM")and(year=='2')):
      limit=16
   elif((dep=="CSD")and(year=='2')):
      limit=16
   elif((dep=="CSE")and(year=='3')):
      limit=21
   elif((dep=="IT")and(year=='3')):
      limit=19
   elif((dep=="ECE")and(year=='3')):
      limit=17
   elif((dep=="EIE")and(year=='3')):
      limit=15
   else:
      limit=0
   
   return limit

def weightt(stuinfo):#used to calculate the weight of the theoretical subjects in calculation of final
   if(stuinfo["currentyear"]=='3'):
      weight=4.5
   elif(stuinfo["currentyear"]=='2'):
      weight=5
   else:
      weight=0
   return weight



@app.route('/',methods = ["GET","POST"])
def hello_world():
   if(request.method=="POST"):
        netra = request.form.get("nid")
        payload={"method": "314","rollno": netra}
        stu={"method" : "32", "rollno": netra}
        stinfo = requests.post('http://teleuniv.in/netra/api.php',data=json.dumps(stu))#request for student data
        att = requests.post('http://teleuniv.in/netra/api.php',data=json.dumps(payload))#request for attendance inforamtion
        result=att.json()
        stuinfo=stinfo.json()
        upperl=ulfinder(stuinfo)
        lowerl=llfinder(stuinfo)
        wt=weightt(stuinfo)
        for i in range(upperl):
            if(result["overallattperformance"]["overall"][i]["percentage"]=="--"):
                     result["overallattperformance"]["overall"][i]["percentage"]=0.00
            if(result["overallattperformance"]["overall"][i]["practical"]=="--"):
                     result["overallattperformance"]["overall"][i]["practical"]=0.00
        fin=helper(result,lowerl,upperl,wt)
        return (render_template("result.html",data=result,info=stuinfo,final=fin,ul=upperl,ll=lowerl,wt=wt))
   else:
         print("Not happening")
         print(132)
         return render_template("index.html")


if __name__ == '__main__':
   app.run(debug = True)