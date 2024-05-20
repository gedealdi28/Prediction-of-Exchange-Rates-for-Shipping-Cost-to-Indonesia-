# Final Project 4 Sekawan 

![Currenseelogo](https://github.com/FTDS-assignment-bay/p2-final-project-4-sekawan/blob/main/Logo3.jpeg)


# Prediction of Exchange Rate Values in Customs Duty Calculator

## Project Overview
This project aims to develop a predictive model for exchange rate values specifically tailored for use in a customs duty calculator. This will help in accurately calculating the cost of shipping goods to Indonesia. By predicting exchange rate fluctuations, businesses and logistics companies can better estimate their potential expenses, aiding in more effective financial planning and decision-making.

### Objective
Our main objective is to create a reliable model that forecasts the exchange rate values that are crucial in determining the customs duties for goods shipped to Indonesia. This model will help importers, exporters, and logistics companies mitigate risks associated with exchange rate volatility and plan their operations more effectively.

## Team Members
- **Aldi** - As Data Scientist and Data Engineer (📝[Github](https://github.com/gedealdi28), 📧[LinkedIn](https://www.linkedin.com/in/gede-aldi-vyacta-pranayena-s-412b741b7))
- **Amri** - As Data Scientist and Data Engineer (📝[Github](https://github.com/amrihakim9), 📧[LinkedIn](https://www.linkedin.com/in/muhammad-amri-hakim-0ba675224))
- **Vania** - As Data Scientist and Data Engineer (📝[Github](https://github.com/vaniaalya14), 📧[LinkedIn](https://www.linkedin.com/in/vania-alya-qonita/))
- **Mesayu** - As Data Analyst (📝[Github](https://github.com/Mesayu), 📧[LinkedIn](https://www.linkedin.com/in/mesayu-gina-puspita-9a81a1233/))

## Project Structure
### Workflow
The workflow is split into 3, separated by roles:

#### Data Engineering
- Data Collection: Data is collected from Google Finance, covering the range from January 1, 2001, to May 5, 2024, for each currency. Afterwards, the data is exported into a CSV file.
- Data Cleaning:  The data is cleaned by handling missing values and performing differencing on non-stationary data that will be predicted using ARIMA
#### Data Science
- Model Development: Created a prediction and forecast to USA, Saudi Arabia, Japan, Korea, Thailand, and Singapore exchange rate using Moving Average, ARIMA, Linear Regression, Deep Learning 
- Model Optimization: Searching best combination of p,d,q on ARIMA finding best model between Moving Average, ARIMA, Linear Regression, Deep Learning for forecasting exchange rate.
#### Data Analysis
- Visualization: Created visual time series of every exchange rate
- Reporting: Create a comprehensive report using your collected findings and insights.

Furthermore, all of our visualisations are also available on [Exploratory Data Analysis](https://public.tableau.com/app/profile/elia.oktaviani/viz/FinalProjectEDA_17121230420550/Dashboard2?publish=yes](https://public.tableau.com/app/profile/mesayu.puspita/viz/insightfinpro/Dashboard1?publish=yes))
And our deployment can be accessed on [streamlit](https://huggingface.co/spaces/amrihakims/CurrenSee)
