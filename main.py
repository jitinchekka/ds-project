from flask import Flask
from flask import request
from flask import render_template
import pandas as pd
import matplotlib.pyplot as plt
import pandas_profiling as pp

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("upload.html")


# These are the extension that we are accepting to be uploaded
app.config["ALLOWED_EXTENSIONS"] = set(
	["txt", "pdf", "png", "jpg", "jpeg", "gif", "csv"]
)


def allowed_file(filename):
	return (
		"." in filename
		and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
	)


@app.route("/success", methods=["POST"])
def success():
	if request.method == "POST":
		# check if the post request has the file part
		if "file" not in request.files:
			flash("No file part")
			return redirect(request.url)
		f = request.files["file"]
		f.save(f.filename)
		# If the file is not one of the allowed types, we return an error
		if not allowed_file(f.filename):
			return "File type is not allowed", 400
		df = pd.read_csv(f.filename)
		profile=pp.ProfileReport(df)
		# Save the report as an HTML file in templates folder
		profile.to_file(output_file="templates/profile.html")

		# Add <script> tag to the HTML file to load the JS file
		fd=open("templates/profile.html","a")
		fd.write("<script src='/static/profile.js'></script>")
		fd.close()
		return render_template("profile.html")
		# return render_template("success.html",name=f.filename)
	# If user does not select file, show an error message
	else:
		return render_template("upload.html")

@app.route("/kmeans")
def kmeans():
	return render_template("kmeans.html")

if __name__ == "__main__":

	app.run(host="127.0.0.1", port=8080, debug=True)
