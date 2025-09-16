import requests

HOST = "https://otlp-gateway-prod-gb-south-1.grafana.net/otlp/v1/metrics"
API_KEY = ""

BODY = """{
  "resourceMetrics": [
    {
      "scopeMetrics": [
        {
          "metrics": [
            {
              "name": "test_metric",
              "unit": "s",
              "description": "",
              "gauge": {
                "dataPoints": [
                  {
                    "asInt": 1,
                    "timeUnixNano": 1758041068201000000,
                    "attributes": [
                      {
                        "key": "bar_label",
                        "value": {
                          "stringValue": "abc"
                        }
                      }
                    ]
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}"""

response = requests.post(
    HOST,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    data=BODY
)

print(response.status_code)
print(response.text)
