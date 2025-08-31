
<p align="center">
  <img src="https://raw.githubusercontent.com/explomind1/Prolific-Survey-Distribution-Solution/main/d_TJeFaR7L.svg" >
</p>



# Prolific Survey Distribution Solution

## Overview
This project addresses a significant limitation on the Prolific platform, which restricts users to distributing only one survey link per study. Our solution enables the distribution of multiple surveys, particularly beneficial for complex research setups involving multiple datasets. This is achieved using AWS Lambda, API Gateway, and Firebase, creating a seamless experience for distributing multiple surveys hosted on Qualtrics via Prolific.

## Features
- **Dynamic Survey Allocation**: Automatically assigns surveys to participants based on availability and previous completions.
- **Scalable**: Utilizes AWS Lambda for on-demand, scalable computing resources.
- **Real-Time Data Management**: Firestore is used for real-time data updates and management.

## Architecture
This system integrates several technologies:
- **AWS Lambda**: Manages the logic to distribute survey links dynamically.
- **API Gateway**: Provides an endpoint that triggers the Lambda function.
- **Firebase Firestore**: Stores and manages participant and survey data.

## Prerequisites
- AWS account with access to Lambda and API Gateway.
- Firebase project with Firestore enabled.
- Access to the Qualtrics and Prolific platforms for survey and participant management.

## Setup Instructions

### 1. Firebase Setup
- Initialize your Firebase project and enable Firestore.
- Set up Firebase Admin SDK and obtain your credentials file (`firebase_credentials.json`).

### 2. Deploying AWS Lambda
- Create a new Lambda function in your AWS Console - Python 3.10 runtime, x86-64 architecture.
- On your local machine, open the `dockerdeps` folder and follow the instructions in `dockerinstruct.txt`. 
- Zip the resulting `extracted-deps` folder and upload it as the source code to the Lambda function

### 3. Configuring API Gateway
- Set up a new API Gateway (REST) that triggers the Lambda function.
- There should be a 'ANY' method set up by default in Resources in the API console. Add `PROLIFIC_ID` as a URL query string parameter, configure it in both Method Request and Integration Request. In Method Request, simply add `PROLIFIC_PID` as a new parameter. In Integration Request, add `PROLIFIC_PID` and enter `method.request.querystring.PROLIFIC_PID` in the "Mapped from:" box.
- The API should de-facto be on a stage called 'default'; for safety, you will need to 'Deploy' the API on the default stage everytime before making some change and testing.

### 4. Firestore Configuration
- In your Firestore database, create a collection called `MoralCompositionTestRun`. In that, create a document called `ManagementData`. 
- On your local machine, run `python db_fetch.py` inside the `dockerdeps` folder, it should initialize the database properly (check that `config.py` contains the correct credentials to refer to the database on firestore!)
- NOTE: This code is set up to work with these firestore names. Simply replace all names with whatever your names are in `lambda_function.py` and `db_fetch.py` for it to work with your firestore database!

### 5. Testing
There are three ways you can test, I recommend doing atleast one of the first two along with the third one:
1. In the AWS Lambda console, go to Test and provide the test event json provided in `test_event.json`. If everything works, you should see a green box with some response about redirecting the user to the survey. NOTE: Change the parameters in the JSON to match your lambda function name, query string, etc.!
2. In the API Gateway Console --> Resources --> ANY, you should find a 'Test' tab where you can set the method as `GET` and provide `PROLIFIC_PID=test123` and run the test. You should again see a green box with either 1) a message about redirecting the user to the survey or 2) that the user has taken all surveys (depending on whether you tested with this PID before; either one is good news.) 
3. To test this directly on your browser, you need to find the Invoke URL of the API gateway, which you can find by going to the Lambda Console --> Configuration tab --> Triggers, and it will list the API gateway and the endpoint URL underneath it. It should end with `...[API_STAGENAME]/[LAMBDA_FUNCNAME]`. So for me it ended in `...default/prolificSolution`. Copy the full endpoint into a new broswer window and suffix it with `?PROLIFIC_ID=test456` and run, It should redirect to the Qualtrics survey specified in the lambda function! 
- Check your Firestore Console; it should populate with a new participant `test456` along with the survey identifier. 

## Usage
Once set up, provide the API Gateway endpoint to Prolific as the survey link. When participants access this link, they are dynamically redirected to an available Qualtrics survey based on the logic defined in your Lambda function.

## Conclusion
This solution significantly enhances the capability to conduct large-scale, multi-survey studies on Prolific, ensuring efficient and flexible participant management. It's especially useful for researchers in the machine learning community, who require robust data collection from diverse sets of participants.

