# Search Engine

This is an enhanced version of a simple search engine application that allows users to upload, search, view, and delete documents.

## Table of Contents

  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Features

  - **Upload Documents**: The application supports uploading of .txt, .pdf, .csv, and image files. The contents of the uploaded files are stored in a database for later search and retrieval.

  - **Search Documents**: Users can enter a search query to search the uploaded documents. The search algorithm scans the database for documents that match the query and returns the top 5 matches. Each search result includes the title of the document and a snippet of text that matches the query.

  - **View Documents**: Users can view a list of all the uploaded documents. The list includes the title of each document and a preview of its contents.

  - **Delete Documents**: Users can now delete documents from the database.
  - **Download Article from Guardian**: Users can download the 10 newest articles from Guardian Open-source API.

## Tech Stack

  - **Front-end**: The application uses Streamlit, a fast and easy way to create data apps.
  - **Database**: The documents are stored in a PostgreSQL database. The application uses environment variables for the database connection configuration.

## Setup

  1. Clone this repository to your local machine.
  2. Set up the following environment variables for the database connection:
     - `PASSWORD`: Your database password
     - `HOST`: The host of your database
     - `DBNAME`: The name of your database
     - `USER`: Your database username
     - `PORT`: The port your database is running on
     - `GUARDIAN_API_KEY`: You can find the key [here](https://open-platform.theguardian.com/)

  3. Install the necessary Python packages by running `pip install -r requirements.txt`.
  4. Run the application with the command: `streamlit run main.py`.

## Usage

Navigate to the application in your web browser. You will see a sidebar with five options: "Home", "Upload Document", "Search", "View Documents","Delete Documents" and "Download Guardian Articles". Use these options to interact with the application.

## Contributing

We welcome contributions to this project. If you want to contribute, please fork this repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss the proposed change.

## License

This project is licensed under the terms of the MIT License.
