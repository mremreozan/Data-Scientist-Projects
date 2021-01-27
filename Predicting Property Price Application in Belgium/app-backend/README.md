<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/adamflasse/Api_deployment">
    <img src="assets/BecodeLogo.png" alt="Logo" width="240" height="180">
  </a>

  <h1 align="center">API Deployment</h1>
  <h3 align="center">Becode project to deploy a machine learning model API</h3>

  <p align="center">
    by Saba Y., Didier U., Emre O. and Adam F.
    <br />
    
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  
* [Getting Started](#getting-started)
  * [Choosing the model](#choosing-the-model)
  * [Setting Work Objectives](#setting-work-objectives)
* [JSON File preprocessing](#JSON-File-preprocessing)
  * [How did we handle the optionals ?](#How-did-we-handle-the-optionals-?)
  * [What about the errors ?](#What-about-the-errors-?)
* [API](#API)
* [Outputs](#outputs)
* [Use case example with Postman](#use-case-example-with-postman)
* [Links](#links)




<!-- ABOUT THE PROJECT -->
## About The Project



In our learning path at Becode we had multiple group projects focusing on real estate in Belgium. First we had to scrape some websites to find data and make a solid dataset. Then we had to "merge" all the other groups dataset and work on them. We have essentially done some major data cleaning and then used what we learned about data visualization to make a presentation. We had a week to get familiar with all types of regression, after which we were asked to test our knowledge to predict house prices on the Belgian market to the best of our abilities using the dataset of our previous mission. Now we have to deploy our model in an API using Flask, Docker and Heroku. 



<!-- GETTING STARTED -->
## Getting Started

Because of group changes, we had different models and dataset in order to complete the mission. Because of the required Json that we receive we had to rework our models in order to match the required features.

### Choosing the model

We've tried many different models to reach the best score possible. We've good results with the gradientBoosting one so we chose this one. 


### Setting work objectives

We had to split the tasks. So we can work paralelly to go further. We've scheduled regular meetings to be sure that everyone knows what the others are doing. 




<!-- USAGE EXAMPLES -->
## JSON File preprocessing

The Api accepts a posted JSON file. We have to work the data so it can fit the features to predict the price of the house. 
The JSON format is the following:

```
{
    "data": {
            "area": int,
            "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
            "rooms-number": int,
            "zip-code": int,
            "land-area": Optional[int],
            "garden": Optional[bool],
            "garden-area": Optional[int],
            "equipped-kitchen": Optional[bool],
            "full-address": Optional[str],
            "swimmingpool": Optional[bool],
            "furnished": Optional[bool],
            "open-fire": Optional[bool],
            "terrace": Optional[bool],
            "terrace-area": Optional[int],
            "facades-number": Optional[int],
            "building-state": Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]
    }
}
```



<!-- ROADMAP -->
### How did we handle the optionals ? 

Basically if one of the optionals doesn't exist we look at the type of the building (which is a required parameter) and then provide you a default feature based on the building type that you provided. 


<!-- CONTRIBUTING -->
### What about the errors ? 

We have different errors that are handled by the API.

It mainly concerns the required parameters because the optionals are handled by the default models.

* The `zip-code` has to be between 1000 and 9999 ( There are no postcode existing in Belgium smaller nor higher than these values ) 
* The required parameters has to be filled correctly otherwise you will get an error. You can refer to the JSON provided earlier. 



<!-- LICENSE -->
## API

We have 2 routes:

* `/` that accepts a `GET` request which returns if the server is alive or not.
* `/predict` that accepts a `GET` request returning a string to explain what the `POST` expect (data and format) and a `POST`request that receives the data of a house in json format.


## Outputs

When at least the required parameters are filled, the API will return a string with the price (as a float) in it.

Otherwise it will show a error message, directing you to this page. 


## Use case example with Postman

Let's say you've filled out all the JSON file properly and it looks like something like this :

```
{
    "data": {
            "area": 100,
            "property-type": "APARTMENT",
            "rooms-number": 4,
            "zip-code": 7000,
            "land-area": 130,
            "garden": true,
            "garden-area": 30,
            "equipped-kitchen": true,
            "swimmingpool": false,
            "furnished": true,
            "open-fire": false,
            "terrace": false,
            "terrace-area": 0,
            "facades-number": 3,
            "building-state": "NEW"
    }
}
```

(The number of each step is referenced in the image below)

* 1) Select the `POST` request
* 2) Click on `Body`
* 3) Click on `Raw` then copy and paste the JSON file above (or one of your own that respect the criterias will be fine) in the `ÌNPUT` section
* 4) Choose `JSON`for the type of document
* 5) Click on `SEND`

The prediction will be shown in the output section

<br />
<p align="left">
  <a href="https://github.com/adamflasse/Api_deployment">
    <img src="assets/Capture d’écran 2020-12-11 à 16.57.43.png" alt="Image" width="400" height="250">
  </a>

 
</p>


Note that the link being used ``http://0.0.0.0:5000/predict`` is a test url. 
The urls working will be displayed in the [Links](#links) section.


If all the required parameters are correctly filled, the output will be:


```
{
    "prediction": [
        (prediction price)
    ]
} 
```

If not :

```
{
    "error": "We can not provide prediction, please input rooms-number feature in your data. Please check: https://github.com/adamflasse/Api_deployment/blob/main/README.md for more info"
}
```




## Links

Urls working: 


## How to build a flask application in Heroku
```python
heroku login
heroku container:login
heroku create
heroku container:push web -a <heroku repository name>
heroku container:release web -a <heroku repository name>
```
click -> 
https://<heroku-repository-name>.herokuapp.com








