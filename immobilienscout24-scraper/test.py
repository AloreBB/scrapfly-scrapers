import json
import os
from pathlib import Path
from cerberus import Validator
import immobilienscout24
import pytest
import pprint

pp = pprint.PrettyPrinter(indent=4)
immobilienscout24.BASE_CONFIG["cache"] = os.getenv("SCRAPFLY_CACHE") == "true"


def validate_or_fail(item, validator):
    if not validator.validate(item):
        pp.pformat(item)
        pytest.fail(
            f"Validation failed for item: {pp.pformat(item)}\nErrors: {validator.errors}"
        )


property_schema = {
    "schema": {
        "type": "dict",
        "schema": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "address": {"type": "string"},
            "propertyLlink": {"type": "string"},
            "propertySepcs": {
                "type": "dict",
                "schema": {
                    "floorsNumber": {"type": "string"},
                    "livingSpace": {"type": "integer"},
                    "livingSpaceUnit": {"type": "string"},
                    "vacantFrom": {"type": "string"},
                    "numberOfRooms": {"type": "integer", "nullable": True},
                    "Garage/parking space": {"type": "string"},
                    "additionalSpecs": {"type": "list", "schema": {"type": "string"}},
                    "internetAvailable": {"type": "boolean"},
                    "internetSpeed": {"type": "string", "nullable": True},
                },
            },
            "price": {
                "type": "dict",
                "schema": {
                    "priceWithoutHeadting": {"type": "string"},
                    "priceperMeter": {"type": "string"},
                    "additionalCosts": {"type": "string"},
                    "heatingCosts": {"type": "string"},
                    "totalRent": {"type": "string"},
                    "basisRent": {"type": "string"},
                    "deposit": {"type": "string"},
                    "garage/parkingRent": {"type": "string"},
                    "priceCurrency": {"type": "string"},
                    "totalRent": {"type": "string"},
                },
            },
            "building": {
                "type": "dict",
                "schema": {
                    "constructionYear": {"type": "integer", "nullable": True},
                    "energySources": {"type": "string"},
                    "energyCertificate": {"type": "string"},
                    "energyCertificateType": {"type": "string"},
                    "energyCertificateDate": {"type": "integer", "nullable": True},
                    "finalEnergyRrequirement": {"type": "string"},
                },
            },
            "attachments": {
                "type": "dict",
                "schema": {
                    "propertyImages": {"type": "list", "schema": {"type": "string"}},
                    "videoAvailable": {"type": "boolean"},
                },
            },
            "agencyName": {"type": "string"},
            "agencyAddress": {"type": "string"},
        },
    }
}


search_schema = {
    "schema": {
        "type": "dict",
        "schema": {
            "@id": {"type": "string"},
            "@modification": {"type": "string"},
            "@creation": {"type": "string"},
            "@publishDate": {"type": "string"},
            "realEstateId": {"type": "integer"},
            "disabledGrouping": {"type": "string"},
            "resultlist.realEstate": {
                "type": "dict",
                "schema": {
                    "@xsi.type": {"type": "string"},
                    "@id": {"type": "string"},
                    "title": {"type": "string"},
                    "address": {
                        "type": "dict",
                        "schema": {
                            "street": {"type": "string"},
                            "houseNumber": {"type": "string"},
                            "postcode": {"type": "string"},
                            "city": {"type": "string"},
                            "quarter": {"type": "string"},
                            "wgs84Coordinate": {
                                "type": "dict",
                                "schema": {
                                    "latitude": {"type": "integer"},
                                    "longitude": {"type": "integer"},
                                },
                            },
                        },
                    },
                    "companyWideCustomerId": {"type": "string"},
                    "floorplan": {"type": "string"},
                    "streamingVideo": {"type": "string"},
                    "listingType": {"type": "string"},
                    "showcasePlacementColor": {"type": "string"},
                    "privateOffer": {"type": "string"},
                    "contactDetails": {
                        "type": "dict",
                        "schema": {
                            "salutation": {"type": "string"},
                            "firstname": {"type": "string"},
                            "lastname": {"type": "string"},
                            "company": {"type": "string"},
                        },
                    },
                    "realtorCompanyName": {"type": "string"},
                    "realtorLogoForResultList": {
                        "type": "dict",
                        "schema": {
                            "@xsi.type": {"type": "string"},
                            "floorplan": {"type": "string"},
                            "titlePicture": {"type": "string"},
                            "urls": {
                                "type": "list",
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "url": {
                                            "type": "dict",
                                            "schema": {
                                                "@scale": {"type": "string"},
                                                "@href": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                            },
                            "galleryAttachments": {
                                "type": "dict",
                                "schema": {
                                    "attachment": {
                                        "type": "list",
                                        "schema": {
                                            "type": "dict",
                                            "schema": {
                                                "@xsi.type": {"type": "string"},
                                                "floorplan": {"type": "string"},
                                                "@titlePicture": {"type": "string"},
                                                "urls": {
                                                    "type": "list",
                                                    "schema": {
                                                        "type": "dict",
                                                        "schema": {
                                                            "url": {
                                                                "type": "dict",
                                                                "schema": {
                                                                    "@scale": {
                                                                        "type": "string"
                                                                    },
                                                                    "@href": {
                                                                        "type": "string"
                                                                    },
                                                                },
                                                            }
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    }
                                },
                            },
                            "spotlightListing": {"type": "string"},
                            "verifiedBy": {
                                "type": "list",
                                "schema": {"type": "string"},
                            },
                            "price": {
                                "type": "dict",
                                "schema": {
                                    "value": {"type": "integer"},
                                    "currency": {"type": "string"},
                                    "marketingType": {"type": "string"},
                                    "priceIntervalType": {"type": "string"},
                                },
                            },
                            "livingSpace": {"type": "integer"},
                            "numberOfRooms": {"type": "integer"},
                            "builtInKitchen": {"type": "string"},
                            "balcony": {"type": "string"},
                            "garden": {"type": "string"},
                            "calculatedTotalRent": {
                                "type": "dict",
                                "schema": {
                                    "totalRent": {
                                        "type": "dict",
                                        "schema": {
                                            "value": {"type": "integer"},
                                            "currency": {"type": "string"},
                                            "marketingType": {"type": "string"},
                                            "priceIntervalType": {"type": "string"},
                                        },
                                    },
                                    "calculationMode": {"type": "string"},
                                },
                            },
                            "attributes": {
                                "type": "list",
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "attribute": {
                                            "type": "list",
                                            "schema": {
                                                "label": {"type": "string"},
                                                "value": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
}


@pytest.mark.asyncio
@pytest.mark.flaky(reruns=3, reruns_delay=30)
async def test_properties_scraping():
    search_data = await immobilienscout24.scrape_search(
        url="https://www.immobilienscout24.de/Suche/de/bayern/muenchen/wohnung-mieten",
        scrape_all_pages=False,
        max_scrape_pages=1,
    )
    urls = ["https://www.immobilienscout24.de/expose/" + i["@id"] for i in search_data]

    result = await immobilienscout24.scrape_properties(
        urls=urls[:3]
    )
    validator = Validator(property_schema, allow_unknown=True)
    for item in result:
        validate_or_fail(item, validator)
    assert len(result) >= 1
    if os.getenv("SAVE_TEST_RESULTS") == "true":
        result.sort(key=lambda x: x["id"])
        (Path(__file__).parent / 'results/properties.json').write_text(
            json.dumps(result, indent=2, ensure_ascii=False, default=str)
        )



@pytest.mark.asyncio
@pytest.mark.flaky(reruns=3, reruns_delay=30)
async def test_search_scraping():
    result = await immobilienscout24.scrape_search(
        url="https://www.immobilienscout24.de/Suche/de/bayern/muenchen/wohnung-mieten",
        scrape_all_pages=False,
        max_scrape_pages=3,
    )
    validator = Validator(search_schema, allow_unknown=True)
    for item in result:
        validate_or_fail(item, validator)
    assert len(result) >= 1
    if os.getenv("SAVE_TEST_RESULTS") == "true":
        result.sort(key=lambda x: x["@id"])
        (Path(__file__).parent / 'results/search.json').write_text(
            json.dumps(result, indent=2, ensure_ascii=False, default=str)
        )

