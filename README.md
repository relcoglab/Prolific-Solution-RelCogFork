

<p align="center">
   <img src="https://github.com/explomind1/AOI_ProlificSurveyAlgoMoralLearning1/blob/main/d_TJeFaR7L.svg" />
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
- Create a new Lambda function in your AWS Console.
- Use the provided Python script for the Lambda function. Make sure to update the `config.py` with your Firebase credentials.

### 3. Configuring API Gateway
- Set up a new API Gateway that triggers the Lambda function.
- Configure the method and deployment settings to expose your Lambda function as a web service.

### 4. Firestore Configuration
- Populate the Firestore `ManagementData` document with initial data for surveys and participants as described in the script.
- Ensure that the Firestore rules allow your Lambda function to read and write to the necessary documents.

## Usage
Once set up, provide the API Gateway endpoint to Prolific as the survey link. When participants access this link, they are dynamically redirected to an available Qualtrics survey based on the logic defined in your Lambda function.

## Conclusion
This solution significantly enhances the capability to conduct large-scale, multi-survey studies on Prolific, ensuring efficient and flexible participant management. It's especially useful for researchers in the machine learning community, who require robust data collection from diverse sets of participants.

