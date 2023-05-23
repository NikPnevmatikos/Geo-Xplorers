# Software Requirements Specification

## For Geo-Xplorers            
### pdf version: **[SRS.pdf](SRS.pdf)**

Version 1.0   

### Contributors:
> Nikolaos Pnevmatikos\
Maria Diamandi\
Aikaterini Milioti\
Ioannis Kalesis\
Eleftherios Stefanou


Table of Contents
=================
* 1 [Introduction](#1-introduction)
* 2 [User Categories](#2-user-categories)
  * 2.1 [Anonymous Users](#21-anonymous-users)
  * 2.2 [Registered Users](#22-registered-users)
  * 2.3 [Admin Users](#23-admin-users)
* 3 [Scope](#3-scope)
* 4 [Constraints](#4-constraints)
* 5 [Requirements](#5-requirements)
  * 5.1 [Functional Requirements](#51-functional-requirements)
    * 5.1.1 [Managing Users](#511-managing-users)
    * 5.1.2 [Search](#512-search)
    * 5.1.3 [Point of interest information](#513-point-of-interest-information)
    * 5.1.4 [Search Results](#514-search-results)
    * 5.1.5 [Posts](#515-posts)
  * 5.2 [Non-Functional Requirements](#52-non-functional-requirements)
    * 5.2.1 [Performance](#521-performance)
    * 5.2.2 [Usability](#522-usability)
    * 5.2.3 [Security](#523-security)
    * 5.2.4 [Scalability](#524-scalability)
    * 5.2.5 [Reliability](#525-reliability)
* 6 [Conclusion](#6-conclusion)



## 1. Introduction
- The idea behind this platform is to create a social media web app, which will utilize data from http://geodata.gov.gr to establish “hotspots” where users will be able to create and upload posts and interact with each other.
- It will allow users to register, search for points of interest, and generate content. Said content will be available to the rest of the user base by allowing searches based on various criteria, including text, distance from point of interest and other data such as general topics or people.


## 2. User Categories
### 2.1 Anonymous: 
- Anonymous users can navigate through the application, search for points of interest, view other posts.

### 2.2 Registered Users:
- Registered users can navigate through the application, search for points of interest, view, like or comment on other user’s  posts. 
- Registered users can view other user’s profiles.
- They can save a point of interest to receive updates in the form of notifications. 

### 2.3 Admin: 
- Can do everything a registered user can, but also update the platform with new points of interest. 
- They can also manage users (delete their account, if necessary).

## 3. Scope
- From the datasets in the geodata.gr site, we chose a few to include in our social media web app
- Notably, the datasets are:
  * “Αεροδρόμια Ελλάδας”
  * “Λίμνες Ελλάδας”
  * “Δημόσια Κτήρια”
  * “Πόλεις”
  * “Σημεία ενδιαφέροντος του Δήμου Καλαμαριάς”
  * “Σημεία ενδιαφέροντος του Δήμου Θεσσαλονίκης”
  * “Σημεία ενδιαφέροντος Χανίων”
  * “Αισθητικά Δάση”
- From the datasets, we will not place all the data contained within them in the database, keeping a small percentage as part of the testing files.
- The remaining data will be used by the admin to manually upload the new geo data to the database, which will trigger multiple notifications on the user’s “saved” searches.
- In the point of interests files, apart from the obvious datasets like “Λίμνες”, which contain lakes, some contain a lot of different points of interests, e.g.  the dataset “Σημεία ενδιαφέροντος του Δήμου Καλαμαριάς”, may contain Pharmacies, Libraries, Churches and a lot more.
- All above data will all be added to the same database under the same table-data model, turning them all into points of interest. i.e For a search for “Θεσσαλονίκη” we will get results containing data from both “Δημόσια Κτήρια”, “Πόλεις” and “Σημεία ενδιαφέροντος του Δήμου Θεσσαλονίκης”.
- Not all datasets are of the same form, with some containing more data/columns than the rest, thus, given that we will utilize the same data model for all, the data model will consist of the largest amount of information provided by a dataset, with any entries with fewer columns from other datasets containing null values.

## 4. Constraints
- Messaging between users is not supported (with the only exception being the ability  to comment in a user’s post).
- Directions from location to point of interest are not provided.
- Not allowing users to create custom shapes for their search results (only the circle shape is supported).
- Point of interest Review (Star Rating).

## 5. Requirements

### 5.1 Functional Requirements
#### 5.1.1 Managing Users
 Users will be able to:
 * Login to the platform
 * Users must be able to edit their account information(email and maybe other details).
 * Create a Post on each location they visit
 * Interact to a post
 * View the places they have visited
 * View the profile of another user

#### 5.1.2 Search
 Users will be able to make searches based on a set of criteria:
 * Distance from a point of interest or a shape
 * Matching words from free text to any point of interest that contains them
 * Metadata such as topics and people
 * Search results based on chosen criteria

#### 5.1.3 Point of Interest Information
- Each point of interest may have additional information
- The point of interest will be placed in it’s exact coordinates in the map
- Each point of interest contains a list of post uploaded by users

#### 5.1.4 Search Results
- Returns all Points of Interest in a specific (chosen by the user) radius, either from a point or from his current location 
- Users will be able to save a search result 
- If any new data is added to the platform which matches the search, then any user who has saved the search result will receive a notification

#### 5.1.5 Posts
- Contain a photo, a free text description
- Include interactions from other users


### 5.2 Non-Functional Requirements

#### 5.2.1 Performance
- No performance requirements exist, other than the search results being provided in a timely manner

#### 5.2.2 Usability
- Web app should be simple to use and each functionality should be self explanatory
- UI should feel flexible and non restricting
- Posts will be shown to users after being  ranked based on interactions

#### 5.2.3 Security
- For Security, the focus will be to guard endpoints of the API from potential malicious users, under the assumption that any user and any kind of request can hit the endpoint

#### 5.2.4 Scalability
- Detailed Commit History and Documentation

#### 5.2.5 Reliability
- Secure and bug-free user experience

## 6. Conclusion
In conclusion, our project aimed to create a social media web platform that incorporates geographical information in order to motivate people to explore the world. Through the use of location-based features, users are able to connect with others who share similar travel interests and experiences, discover new and exciting places to visit, and share their own travel experiences with the world. By creating a community of travel enthusiasts, we hope to inspire and encourage people to explore the world and discover all the unique and wonderful experiences that it has to offer. Through this platform, we believe that we can help people broaden their horizons, expand their cultural understanding, and ultimately lead more fulfilling lives.
