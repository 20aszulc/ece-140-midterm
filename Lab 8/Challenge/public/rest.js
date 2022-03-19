function find_location(){
var x = document.getElementById("Latitude");
var y = document.getElementById("Longitude");
console.log("find location")
 if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);

  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
var x = document.getElementById("Latitude");
var y = document.getElementById("Longitude");
  x.innerHTML =  position.coords.latitude
      y.innerHTML =  position.coords.longitude;
}

 function store_location() {
    fetch("/store_location")
    .then(response=>response.json())
        .then(function(response) {
        document.getElementById("object_list").innerHTML = response;

        });
  }


  function find_object() {
    let object_rank_id = document.getElementById('objectChosen').value;
    console.log(object_rank_id)
    let latitude = document.getElementById("Latitude").innerHTML;
    let longitude = document.getElementById("Longitude").innerHTML;
    console.log("This is latitude"+latitude)
    if(object_rank_id === "" || longitude ==="") {
      console.log("No ID provided");
      document.getElementById("error").textContent = "You have not provided an object ID";
    }
    else {
      let theURL = '/object_rank/'+object_rank_id+'/'+ String(latitude)+'/'+String(longitude);
      console.log(theURL);
      console.log("Starting executing single id");
      document.getElementById("error").textContent = "";
      fetch(theURL)
        .then(response=>response.json())
        .then(function(response) {
          for(var key in response) {
            document.getElementById(key).textContent 
               = key.toUpperCase() + ": " + response[key]
          }
        });
    }
  }