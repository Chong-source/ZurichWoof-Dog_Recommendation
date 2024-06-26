# ZurichWoof: A Dog Recommendation Application
Note: For more detailed documentation, please read [project_report.pdf](project_report.pdf)
## Table of Contents
1. [Introduction](#What-the-project-does)
2. [Instructions](#Instructions-on-running-the-program)
3. [Motivation for Creating ZurichWoof](#Motivation)

## What the project does
Zürich Woof is an application that recommends the dog breeds to the owners based on the user's preferences and demographics. We have also created an user interface that asks a series of questions to the user and shows the top 5 districts of the population of that dog breed in Zürich and also the features of the dog according to the ratings given by the American Kennel Club. This project is mainly written in python, and we also generated our own data such as in district_closeness.py and dog_images_translations.py. We learned a lot about data cleaning, database merging, and User Interface in this project.

## Instructions on running the program
* Please ensure internet connection is good while running this program because when displaying image of the dogs, the program fetches images from the internet using links to the image address.
* Please be patient with the loading time of the map and the dog breed information images, as they can be a bit slow sometimes.
1. Download all of the files from the repository onto the computer as a zip file, open the zip file in a new folder
2. Install all requirements: ```pip install -r requirements.txt```
3. The zip file of the data sets is also uploaded to this repo, and its name is ```data.zip```. Download this file as a zip. Unzip this file, and please ensure that the name of the folder is just 'data' because we're calling using that specific file path.
4. Run the main.py file: ```python3 main.py```
5. You should see the user interface

## Motivation
### Problem Description 
In today's digital age, personalized recommendations have become crucial for enhancing user experience and engagement. 
Our program provides recommendations for prospective dog owners to find the right type of dog for them based off of their demographics and preferences. 

By analyzing key attributes such as age, gender, and location, our system internally matches the user with other users with similar profiles to determine common dog breeds with similar ownership experience. The data set of dog owners created by Open Zurich, the official open dataset that the Zurich city created to let the public analyze more data about their city.

By asking the user for their personal preferences for their prospective dog ownership (such as various personality aspects of the dog) we can further ensure a good match between pet and owner.

### Context 
The context of this problem is we came across this fun and unique data set (Dogs of Zürich) that intrigued us. We wanted to do computations on this dataset and see how must feature we can develop using just the dog's information and owner's information. 

### Motivation for the project
Research has shown that matching the lifestyle and personality of the owner and pet leads to a longer and healthier relationship between the pet and the owner. Thus, we want the owner of the dog to make informed decisions when purchasing a dog in Zürich by choosing the suitable district to live in for them and their dogs. Moreover, matching their preferences with the correct breed.

### Project question 
What are the top 5 districts that has the highest proportion of a each dog breed in Zurich and how can we make various customized suggestions to potential dog owners using the dataset?

