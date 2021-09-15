<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/MySlav/IoT-Zabranjeno-voce">
    <img src="https://i.ibb.co/zbZkRmt/android-chrome-512x512.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">IoT-Zabranjeno-vocee</h3>

  <p align="center">
    Student project - "Internet of Things" course
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![project-schema](https://i.ibb.co/yq5KQ0m/shema-Projekta.jpg])

In some stores, the price of an item depends on its expiry date. For example, if milk’s best before date expires tomorrow, some stores will be selling it at discounted price. The same goes for fruit. 
Because fruit does not have expiry date, stores usually rely on visual judgment on fruit condition; if bananas have many brown spots, it is likely they are nearing the end of their sellable cycle so they are discounted manually by store personnel. 
In this project, we will be creating a platform for applying automated discounts based on the current state of the bananas (the same principle can be applied to any type of fruit).
We will be employing a Raspberry Pi camera to take regular photos of bananas on the store shelf. 
By utilizing deep learning model, our system will judge the remaining time until bananas cannot longer be sold. 
Based on remaining expected life of bananas and defined rules, the system will automatically lower the banana prices in the accounting software and will advertise discounts to all neighboring mobile phones that have our mobile application installed by using BLE beacons.

The system will have the following components:
*	BLE beacon.
*	Shopper mobile application will scan for nearby BLE beacon and display discount information if web app says so.
*	Web application will:
    *	Enable administrators to manage fruit products. Each product will have at least a name, image and price. 
    *	Enable administrators to manage discounts for fruit. For example, administrator can define that bananas will be discounted 40% when their class becomes yellow flecked with brown .
    *	Return discount info for BLE beacon.
    *	Enable viewing of all taken photos and their classifications.
*	Raspberry Pi with camera will take an image of a (single) banana every n minutes, classify it and then upload to database and (possibly) trigger the discount.
*	REST API for Raspberry Pi to upload photos and classification. This API will have a functionality to apply discount if banana is classified as such, triggering an info sent to mobile app.

### Built With

* [Flask](https://flask.palletsprojects.com)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com)
* [PyTorch](https://pytorch.org/)
* [Bootstrap](https://getbootstrap.com)
* [Microsoft Azure](https://azure.microsoft.com) - SQL server and VM(Oracle linux based)
* [Android Studio](https://developer.android.com/studio)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

How to setup every component.
* Model training
  ```sh
  pip install -r /model/requirements.txt
  ```
* Raspberry PI - only needed if you are not on raspbian distro
  ```sh
  pip3 install -r /raspi/requirements.txt
  ```
* Web app & Rest API
  ```sh
  pip install -r /web_app_rest_api/requirements.txt
  ```
* DB
     * run /db/create.sql to create needed tables in SQL server

Note - You need to open port 5000 on your VM where the web app and Rest API are deployed.
<!-- USAGE EXAMPLES -->
## Usage

How to start components.

* Raspberry PI - only needed if you are not on raspbian distro
  ```sh
  python3 /raspi/PiCamera.py
  ```
  
* Web app & Rest API
  ```sh
  python /web_app_rest_api/app.py
  ```

<!-- CONTACT -->
## Contact

Mislav Spajic - mislav.spajic@racunarstvo.hr

Karlo Hren - karlo.hren@racunarstvo.hr

Nenad Durak - durak.nenad@racunarstvo.hr

Hrvoje Kopic - hrvoje.kopic@racunarstvo.hr

Project Link: https://github.com/MySlav/IoT-Zabranjeno-voce
