

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
    if(object_rank_id.trim() === "") {
      console.log("No ID provided");
      document.getElementById("error").textContent = "You have not provided an object ID";
    }
    else {
      let theURL = '/object_rank/'+object_rank_id;
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