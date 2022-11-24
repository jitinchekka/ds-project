from flask import Flask
from flask import request
from flask import render_template
import pandas as pd
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("upload.html")

@app.route('/success',methods=["POST"])
def success():
	if request.method=='POST':
		f=request.files['file']
		f.save(f.filename)
		df=pd.read_csv(f.filename)
		describe = df.describe()
		describe.round(2)
		print("Describe\n",describe)
		stat = describe.head().index.values
		return render_template("success.html",columns=df.columns,n=len(df.columns),describe=describe,stat=stat)
		# return render_template("success.html",name=f.filename)
if __name__ == "__main__":
	
	app.run(host="127.0.0.1", port=8080, debug=True)