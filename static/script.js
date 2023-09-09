document.addEventListener("DOMContentLoaded", function() { //ensures JavaScript code is executed after the page has fully loaded
    
    //get references to form and result elements using their IDs
    const form = document.getElementById("itinerary-form"); //get the form element
    const resultDiv = document.getElementById("itinerary-result"); //get the div where the result will be displayed
    
    //add an event listener to the form for the submit event
    form.addEventListener("submit", async function(event) {
       
        //prevent refreshing the page (default form submission behavior)
        event.preventDefault();
        
        //get values from the user's input fields
        const destination = document.getElementById("destination").value;
        const interests = document.getElementById("interests").value;
        const schedule = document.getElementById("schedule").value;

        
        try {
            //send a POST request to the "/generate-itenerary" endpoint on Flask server (found in travel.py)
            const response = await fetch("http://127.0.0.1:5001/generate-itinerary", {
                method: "POST", //use POST method to send data
                headers: {
                    "Content-Type": "application/json", //specify the request body is JSON
                },
                body: JSON.stringify({destination, interests, schedule}), //convert data to JSON format and send it in the body
            });

            // Log the response content to the console for debugging
            // console.log(await response.text());

            //check if the response status is okay (HTTP status 200)
            if (!response.ok) {
                throw new Error("Error generating itinerary"); //if not okay, throw an error
            }

            //parse the JSON response data
            const data = await response.json();

            //display the generated itinerary in the resultDiv
            resultDiv.innerText = data.itinerary;

        } catch (error) {
            console.error("An error occurred:", error); //log any errors to the console
            resultDiv.innerText = "An error occurred: " + error.message; //display the server error message
        }
    });
});
