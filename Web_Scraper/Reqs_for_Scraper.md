# Requirements for Web Scrapper


## Packages
[Pandas](https://pandas.pydata.org/)
[Requests] (https://requests.readthedocs.io/en/master/)
[Selenimum](https://selenium-python.readthedocs.io/)

## Webdriver
In order for Selenium to work, it needs a webdriver. The driver depends on the browser you want to use, and are referenced to by the Selenium docs [here](https://selenium-python.readthedocs.io/installation.html#drivers). **Make sure to add it to your PATH.**

If the executable file is not in an executable path, it can be fined in the python script itself. It is listed under *Global Variables* with the variable name *driver*. Enter the path between the parentheses as *executable_path = '(PATH HERE)'*

#### Windows
Path can be found by going to the *Control Panel*, then searching for *environmental variables*.

#### MacOS/Linux

In the terminal, use the command echo $PATH

An example case: Using selenium with Firefox on Linux. Installation done with [this](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu) quICK guide.

## Sources
https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f

