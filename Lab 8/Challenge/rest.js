function click_buzz(){
    let theURL = '/buzzIt/';
    console.log("Starting executing buzz");
    fetch(theURL)
}

function click_led(){
    let theURL = '/ledIt/';
    console.log("Starting executing led");
    fetch(theURL)
}


 function distance_range() {
    let distance_range_id = document.getElementById('aDistance').value;
    console.log(distance_range_id)
    if(distance_range_id.trim() === "") {
      console.log("No ID provided");
      document.getElementById("error").textContent = "You have not provided an distance ID";
    }
    else {
      let theURL = '/distance_range/'+distance_range_id;
      console.log("Starting executing single id");
      document.getElementById("error").textContent = "";
      fetch(theURL)
 for(var key in response) {
            document.getElementById(key).textContent
               = key.toUpperCase() + ": " + response[key]
          }
        });
    }
  }


  function time_rank() {
    let time_rank_id = document.getElementById('aTimeRank').value;
    console.log(time_rank_id)
    if(time_rank_id.trim() === "") {
      console.log("No ID provided");
      document.getElementById("error").textContent = "You have not provided an time ID";
    }
    else {
      let theURL = '/time_rank/'+time_rank_id;
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