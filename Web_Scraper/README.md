# Web Scrapper

## Description

The Webscrapper is the data gathering component of the FSOLG program. It is responsible for the collection of data and organizing it in an organized directory to be used by the machine learning algorithm. It is developed as a separate component here and then integrated into the FSOLG program whenver an updated, stable build is available.

## Sources

Data is scraped from 2 sources.

- [Basketball-Reference](https://www.basketball-reference.com/) - Source for the teams and players stats. Has historical data going back decades and is widely regarded as the most trusted source for NBA data outside of the NBA itself.
- [RotoGuru](http://rotoguru2.com/) - Source for historical data on players fantasy salaries. This was used as an alternative means of gathering data on fantasy salaries as a result of the NBA season being postponed due to COVID-19.

## Dependencies

- Python 3.8 - [https://www.python.org/downloads/]
  - Associated packages are listed in the *Reqs_for_Scraper.md* file.
