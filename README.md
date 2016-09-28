## Coastal valuation

The objective of this web service API is to assess the expected value of coastal real estate, given sea level rise.  The assessed value will combine data from [NOAA's sea level rise estimates](https://www.climate.gov/maps-data/dataset/sea-level-rise-map-viewer) and [Zillow's real estate estimates](http://www.zillow.com/howto/api/GetZestimate.htm).  We will have to figure out exactly what the input and output parameters should be, but we will need to calculate the time profile of real estate value under multiple scenarios.  Whether that gets surfaced to the end-user of the service is still in question.

Currently **the only working feature is the geocoding service**, since [coastal.noaa.gov](https://coastal.noaa.gov) is currently down.  Plus we should all figure out what we need to do, and how to develop, anyway.  A brief video that describes the available data (when the site is live again) is available [here](https://www.climate.gov/news-features/decision-makers-toolbox/viewing-sea-level-rise).

## Developing

The stack relies on 

### Prerequisites

- Install [Docker Compose](https://docs.docker.com/compose/install).

### Workflow
```bash
docker-compose build
docker-compuse up
```
The 

Ensure that you have a JSON viewer browser extension, like [**this one**](https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc?hl=en). When you have developed, submit a pull request.  The repo administrators will test the new service, run it against our CI service tests. If it passes muster, the administrators will push directly to production. The production APIs will evenutally be at `https://api.nature.tech` (??). You will need to request authority to push directly from [danhammer](https://github.com/danhammer).
