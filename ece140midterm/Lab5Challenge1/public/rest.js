  function age_range() {
    let age_range_id = document.getElementById('anAge').value;
     console.log(age_range_id)
    if(age_range_id.trim() === "") {
      console.log("No ID provided");
      document.getElementById("error").textContent = "You have not provided an Age ID";
    }
    else {
      let theURL = '/age_range/'+age_range_id;
      console.log("Starting executing single id");
      document.getElementById("error").textContent = "";
      fetch(theURL)
        .then(response=>response.json())
        .then(function(response) {
          for(var key in response) {
            document.getElementById(key).textContent 
               = key.toUpperCase() + ": " + response[key]
          }

            let photo_id1 = document.getElementById('id').innerHTML
            let result = photo_id1.replace("ID: ","")
           let photo = parseInt(result)
           console.log(photo)
            document.getElementById('textInput').value = photo
            click_display()
        });
    }
  }
  

  function height_range() {
    let height_range_id = document.getElementById('aHeight').value;
    console.log(height_range_id)
    if(height_range_id.trim() === "") {
      console.log("No ID provided");
      document.getElementById("error").textContent = "You have not provided an height ID";
    }
    else {
      let theURL = '/height_range/'+height_range_id;
      console.log("Starting executing single id");
      document.getElementById("error").textContent = "";
      fetch(theURL)
        .then(response=>response.json())
        .then(function(response) {
          for(var key in response) {
            document.getElementById(key).textContent 
               = key.toUpperCase() + ": " + response[key]
          }
          let photo_id1 = document.getElementById('id').innerHTML
          let result = photo_id1.replace("ID: ","")
           let photo = parseInt(result)
           console.log(photo)
          document.getElementById('textInput').value = photo
          click_display()
        });
    }
  }


function display() {
   // Get the current value from the text input box
   let photo_id1 = document.getElementById('id').innerHTML
   let result = photo_id.replace("ID: ","")
   let photo_id = parseInt(result)
   document.write(photo_id);
   alert("photoId"+photo_id)
   print()
   // This URL path is going to be the route defined in app.py
   let theURL='/photos/'+photo_id
   // This logger is just to keep track of the function call.
   // You can use such log messages to debug your code if you need.
   console.log("Making a RESTful request to the server!")
   // fetch is a Javascript function that sends a request to a server
   fetch(theURL)
       .then(response=>response.json()) // Convert response to JSON
       // Run the anonymous function on the received JSON response
       .then(function(response) {
           // Set the value of the img_src attribute of the img tag
           // to the value received from the server
           let img = document.getElementById('image')
           img.src = response['img_src']
       });
 }



function click_display() {
   // Get the current value from the text input box
   let photo_id = document.getElementById('textInput').value

   // This URL path is going to be the route defined in app.py
   let theURL='/photos/'+photo_id;
   // This logger is just to keep track of the function call.
   // You can use such log messages to debug your code if you need.
   console.log("Making a RESTful request to the server!")
   // fetch is a Javascript function that sends a request to a server
   fetch(theURL)
       .then(response=>response.json()) // Convert response to JSON
       // Run the anonymous function on the received JSON response
       .then(function(response) {
           // Set the value of the img_src attribute of the img tag
           // to the value received from the server
           let img = document.getElementById('image')
           img.src = response['img_src']
       });
 }

 function click_price(){
       // Get the current value from the text input box
   let photo_id = document.getElementById('textInput').value

   // This URL path is going to be the route defined in app.py
   let theURL='/price/'+photo_id;
   // This logger is just to keep track of the function call.
   // You can use such log messages to debug your code if you need.
   console.log("Making a RESTful request to the server!")
   // fetch is a Javascript function that sends a request to a server
   fetch(theURL)
       .then(response=>response.json()) // Convert response to JSON
       // Run the anonymous function on the received JSON response
       .then(function(response) {
       document.getElementById('price').innerHTML = response;

       //img.src = response['']
       });
}