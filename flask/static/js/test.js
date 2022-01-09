if ("{{result}}".toString() == "error") {
    document.getElementById("success").setAttribute("style","display:none");  
    document.getElementById("error").setAttribute("style","display");  
}
else{
    document.getElementById("error").setAttribute("style","display:none");  
    document.getElementById("success").setAttribute("style","display");  
}
alert("result");