import requests
import json
import base64


def get_yelp_reviews(url: str, business_id: str, start_index: int = 1):
    try:
        # Construir el parámetro 'after' para la paginación
        pagionation_data = {"version": 1, "type": "offset", "offset": start_index}
        after = base64.b64encode(json.dumps(pagionation_data).encode("utf-8")) \
            .decode("utf-8") if start_index != 1 else None

        payload = [
            {
                "operationName": "GetBusinessReviewFeed",
                "variables": {
                    "encBizId": business_id,
                    "reviewsPerPage": 10,
                    "selectedReviewEncId": "",
                    "hasSelectedReview": False,
                    "sortBy": "DATE_DESC",
                    "languageCode": "en",
                    "ratings": [5, 4, 3, 2, 1],
                    "isSearching": False,
                    "after": after,
                    "isTranslating": False,
                    "translateLanguageCode": "en",
                    "reactionsSourceFlow": "businessPageReviewSection",
                    "minConfidenceLevel": "HIGH_CONFIDENCE",
                    "highlightType": "",
                    "highlightIdentifier": "",
                    "isHighlighting": False,
                },
                "extensions": {
                    "operationType": "query",
                    "documentId": "ef51f33d1b0eccc958dddbf6cde15739c48b34637a00ebe316441031d4bf7681",
                },
            }
        ]

        headers = {
            "authority": "www.yelp.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://www.yelp.com",
            "referer": url,
            "x-apollo-operation-name": "GetBusinessReviewFeed",
        }

        response = requests.post("https://www.yelp.com/gql/batch", headers=headers, data=json.dumps(payload))
        return response.json()

    except Exception as e:
        print(f"Error al hacer la petición a Yelp: {e}")
        return None
