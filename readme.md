# Item Catalog:
This web site shows TV series with their genre. It has a option to login after logging in you can add, edit and delete TV series.
## Requirements:
  Install the required items from their respective website.
* [Python 2.7](https://www.python.org/downloads/)
* [Virtual box](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

## Setting the environment:
* Download or clone the [udacity-vm](https://github.com/udacity/fullstack-nanodegree-vm) to your computer.
* Then download or clone the itemCatalog and copy it inside the udacity's vagrant folder.

## Usage:
* inside udacity's vagrant folder open your terminal and type `vagrant up` then `vagrant ssh`
* then go to the itemCatalog folder and run `python database_setup.py` , `python fake_data.py` to populate data in websites
`python application.py`.
* Go to a browser and type localhost:5050 to see the website.
