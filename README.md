# Client and server Script using GUI (ITNE352 Project)

# Project Description
This project involves creating two Python scripts: a client script and a server script.
The client script features a graphical user interface (GUI) that displays a main menu with several submenus for the user to interact with.
The server script listens for incoming requests from the client and responds by retrieving relevant news data from an external API using NewsAPI (https://newsapi.org/)

**Group**: A16

**Course code**: ITNE352

**Section**: 1

**Semester**: First Semester 2024-2025

**Student names & IDs:**
1. Name: Hawra Fadhel Abbas           ID: 202208944 
2. Name: Noora Salah Alkhalaqi        ID: 202209541

## Table of Contents:
1. Requirements
2. How to run the system
3. Explanation of clientScript.py 
4. Explanation of serverScript.py 
5. Additional concepts
6. Acknowledgments
7. Conclusion


## Requirements

## How to run the system

## Explanation of clientScript.py

## Explanation of serverScript.py 
The serverScript.py handles communication between the client and the News API. It listens for client requests, retrieves news data (like headlines or sources) from the API, and sends the response back to the client.

- Key functions:

Socket Communication: The server uses Python's socket library to create a TCP server that listens for incoming connections on a specified port (65432). When a client connects, the server accepts the connection and starts a new thread to handle the interaction with the client.

Multithreading: The server can handle multiple clients simultaneously using threads. Each client’s requests are handled in separate threads, ensuring that the server remains responsive even with multiple users.

Request Parsing: When the server receives a request, it parses the request string (which includes parameters such as the request type and search criteria). Based on the request, it constructs the appropriate API query for fetching news data.

Data Fetching: The server sends a request to the News API (https://newsapi.org/) with the appropriate parameters (such as category, country, or keyword) and retrieves the news data in JSON format. If the request is successful, the server processes the data and extracts relevant details such as the article title, source, description, and publication date.

Data Response: After processing the data, the server sends the news articles (or sources) back to the client in a serialized format using pickle. The client can then display the results in the user interface.

Error Handling: The server handles any errors that occur during the request process, such as network errors or invalid API responses, and returns appropriate error messages to the client.

Data Saving: For each client request, the server saves the fetched data into a JSON file, which includes details like the client’s name, request type, and the results fetched. This provides a record of the requests and the data returned.

## Additional concepts

## Acknowledgments

## Conclusion



