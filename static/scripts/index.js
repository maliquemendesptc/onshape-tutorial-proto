// JavaScript function which can be called in the client
function validate(){
  var result = 5;
  console.log(result);

  
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
    }
  };
  xhttp.open("GET", "validate", true);
  xhttp.send();
}