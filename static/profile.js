console.log("hello world");
const heading = document.querySelector(".navbar-brand.anchor"),
    corrnavUl = document.querySelector(".nav.navbar-nav.navbar-right"),
    correlations = document.querySelectorAll(".section-items")[3],
    corrheader = document.querySelectorAll(".row.header");
heading.innerHTML = "Exploratory Data Analysis";
heading.style.fontWeight = "bold";
heading.style.fontSize = "25px";

//Inclusion of tags
document.head.innerHTML += '<link rel="preconnect" href="https://fonts.googleapis.com">'
document.head.innerHTML += '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
document.head.innerHTML += '<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300&display=swap" rel="stylesheet"></link>'
document.body.style.fontFamily = "Nunito"

//Correaltion Removal and new Navtag with Changing of Header Names
correlations.style.display = "none";
corrheader[3].style.display = "none";
corrheader[2].children[1].innerText = "Scatter Plots";
corrheader[5].children[1].innerText = "Sample Rows";
corrnavUl.children[3].style.display = "none";
const Next = document.createElement('li');
Next.innerHTML = '<a class="anchor" href="#sample">Next</a>'
corrnavUl.appendChild(Next);

//changing text of Nav
corrnavUl.children[2].children[0].innerHTML = "Scatter Plots";
corrnavUl.children[5].children[0].innerHTML = "Sample Rows";

//New Buttons
/* <button type="button" class="btn btn-primary btn-lg">Large button</button>
<button type="button" class="btn btn-secondary btn-lg">Large button</button> */
const nextPage = document.createElement('div');
const Cluster = document.createElement('a'),
    Regression = document.createElement('a');
nextPage.append(Cluster);
nextPage.append(Regression);
// console.log(Cluster.children)
Cluster.innerHTML = '<button type="button" class="btn btn-primary btn-lg"><i class="bi bi-arrow-left"></i>Clustering</button>';
Regression.innerHTML = '<button type="button" class="btn btn-primary btn-lg">Prediction</button>';
Cluster.children[0].style.margin = "10px";
Cluster.children[0].style.width = "140px";
Regression.children[0].style.margin = "10px";
Regression.children[0].style.width = "140px";
Regression.children[0].style.marginRight = "70px";
document.body.append(nextPage);
nextPage.style.display = "flex"
nextPage.style.margin = "30px"
nextPage.style.justifyContent = "End"
Cluster.href = "clustering_before"
Regression.href = "prediction_before"

// RaKo PCA
const pca = document.createElement('a');
nextPage.append(pca);
pca.innerHTML = '<button type="button" class="btn btn-primary btn-lg"><i class="bi bi-arrow-left"></i>PCA</button>';
pca.children[0].style.marginRight = "70px";
pca.children[0].style.margin = "10px";
pca.children[0].style.width = "140px";
pca.href = "pca_before"

//footer removal
document.querySelector(".row.center-block.footer-text").style.display = "none";


