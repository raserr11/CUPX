![CUPX Badge](./images/CUPX%20(2).png)
# CUPX : Electric Consumption Analysis App


This application is designed to streamline the process of analyzing electric consumption reports for companies. It provides valuable insights in a faster, more visual, and cleaner way.

## Table of Contents

- [CUPX : Electric Consumption Analysis App](#cupx--electric-consumption-analysis-app)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Background](#background)
  - [Current Features](#current-features)
  - [Technologies Used](#technologies-used)
  - [Future Plans](#future-plans)
  - [Getting Started](#getting-started)
  

## Introduction

The CUPX App automates the extraction of valuable information from Excel reports provided by electric companies. It aims to save time and reduce errors compared to manual analysis using Excel, and is intended to expand with more advanced features such as cost simulations and savings forecasts in the future.

## Background

In my previous employment, a significant amount of time was spent manually analyzing electric consumption reports from companies using Excel. This process was not only time-consuming but also prone to errors. Recognizing the need for a more efficient solution, I developed this application to address that real-world problem.

In future iterations, the application will expand to include simulations of annual costs and savings forecasts, further enhancing its utility.

## Current Features

- **Data Extraction**: Automatically processes Excel files to extract essential consumption data.
- **Visual Representation**: Generates graphs and visualizations for easier interpretation of data.
- **Clean Interface**: Presents information in a structured and user-friendly manner.

*Note:* The project is currently in its first stage and fulfills one of the intended functionalities—extracting valuable information from the provided Excel files more quickly, visually, and cleanly.

## Technologies Used

- **Python 3.12**
- **Django**: Web framework for building the application.
- **Pandas**: Data manipulation and analysis.
- **Matplotlib & Seaborn**: Data visualization libraries.
- **HTML & CSS**: Front-end development.
- **Bootstrap**: Responsive design framework.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![NumPy](https://img.shields.io/badge/NumPy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-009978?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0668A1?style=for-the-badge&logo=seaborn&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

## Future Plans

The project will be resumed later to continue adding functionalities, including:

- **Annual Cost Simulations**: Implementing simulations of annual costs using the client's current prices and the prices offered by salespeople (like myself at that time). This will allow for comparisons and savings forecasts over the contract years of our offer compared to the client's current prices.
  
- **Contract Modalities Consideration**: The simulations will take into account different contract modalities (fixed, pool, and mixed), both for the current contract and the offered one.

- **Data Integration from OMIE**: Incorporating monthly data extraction from OMIE (Operador del Mercado Ibérico de Energía) to support accurate simulations and analyses.

- **Advanced Data Analysis**: Implementing more complex analysis features.
  
- **User Authentication**: Adding user login and permissions.
  
- **Database Integration**: Storing and managing data persistently.
  
- **Reporting Tools**: Generating comprehensive reports.
  
- **Optimization**: Improving performance and scalability.

*Note:* These advanced features will be developed as I gain more experience in the field of development.

## Getting Started

To run the application locally, follow these steps:

1. **Install the required packages**

   Make sure you have the following Python packages installed:

   ```bash
   pip install django pandas matplotlib seaborn
   ```

2. **Run the application**

   In your terminal, navigate to the project directory and run:

   ```bash
   python3 manage.py runserver
   ```

3. **Access the application**

   Open your web browser and go to:

   ```
   http://localhost:8000/
   ```
4. **Use Example Reports**

   In the `cups-examples` folder, you will find real CUPs reports with modified client information . Upload these reports through the application's upload screen to test the app.
