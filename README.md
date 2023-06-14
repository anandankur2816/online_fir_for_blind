# online_fir_for_blind
Online fir helping blind people for hackathon.
Voice-Enabled online FIR Filling System for Disabled using Selenium
Close the dialog
Role
I formulated the idea and developed the solution using Playwright

Project goal
Project Tasks:
Design and implement a web-based FIR filling system that can be controlled via voice commands.
Use Selenium to automate web interactions and allow for voice commands to be translated into web inputs.
Develop a voice recognition system that can accurately recognize and interpret commands from individuals with disabilities.
Implement a database management system (DBMS) to store FIR data and make it easily accessible.

Challenges:
Ensuring accurate voice recognition and interpretation, particularly for individuals with unique speech patterns or disabilities.
Integrating the voice recognition system with the web-based FIR filling system using Selenium.
Managing and organizing the large amounts of data that the system will generate and store.
Ensuring the system is secure and meets data privacy regulations.

Solution
Here's an overview of the project solution:
The script imports the necessary libraries, including Selenium and speech recognition.
A list of fields to ask for and the duration for each field is defined, along with a function to convert text to speech using pyttsx3.
A loop is set up to ask the user each question and store the response in a dictionary. The loop continues until all questions have been answered.
The information is then used to fill in a complaint form on a website using Selenium, which involves opening a Chrome browser, navigating to the appropriate page, filling in the form, and submitting it.
The script also tweets about the incident using Selenium, which involves logging into a Twitter account, composing a tweet, and posting it.
Overall, the project solution allows users to easily and quickly report an incident by simply speaking to the assistant and having it fill out the necessary forms and post on social media on their behalf.
https://youtu.be/RSWkcD8P0nE
