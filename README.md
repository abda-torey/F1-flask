# F1 Drivers and Teams Data Web App
## Overview
This web application is designed to provide Formula 1 enthusiasts with detailed information about their favorite drivers and teams. Built using Flask and leveraging Google Cloud Datastore for backend storage, the app offers features such as filtering drivers by team or wins, viewing team details, and comparing statistics between drivers or teams.

## Features
1. Driver and Team Filters: Users can filter drivers by their team affiliation or total race wins. Similarly, teams can be filtered based on championship titles won.
2. Detailed Profiles: Access detailed profiles of F1 drivers and teams, including historical performance metrics and season-by-season breakdowns.
3. Comparative Analysis: The application allows for side-by-side comparison of drivers or teams, helping users analyze performance metrics directly.

## Getting Started
### Prerequisites
Before running this application, ensure you have the following installed:

 - Python 3.6+
 - Flask
 - Google Cloud SDK
 - A Google Cloud Platform account with Datastore enabled
## Installation
1. Clone the repository:

```
git clone <repository-url>
```
2. Navigate to the project directory:

```
cd <project-directory>
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Set up Google Cloud Datastore credentials:

Follow Google Cloud documentation to create a service account and download your credentials JSON file. Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your JSON file.

```
export GOOGLE_APPLICATION_CREDENTIALS="<path-to-your-service-account-file.json>"
```


## Usage
- Home Page: Start exploring F1 drivers and teams from the home page.
- Filter Drivers/Teams: Use the filter options to narrow down drivers or teams based on specific criteria.
- View Details: Click on a driver or team to view detailed profiles.
- Compare: Select drivers or teams to compare and analyze their performance metrics side-by-side.
