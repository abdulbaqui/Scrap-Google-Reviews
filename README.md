
# Scrap Google Reviews

I have used selenium for python to scrap reviews from google reviews. The output of this 
script would be a csv file consisting on the following dat.

* Reviewer Name (text)
* Review content (text)
* Full review link (text)
* Rating (int)
* Review Time Information
* Did the shop owner reply (bool)
* Reply text from Owner (text)

## Author

[@abdulbaqui](https://www.github.com/abdulbaqui)


## Run Locally

Clone the project

```bash
  git clone git@github.com:abdulbaqui/Scrap-Google-Reviews.git
```

Go to the project directory


Install dependencies

```bash
  pip install requirements.txt
```

Replace the path of the webdriver as per your system driver or if the driver is not present donwload and install

```bash
  '/usr/lib/chromium-browser/chromedriver'
```
Run the script

```bash
   python3 scrap_google_reviews.py
```

Thank you !!