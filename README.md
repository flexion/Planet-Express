# Planet Express (Rackspace) Delivery

![professor](https://raw.githubusercontent.com/flexion/Planet-Express/master/assets/professor.jpg)

*Good news everyone!*

Navigate your Rackspace account from the command line, or from Python code.

Easily generate JSON Lists of...
 
 - IP addresses
 - servers
 - images
 - image members
 - loadbalancers

And do stuff!...

 - add members to images

*Bad news everyone. Only the second generation API is supported.*

## Setup

`clone` this repo

`cd` to root directory

`./setup.sh` to install dependencies

## Running

edit your `PlanetExpress/settings/local_settings.py` file

`./env/bin/activate` your virtualenv

`python ./PlanetExpress` to see what your options are

Here's a test:

`python ./PlanetExpress get servers`