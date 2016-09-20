### Coastal valuation

The objective of this web service API is to assess the expected value of coastal real estate, given sea level rise.  The assessed value will combine data from [NOAA's sea level rise estimates](https://www.climate.gov/maps-data/dataset/sea-level-rise-map-viewer) and [Zillow's real estate estimates](http://www.zillow.com/howto/api/GetZestimate.htm).  We will have to figure out exactly what the input and output parameters should be, but we will need to calculate the time profile of real estate value under multiple scenarios.  Whether that gets surfaced to the end-user of the service is still in question.

Currently **the only working feature is the geocoding service**, since [coastal.noaa.gov](https://coastal.noaa.gov) is currently down.  Plus we should all figure out what we need to do, and how to develop, anyway.  A brief video that describes the available data (when the site is live again) is available [here](https://www.climate.gov/news-features/decision-makers-toolbox/viewing-sea-level-rise).

### Developing

The proposed workflow follows:

- Fork the repository.
- Download and install the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads).  This will include the [Python Development Server](https://cloud.google.com/appengine/docs/python/tools/devserver), launched using the `dev_appserver.py` script (which will be appropriately placed on your Path during install).
- Edit the code, add features, add tests, whatever.  Test the service locally by running `dev_appserver.py .` from within the `coastal-valuation` directory (at the same level as `app.yaml`).  The default local server will run at `localhost:8080`.  So, for example, navigate to

[`http://localhost:8080/address?address=275 Beresford Creek Street&city=Daniel Island&state=SC&zip=29492`](http://localhost:8080/address?address=275%20Beresford%20Creek%20Street&city=Daniel%20Island&state=SC&zip=29492)

```json
{
    "response": {
        "coords": {
            "lat": 32.862305,
            "lon": -79.919835
        },
        "innundation": 0.385538
    },
    "meta": {
        "reference": "$695,503.00"
    }
}
```
- Ensure that you have a JSON viewer browser extension, like [**this one**](https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc?hl=en).

- Submit a pull request.  The repo administrators will test the new service, run it against our [TravisCI](https://travis-ci.org/) tests. If it passes muster, the administrators will push directly to App Engines production servers.  The command to push to App Engine follows.

```bash
appcfg.py update --oauth2 .
```

- The production APIs will be available at `https://earthgenome.appspot.com` and evenutally at `https://api.nature.tech` (??). You will need to request authority to push directly from [danhammer](https://github.com/danhammer).
