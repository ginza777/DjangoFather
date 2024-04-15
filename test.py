import requests
import json
import os
import time


def get_new_token():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': '_gcl_au=1.1.558858711.1710348550; tmr_lvid=0d99118a952e4141222dfb59d523606f; tmr_lvidTS=1710348549818; _gid=GA1.2.1918091690.1710348550; _ym_uid=1710348550616172014; _ym_d=1710348550; access_token=eyJraWQiOiIwcE9oTDBBVXlWSXF1V0w1U29NZTdzcVNhS2FqYzYzV1N5THZYb0ZhWXRNIiwiYWxnIjoiRWREU0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJVenVtIElEIiwiaWF0IjoxNzEwMzQ4NTUxLCJzdWIiOiIyZmFjNGM5Ni02ZmMwLTQyOTctODA0Yi1kMWQ4NzU0YjFmOTAiLCJhdWQiOlsidXp1bV9hcHBzIiwibWFya2V0L3dlYiJdLCJldmVudHMiOnt9LCJleHAiOjE3MTAzNDkyNzF9.ffJdn0EanTyh4mjD1Ncj-jqBgGstZZ4geqwSdXluPmpn9mjo2lggymor6L7Kckf2vxXnuKJ3k78fpxnnAngNBg; refresh_token=v4Oi%2FACVN8AwbVhqfYqhy06cTTJ8Cqy2ZzUbtikyF4XI9qt3KhDkIkufpiLIpwZW%2BhP479Yk%2FN8BIpeEckB6sbVi8k5A0clfT3yHLD6wyMj3IdMkpSwd1Iv%2FYelDKkzt101mFhdmKJq6YwwygRC3jzie1jse7TjdagSBMtsvq%2FgqfXpFTwQIgW%2ByaL8MrXxY95TBvqCL8Yrk1ACk2OIq7ZLSQP2vt8vjNkRU74dFrjCfRC0pRmeFpmoKQp7YV1%2FEOevOYJvM%2Fzbmxi5psUzkWnTUe79bGamCsNytRUwYlP8XbPfK%2BsoaUYw007uXFRdEvind087AURpwvTJagK%2Brx9xxZn1n%2BmIjs%2FdPI9M%2FAXH5YNd3Tafm0CAhofFSzNK%2BcmwPVuACgVvozIS6XkkYt3Qcem19QxrJrOmbqv32Dqbme88Bk83gy8RZr49HzpXJ1l0x%2FaYmbBb7h5ttA5Zfkag0P8oKGK8ok9h5qqEQE9Imz1tCBSpJLbdPCW5%2FhhNVmzu950V3ZG40eqtb%2B5A6%2FfPgwDVSY6QoUcC3hxB8fAYtv3roWz6Ywmk1zGj82mEWWVb08Fqonmo7BTFhZq8xdMOQnhsJ8vyG%2FCUTTM0k8yOaYyTtsM9d2zkF6uuGo85C6bpe9PPd7ulSzx1j2hY17jyROZIjzpCDWz0m8CMcDqXkPqlD87aVkZq8rZdu%2FFUQSiQVB74%3D--NzfJH21je%2F8FRgTg--dxkboG%2F8l72llP0C%2BnYVvA%3D%3D; _ym_isad=2; _fbp=fb.1.1710348550284.1100734468; cf_clearance=rM2yoJB2ha7.N68OFqcJ4Vn4o1Axyb3IyTuf0jjqN8k-1710348551-1.0.1.1-RxtkTdiQvEt51hD_pXZ0obpoXtPMgQtLryixHtPtxWFC06Wy5n6hWaPwFZre6TDc17v6srpCPGSwVojgR8D9Cw; _ym_visorc=b; _ga=GA1.1.225888920.1710348550; _ga_7KCSSWWYYD=GS1.1.1710348549.1.1.1710348635.59.0.0; _ga_EZ8RKY9S93=GS1.2.1710348550.1.1.1710348636.0.0.0',
        'Origin': 'https://uzum.uz',
        'Referer': 'https://uzum.uz/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'baggage': 'sentry-environment=production,sentry-release=uzum-market%401.19.0,sentry-public_key=e1a87daa698047a7ace4c53be14f63e8,sentry-trace_id=801c8f340642486c931a107764f5e97e',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sentry-trace': '801c8f340642486c931a107764f5e97e-b81f00c869633d7a-0',
    }

    response = requests.post('https://id.uzum.uz/api/auth/token', headers=headers)
    cookie_data = response.headers.get("Set-Cookie")
    access_token = cookie_data.split(';')[0].split('=')[1]
    return access_token


def get_product_info(product_id: int, access_token) -> dict:
    """
    Get product info
    """

    data = os.popen(f"""
    curl 'https://api.uzum.uz/api/v2/product/{product_id}' \
  -H 'authority: api.uzum.uz' \
  -H 'accept: application/json' \
  -H 'accept-language: uz-UZ' \
  -H 'authorization: Bearer {access_token}' \
  -H 'baggage: sentry-environment=production,sentry-release=uzum-market%401.18.9,sentry-public_key=e1a87daa698047a7ace4c53be14f63e8,sentry-trace_id=112cc133f645442ba94e3573e1166266,sentry-sample_rate=0.001,sentry-transaction=product,sentry-sampled=false' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'origin: https://uzum.uz' \
  -H 'pragma: no-cache' \
  -H 'referer: https://uzum.uz/' \
  -H 'sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'sentry-trace: 112cc133f645442ba94e3573e1166266-8003c1ff2eedc07f-0' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36' \
  -H 'x-iid: dccec7d3-2f25-481d-ac39-856fccb37203'""").read()
    try:

        data = json.loads(data)
        print(data)
    except Exception as e:
        data = {}
    return data


def get_product_id_list():
    url = "https://uzum.ruzimurodov.uz/api/v1/product/product-ids/"
    data = requests.get(url).json()
    return data.get("ProductIds", [])


def send_product_info(product_id: int, data: dict):
    url = f"https://uzum.ruzimurodov.uz/api/v1/product/product-detail/{product_id}/"
    print(100*"#")
    print(data)
    response = requests.post(url, json=data)
    print(response.ok, response.status_code)
    return response.json()


def main():
    access_token = get_new_token()
    product_ids = get_product_id_list()
    print(100*"$")
    print(product_ids, access_token)
    for product_id in product_ids:
        try:
            product_info = get_product_info(product_id, access_token=access_token)
            print(product_info)
            if product_info and product_info.get("payload") and product_info.get("payload").get("data"):
                product_info = product_info.get("payload").get("data")

                send_product_info(product_id, product_info)
                time.sleep(0.1)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(6)
