from flask import Flask, request, jsonify
from flask_cors import CORS # import CORS from flask_cors
import openai
import os

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Set OpenAI API key
#openai.api_key = os.getenv("OPENAI_API_KEY") # using environment var to keep API key secret
openai.api_key = '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'

@app.route('/')
def home():
    # serve the static HTML file located at the root path
    return app.send_static_file('index.html')


@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        # Get user inputs from frontend request (assumes JSON input)
        data = request.json
        destination = data['destination']
        interests = data['interests']
        schedule = data['schedule']

        # Check if required data is provided
        if not destination or not interests or not schedule:
            raise ValueError("Missing required input data")

        # Construct a prompt for the ChatGPT API
        #prompt = f"Create a travel itinerary for a trip to {destination} with the following details: The traveler is interested in {interests}. The trip is scheduled for {schedule}. "
        #prompt = f"Create a travel itinerary for a trip to china. The traveler is interested in cultural food. The trip is scheduled for december."
        messages = [
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": f"Create a travel itinerary for a trip to {destination} with the following details: The traveler is interested in {interests}. The trip is scheduled for {schedule}."}
        ]

        # Make an API request to ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ChatGPT engine
            messages=messages,
            max_tokens=1000, # Adjust the number of tokens as needed
            #temperature=0.2, # Control the randomness of the response (0 for deterministic)
        )

        #DEBUGGING
        #print(response)

        # Extract and return the generated itinerary from the API response
        itinerary = response['choices'][0]['message']['content'].strip()

        #DEBUGGING
        #print(itinerary)

        return jsonify({'itinerary': itinerary})

    except ValueError as ve:
        # Handle missing input data errors with a 400 Bad Request response
        return jsonify({'error': str(ve)}), 400  # Bad Request

    except openai.error.OpenAIError as ai_err:
        # Handle OpenAI API errors and log the error message
        app.logger.error(f"OpenAI API error: {str(ai_err)}") # log the OpenAI API error message
        return jsonify({'error': str(ai_err)}), 500  # Internal Server Error

    except Exception as e:
        # Handle unexpected errors with a 500 Internal Server Error response
        return jsonify({'error': str(e)}), 500

# start Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)