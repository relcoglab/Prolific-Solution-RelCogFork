
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
- On your local machine, open the `dockerdeps` folder and follow the instrunctions in `dockerinstruct.txt`. 
- Zip the resulting `extracted-deps` folder and upload it as the source code to the Lambda function

### 3. Configuring API Gateway
- Set up a new API Gateway (REST) that triggers the Lambda function.
- There should be a 'ANY' method set up by default in Resources in the API console. Add `PROLIFIC_ID` as a URL query string parameter, configure it in both Method Request and Integration Request.
- The API should de-facto be on a stage called 'default'; for safety, you will need to 'Deploy' the API on the default stage everytime before making some change and testing.

### 4. Firestore Configuration
- In your Firestore database, create a collection called 'MoralCompositionTestRun'. In that, create a document called `ManagementData`. In that create two fields: `participants` and `surveys`, both are maps. You can refer to `db_fetch.py` to see how they are structured. Ideally, simply running `db_fetch.py` on your local machine should initialize the firestore as needed, but that isn't tested (yet).

### 5. Testing
- In the AWS Lambda console, go to Test and provide the test event json provided in `test_event.json`. If everything works, you should see a green box with some response about redirecting the user to the survey.
- In the API Gateway Console --> Resources --> ANY, you should find a 'Test' tab where you can set the method as `GET` and provide `PROLIFIC_PID=test123` and run the test, you should again see a green box with wither a message about redirecting the user to the survey or that the user has taken all surveys (depending on whether you tested with this PID before and the firestore document has populated that PID field with all the surveys that were provided in the lambda function.) 
- Now to test this directly on your browser, you need to find the Invoke URL of the API gateway, which you can find by going to the Lambda Console --> Configuration tab --> Triggers, and it will list the API gateway and the endpoint URL underneath it. It should end with `...[API_STAGENAME]/[LAMBDA_FUNCNAME]`. Copy that into a new broswer window and suffix it with `?PROLIFIC_ID=test456`, It should redirect to the Qualtrics survey! 
- Check your Firestore Console; it should populate with a new participant `test456` with the survey identifier as well. 

## Usage
Once set up, provide the API Gateway endpoint to Prolific as the survey link. When participants access this link, they are dynamically redirected to an available Qualtrics survey based on the logic defined in your Lambda function.

## Conclusion
This solution significantly enhances the capability to conduct large-scale, multi-survey studies on Prolific, ensuring efficient and flexible participant management. It's especially useful for researchers in the machine learning community, who require robust data collection from diverse sets of participants.

