import requests
import json


def send_api(path, method):
    API_HOST = "https://www.bigkinds.or.kr/api/news/search.do"
    url = API_HOST + path
    # headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    headers = {
        "accept-language": "en-US,en;q=0.9,ko;q=0.8,ko-KR;q=0.7,ja;q=0.6",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }

    body = {"indexName":"news",
            "searchKey":"hi",
            "searchKeys":[{}],
            "byLine":"",
            "searchFilterType":"1",
            "searchScopeType":"1",
            "searchSortType":"date",
            "sortMethod":"date",
            "mainTodayPersonYn":"",
            "startDate":"2022-08-01",
            "endDate":"2022-11-01",
            "newsIds":[],
            "categoryCodes":[],
            "providerCodes":[],
            "incidentCodes":[],
            "networkNodeType":"",
            "topicOrigin":"",
            "dateCodes":[],
            "editorialIs":"false",
            "startNo":1,
            "resultNumber":10,
            "isTmUsable":"false",
            "isNotTmUsable":"false"}

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        print("response status %r" % response.status_code)
        print("response text %r" % response.text)
    except Exception as ex:
        print(ex)


# 호출 예시
send_api("", "POST")