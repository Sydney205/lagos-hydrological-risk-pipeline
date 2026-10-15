
# Lagos Hydrological Risk Pipeline 🌧️

A data science project investigating historical weather and hydrological patterns to better understand environmental conditions associated with flood risk in Lagos, Nigeria.

Flooding affects communities, businesses, transportation, and access to essential services. The Lagos Hydrological Risk Pipeline explores how historical environmental data can help us investigate these challenges through data analysis and evidence-based risk assessment.

We are a team of six building this project in public, documenting our progress, challenges, and discoveries as we work.

## 🎯 Project Objectives

- Collect and analyse historical weather and hydrological data for Lagos and its surrounding hydrological context.
- Investigate relationships between precipitation, soil moisture, river discharge, and other environmental variables.
- Explore temporal patterns and spatial differences across locations.
- Develop a transparent numerical flood-risk scoring methodology, with a proposed scale of 0 to 100.
- Compare environmental patterns with documented flood incidents where reliable records are available.
- Communicate findings, limitations, and lessons learned through open collaboration and technical writing.

## 📊 Data Sources

| Source | Purpose |
|---|---|
| [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) | Historical weather and environmental variables |
| [Open-Meteo Global Flood API](https://open-meteo.com/en/docs/flood-api) | Model-derived river discharge data |
| [Hugging Face Dataset](https://huggingface.co/Sydney205/lagos-hydrological-zone-data) | Access to the project's published dataset |

Our dataset covers historical dates beginning in May 2012, with ongoing updates to the latest available data.

### Key Variables

The dataset includes environmental indicators such as:

- `Date`: Date of the observation.
- `State`: State associated with the location.
- `LGA_Location`: Local Government Area or location identifier.
- `precipitation_sum`: Daily accumulated precipitation.
- `river_discharge`: Model-derived river discharge.
- `soil_moisture_0_to_7cm`: Soil moisture in the upper soil layer.
- `soil_moisture_7_to_28cm`: Soil moisture at a deeper soil layer.
- `et0_fao_evapotranspiration`: Reference evapotranspiration.
- `wind_speed_10m_max`: Maximum wind speed at 10 metres.
- `wind_gusts_10m_max`: Maximum wind gust speed at 10 metres.

Column availability and completeness may vary across dates and locations. Refer to the dataset and its documentation for the current schema, units, and data coverage.

## 🔬 Methodology

Our workflow is designed to move from raw environmental data towards a transparent and carefully evaluated risk assessment.

1. **Data collection:** Retrieve historical weather and hydrological variables from available sources.
2. **Data preparation:** Clean, organise, and validate records for analysis.
3. **Exploratory data analysis (EDA):** Investigate distributions, missing values, temporal trends, spatial differences, and relationships between variables.
4. **Environmental pattern analysis:** Explore combinations of conditions that may be associated with elevated flood risk.
5. **Risk score development:** Investigate a numerical score from 0 to 100 using a documented methodology.
6. **Validation and evaluation:** Compare findings with independent flood reports or incident records where reliable data is available.
7. **Communication:** Document findings, limitations, and recommendations.

The methodology will evolve as we learn more about the data and evaluate our assumptions.

## ⚠️ Important Limitations

**This project is exploratory and is not yet a validated flood-prediction system.**

Our environmental dataset does not contain comprehensive, independently verified labels indicating whether flooding occurred at each location and time.

It is therefore important to distinguish between environmental conditions associated with flood risk and confirmed flood events.

- High rainfall or soil moisture does not, by itself, prove that flooding occurred.
- River discharge values from the Global Flood API are model-derived estimates, not necessarily direct measurements from local river gauges.
- Data resolution, missing observations, and geographic coverage may affect location-level comparisons.
- Any proposed risk score requires a documented methodology and appropriate evaluation before it can support reliable conclusions.
- A score of 80 out of 100 would not mean an 80% probability of flooding unless a separate probabilistic model had been appropriately calibrated and validated.

We aim to communicate these uncertainties honestly throughout the project.

## 🛠️ Technology Stack

- **Python** for data processing and analysis.
- **pandas and NumPy** for data manipulation and numerical operations.
- **scikit-learn** for potential modelling and evaluation.
- **Google Colab** for exploratory analysis and collaborative notebooks.
- **Git and GitHub** for version control and team collaboration.
- **Hugging Face** for dataset hosting and sharing.
- **Open-Meteo APIs** for historical weather and hydrological data.

## 🚧 Current Project Status

We are currently updating the dataset and beginning exploratory data analysis.

Our immediate priorities are:

- Examine dataset quality and completeness.
- Investigate temporal and spatial environmental patterns.
- Explore relationships between environmental indicators.
- Identify methodological challenges and potential sources of bias.
- Establish a transparent approach to developing and evaluating the proposed flood-risk score.

The numerical scoring methodology and its evaluation criteria are still under development. We will share findings as the analysis progresses.

## 👥 Team Collaboration

This project is being developed by a team of six working across data engineering, data science, exploratory analysis, project coordination, and technical communication.

We use Git and GitHub to coordinate development, review changes, and maintain a shared project history.

Our approach emphasises collaboration, reproducibility, documentation, and learning through experimentation.

## 🌍 Building in Public

We believe that the process of solving a real-world problem is worth sharing, not just the final result.

We use [OpenStage.dev](https://openstage.dev/) to share the project's progress as we investigate the data, refine our methodology, and learn from challenges along the way.

Follow the journey, explore our work, and share constructive feedback as the project develops.

## 📚 Explore the Project

- **Dataset:** [Lagos Hydrological Zone Data on Hugging Face](https://huggingface.co/Sydney205/lagos-hydrological-zone-data)
- **Build in public:** [OpenStage.dev](https://openstage.dev/)
- **Historical weather data:** [Open-Meteo Documentation](https://open-meteo.com/en/docs/historical-weather-api)
- **River discharge data:** [Open-Meteo Global Flood API](https://open-meteo.com/en/docs/flood-api)

## 🤝 Contributions and Feedback

We welcome constructive feedback, suggestions for relevant datasets, methodological discussions, and ideas that can improve the quality of this research.

If you have experience in hydrology, climate science, geospatial analysis, flood-risk assessment, or data science, your perspective could help us ask better questions and strengthen our approach.

## 💡 Our Vision

We want to explore how data science can contribute to a better understanding of environmental risks affecting communities in Lagos.

We recognise that data alone cannot solve flooding. However, carefully analysed evidence can help researchers and decision-makers investigate problems more effectively.

**We are building the Lagos Hydrological Risk Pipeline one dataset, one analysis, and one question at a time.**

*This project is a work in progress. Findings and methodologies will be updated as the research develops.*
