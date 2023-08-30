from flask import Flask
from flask import request
from flask import render_template
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import  ydata_profiling as pp
from sklearn.cluster import KMeans
# from sklearn import preprocessing
from sklearn import linear_model
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

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


file_name = "diabetes.csv"
# file_name = "landslide_data3_miss.csv"


@app.route("/success", methods=["POST"])
def success():
	if request.method == "POST":
		# check if the post request has the file part
		if "file" not in request.files:
			flash("No file part")
			return redirect(request.url)
		f = request.files["file"]
		file_name = f.filename
		f.save(f.filename)
		# If the file is not one of the allowed types, we return an error
		if not allowed_file(f.filename):
			return "File type is not allowed", 400
		df = pd.read_csv(f.filename)
		profile = pp.ProfileReport(df)
		# Save the report as an HTML file in templates folder
		profile.to_file(output_file="templates/profile.html")

		# Add <script> tag to the HTML file to load the JS file
		fd = open("templates/profile.html", "a")
		fd.write("<script src='/static/profile.js'></script>")
		fd.close()
		return render_template("profile.html")
		# return render_template("success.html",name=f.filename)
	# If user does not select file, show an error message
	else:
		return render_template("upload.html")


@app.route("/pca_before")
def pca_before():
	f = file_name
	df = pd.read_csv(f)
	# n=number of columns

	return render_template("pca_before.html", columns=len(df.columns))


@app.route("/pca_after", methods=["POST"])
def pca():
	# Print the request object
	print(request.form)
	f = file_name
	df_copy = pd.read_csv(f)
	n_components = int(request.form["n_components"])
	# Preprocessing
	df_copy = df_copy.dropna()
	df_copy = df_copy.drop_duplicates()
	# df_copy = df_copy.drop(["Outcome"], axis=1)
	# Standardize the data
	X = StandardScaler().fit_transform(df_copy)
	# PCA
	pca = PCA(n_components=n_components)
	principalComponents = pca.fit_transform(X)
	# Create a dataframe with the principal components
	principalDf = pd.DataFrame(data=principalComponents)
	print(principalDf)
	columns = len(principalDf.columns)
	print(columns)
	return render_template("pca_after.html", n=columns, principalDf=principalDf.values)


@app.route("/clustering_before")
def kmeans():
	f = file_name
	df = pd.read_csv(f)
	return render_template("clustering.html", columns=df.columns.values)


@app.route("/clustering_after", methods=["POST"])
def clustering():
	# Print the values of the form
	print(request.form)
	if request.method == "POST":
		f = file_name
		i = request.form["x"]
		j = request.form["y"]
		n = int(request.form["x_value"])
		print("n=", n)
		df = pd.read_csv("diabetes.csv")
		print(i, j)
		# Sklearn K means clustering
		kmeans = KMeans(n_clusters=n).fit(df[[i, j]])
		# Plot the clusters with cluster centers
		matplotlib.pyplot.scatter(
			df[i], df[j], c=kmeans.labels_.astype(float), s=50, alpha=0.5
		)
		matplotlib.pyplot.xlabel(i)
		matplotlib.pyplot.ylabel(j)
		matplotlib.pyplot.title("K means clustering")
		# Save the plot as a png file in static folder
		matplotlib.pyplot.savefig("static/{}_{}.png".format(i, j))
		#Clear the plot
		matplotlib.pyplot.clf()
		# Return the plot to the user
		graph = "{}_{}.png".format(i, j)
		print("Graph is ", graph)
		# graphs.append(fig)
		print(df.columns)
	return render_template("rako_k_means.html", columns=df.columns, graph=graph)
	# return render_template("kmeans.html",columns=df.columns)


@app.route("/prediction_before")
def prediction():
	f = file_name
	df = pd.read_csv(f)
	return render_template("prediction_before.html", columns=df.columns.values)


@app.route("/prediction_after", methods=["POST"])
def prediction_after():
	print("POST request", request.form)
	x_column = request.form["x"]
	y_column = request.form["y"]
	x_value = float(request.form["x_value"])
	df = pd.read_csv(file_name)
	# Split the data into training/testing sets
	diabetes_X_train = df[x_column][:-20]
	diabetes_X_test = df[x_column][-20:]
	diabetes_y_train = df[y_column][:-20]
	diabetes_y_test = df[y_column][-20:]

	# Create linear regression object
	regr = linear_model.LinearRegression()
	# Train the model using the training sets
	regr.fit(diabetes_X_train.values.reshape(-1, 1), diabetes_y_train)
	# Make predictions using the testing set
	diabetes_y_pred = regr.predict(diabetes_X_test.values.reshape(-1, 1))

	# The coefficients
	print("Coefficients: ", regr.coef_)
	# The mean squared error
	print(
		"Mean squared error: %.2f"
		% mean_squared_error(diabetes_y_test, diabetes_y_pred)
	)
	predicted_value = regr.predict([[x_value]])
	print("Predicted value: ", predicted_value)
	# The coefficient of determination: 1 is perfect prediction
	coef = r2_score(diabetes_y_test, diabetes_y_pred)
	print(
		"Coefficient of determination: %.2f"
		% r2_score(diabetes_y_test, diabetes_y_pred)
	)

	# Plot output
	matplotlib.pyplot.scatter(diabetes_X_test, diabetes_y_test, color="black")
	matplotlib.pyplot.plot(diabetes_X_test, diabetes_y_pred, color="blue", linewidth=3)
	matplotlib.pyplot.xlabel(x_column)
	matplotlib.pyplot.ylabel(y_column)
	matplotlib.pyplot.title("Linear Regression")
	matplotlib.pyplot.savefig("static/{}_{}.png".format(x_column, y_column))
	# clear the plot
	matplotlib.pyplot.clf()
	graph = "{}_{}.png".format(x_column, y_column)
	return render_template(
		"prediction_after.html",
		graph=graph,
		predicted_value=predicted_value.item(),
		columns=df.columns,
		m=regr.coef_[0],
		c=regr.intercept_,
		coef=coef,
	)


if __name__ == "__main__":

	app.run(host="127.0.0.1", port=8080, debug=True)
