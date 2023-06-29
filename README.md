# Search Engine

This is a simple search engine application that allows users to upload, search, and view documents.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

- **Upload documents**: The application supports uploading of .txt and .pdf files. The contents of the uploaded files are stored in a database for later search and retrieval.

- **Search documents**: Users can enter a search query to search the uploaded documents. The search algorithm scans the database for documents that match the query and returns the top 3 matches. Each search result includes the title of the document and a snippet of text that matches the query.

- **View documents**: Users can view a list of all the uploaded documents. The list includes the title of each document and a preview of its contents.

## Tech Stack

- **Front-end**: The application uses [Streamlit](https://streamlit.io/), a fast and easy way to create data apps.

- **Database**: The documents are stored in a database. The application uses environment variables for the database connection configuration.

## Setup

1. Clone this repository to your local machine.

2. Set up the following environment variables for the database connection:
    - `PASSWORD`: Your database password
    - `HOST`: The host of your database
    - `DBNAME`: The name of your database
    - `USER`: Your database username
    - `PORT`: The port your database is running on

3. Install the necessary Python packages by running `pip install -r requirements.txt`.

4. Run the application with the command: `streamlit run main.py`.

## Usage

Navigate to the application in your web browser. You will see a sidebar with four options: "Home", "Upload Document", "Search", and "View Documents". Use these options to interact with the application.

## Contributing

We welcome contributions to this project. Please fork this repository, make your changes, and submit a pull request.
