## Coastal valuation

The objective of this web service API is to assess the expected value of coastal real estate, given sea level rise.  The assessed value will combine data from [NOAA's sea level rise estimates](https://www.climate.gov/maps-data/dataset/sea-level-rise-map-viewer) and [Zillow's real estate estimates](http://www.zillow.com/howto/api/GetZestimate.htm).  We will have to figure out exactly what the input and output parameters should be, but we will need to calculate the time profile of real estate value under multiple scenarios.  Whether that gets surfaced to the end-user of the service is still in question.

Currently **the only working feature is the geocoding service**, since [coastal.noaa.gov](https://coastal.noaa.gov) is currently down.  Plus we should all figure out what we need to do, and how to develop, anyway.  A brief video that describes the available data (when the site is live again) is available [here](https://www.climate.gov/news-features/decision-makers-toolbox/viewing-sea-level-rise).

## Developing
 
**TODO: Flesh out this section.**

### Prerequisites

- Install [Docker Compose](https://docs.docker.com/compose/install).
- Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

### Workflow

Build 

```bash
docker-compose build
docker-machine create --driver virtualbox default
docker-machine ip
```

You should see the IP address of the docker service, something like `192.168.99.101`.  Then, start the server:

```bash
docker-compose up
```

You may need to run `docker-machine start default`. If you still can't connect, and the docker-machine is running, you can configure compose to use the machine with eval `$(docker-machine env default)`

Test the service with the following call:

[http://192.168.99.101:5000/v1/address?address=275 Beresford Creek Street&city=Daniel Island&state=SC&zipcode=29492](http://192.168.99.101:5000/v1/address?address=275%20Beresford%20Creek%20Street&city=Daniel%20Island&state=SC&zipcode=29492)

You may have to swap in the appropriate IP address.

Ensure that you have a JSON viewer browser extension, like [**this one**](https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc?hl=en). When you have developed, submit a pull request.  The repo administrators will test the new service, run it against our CI service tests. If it passes muster, the administrators will push directly to production. The production APIs will evenutally be at `https://api.nature.tech` (??). You will need to request authority to push directly from [danhammer](https://github.com/danhammer).
