# **Hotel Recommendation System**
## **Description**
Despite the fact that there are a bunch of websites recommending hotel options based on customer preferences, there is no example in the market that will find your preferred place based on the prompt that the user will provide and will be based on information like hotel description, vicinity description, reviews and amenities at the same time. So this project aims to address that issue and recommmend the top 5 hotels that will most suit the prompt of the user. The model is constructed on a 10-hotel dataset in Rome, however in the future it can be enhanced in case there are enough computational resources.

## **Installation Guide**
To get this project up and running on your local machine, follow these steps:
1. Prerequisites
Ensure you have Python 3.8 or higher installed on your machine.
2. Clone the Repository
Start by cloning the repository to your local machine with this:
- git clone https://github.com/sonahakobyannn/Hotel_Recommendation_system.git
3. Install Dependencies
This project relies on several Python libraries. Install them using pip:
- pip install -r requirements.txt

## **Usage**
1. Run the data_preparation.py file to read the initial data, clear unnecessary columns, group the top 10 comments by hotel id, truncate the data up to 10 hotels and get the final dataframe that model will eventually work on.
2. Run chroma.py file to create database containing the ids of hotels and each of their openai embeddings based on the textual data
3. Run in the command line "streamlit model_and_app.py" to see the web representation
4. enter the prompt and get your results!
