# Number Verification Quickstart App Node

Welcome to Glide Number Verification Quickstart project! This web app is built with Express and deploys seamlessly to Google Cloud Platform (GCP) using CloudRun. Follow the instructions below to get started quickly.

## Prerequisites

1. **GCP Account**: Ensure you have an active Google Cloud Platform (GCP) account.
2. **Number Verify Service**: Subscribe to the Number Verify service in your GCP account.

## Quick Start Guide

### 1. Clone the Repository

```bash
git clone git@github.com:GlideApis/number-verification-nodejs-server-demo.git
cd number-verification-nodejs-server-demo
```

### 2. Deploy the Application

Run the following command to deploy the app:

```bash
npm run deploy
```

This command will handle everything, including deploying the app to CloudRun.

### 3. Follow the CLI Guidelines

During the deployment process, the CLI will guide you through several steps:

- **Credentials Setup**: 
  - You will be prompted to provide credentials. 
  - Go to your Glide dashboard, click the "Copy All Fields" button, and then paste the copied fields into the CLI when prompted.

- **Update Redirect URL**: 
  - Once the deployment is complete, the CLI will print a new redirect URL for the deployed application.
  - Copy this URL and go back to your Glide dashboard.
  - Edit the default redirect URL by clicking the edit button and replacing it with the new URL provided by the CLI.

### 4. Launch the Application

- The CLI will print the URL of the deployed application.
- Click this URL to start the app.

### 5. Explore the Demo

- **Non-Mobile Devices**: If you're accessing the app from a non-mobile device, you can use our test number to get the full experience:
  - Test Number: `+555123456789`
 
- **Mobile Devices**: If you're accessing the app from your phone, feel free to test it with any valid number.

Enjoy testing and exploring the app!
