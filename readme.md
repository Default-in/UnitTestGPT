# genAI Project

genAI is a project consisting of three main layers: frontend, service layer, and backend. Each layer plays a crucial role in the overall functioning of the project.

## First Layer - Frontend

The first layer serves as the user interface, where a Google Sheet acts as the platform for user interactions. Users can input data into the Google Sheet, and this data is then sent to the service layer for processing. The first layer provides the following functions:

1. `get_data()`: This function allows the frontend to fetch data from the Google Sheet.
2. `write_data(data)`: This function enables the frontend to write data to the Google Sheet.

### How to Use the First Layer

To utilize the first layer effectively, follow these steps:

1. Create a Google Sheet and share it with the email ID: `openai@generativeai-393802.iam.gserviceaccount.com`.
2. The Google Sheet should be in the specified format, which can be found here: [Google Sheet Format](https://docs.google.com/spreadsheets/d/1ZqR_pt8DFvfS19S11x4VUqJtHBRE5up9hkWj2sd3ETw/edit?usp=sharing).
3. Update the Google Sheet name in the `constants.py` file. By default, the Google Sheet tab name is "Sheet1."

## Second Layer - Service Layer

The second layer acts as the service layer, where the received data from the frontend is processed before being sent to the backend. This layer facilitates communication between the frontend and the backend.

### How to Use the Second Layer

--------------------
## Third Layer - Backend

The backend is the core of the genAI project, responsible for the actual interaction with the OpenAI API. It houses various functions that perform tasks like requesting chat credits, monitoring usage, performing completions, handling chat interactions, generating embeddings, and fine-tuning models.

The backend consists of the following functions:

1. `chatgpt_credits()`: Retrieves information about the remaining credits for the OpenAI API.
2. `chatgpt_usage(start_date, end_date)`: Provides usage statistics for the OpenAI API within the specified date range.
3. `completion()`: Handles basic completions using the OpenAI GPT-3.5 model.
4. `chat_completion()`: Manages chat-based completions using the OpenAI GPT-3.5 model.
5. `embeddings()`: Generates embeddings for the given text using the OpenAI model.
6. `fine_tune()`: Performs fine-tuning of the OpenAI GPT-3.5 model for specialized tasks.
### How to Use the Third Layer

To utilize this layer, you will need two keys:

1. OpenAI API key
2. OpenAI Bearer Token

#### How to Get the OpenAI API Key

1. Log in to the OpenAI platform: https://platform.openai.com/apps
2. Select the API section.
3. Click on your profile icon located in the top right corner.
4. Choose "View API key."
5. Create a new API key and copy it.
6. Note that the API key might not be visible again, so be sure to copy it and store it securely.

#### How to Get the OpenAI Bearer Token

1. Log in to the OpenAI platform: https://platform.openai.com/apps
2. While logging in, open the inspect window in your browser.
3. Under the network tab, examine the response from the URL: https://auth0.openai.com/oauth/token
4. Copy the access token from the response.

By following these steps, you will obtain both the OpenAI API key and the OpenAI Bearer Token, which are essential for accessing and using the third layer of the genAI project.

