from array import array
import struct
from xml.etree.ElementTree import tostring
import requests
import json

def get_links(): 

  url = "https://www.waitrose.com/api/content-prod/v2/cms/publish/productcontent/browse/-1?clientType=WEB_APP"

  startNo = 1
  sizeNo = 128
  preList = []
  listOfProds = []

  while startNo < 5000:
    payload = json.dumps({
      "customerSearchRequest": {
        "queryParams": {
          "size": sizeNo,
          "category": "10051",
          "filterTags": [],
          "sortBy": "MOST_POPULAR",
          "orderId": "0",
          "start": startNo
        }
      }
    })
    headers = {
      'authority': 'www.waitrose.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'authorization': 'Bearer unauthenticated',
      'breadcrumb': 'browse-fe',
      'content-type': 'application/json',
      'cookie': 'mt.v=2.857123761.1655247124725; wtr_cookie_consent=1; wtr_cookies_advertising=1; wtr_cookies_analytics=1; wtr_cookies_functional=1; _gcl_au=1.1.454583516.1655247127; _gid=GA1.2.841286658.1655247127; _cs_c=0; _fbp=fb.1.1655247127615.845036290; _pin_unauth=dWlkPU5UVmhOemcwWm1RdE9EazROaTAwTUdZekxXSmtZV0V0T1RSbU0yTTJORGhtT0RRdw; eds=INS-vi42-303388996:265076283-1655247127^709016667-1655247127; _hjSessionUser_1434770=eyJpZCI6IjdjMTIxYjVmLTRjODItNWM1MC1hMDllLWVhYTYxNjJiMzAyYyIsImNyZWF0ZWQiOjE2NTUyNDcxNDE2NTAsImV4aXN0aW5nIjp0cnVlfQ==; _abck=2203AED3FEE0BA9218EB4DE5F9FF3D54~0~YAAQuO1lX3WtLymBAQAA+T6NZwi9LYYUDiXtS6WLcEuDNCgOlmHAVDWKs/QcXL+P4Xjf9OLo0jqNHe77+4aekkQz9HQsRb9cU8zgdZvmeXlk2YTGBnwegl4PXuMk8AbcEgbOPp01co0HIXwcxS1wHk4EEgjtJCKtv6YVjW7fIxVevwCkcNePUGLO4ibNP924as3v9PJUPck7vXcnRl+T/wC2WrCcipGaJ00XaVV491JYa3tnIgMLNXAqTn/qMH8ZceEyyd+y9zn7RyIW4iPrv8Ltk2I6ulhPt+VExROqgU9SR2LdX7qZPHvVc8LFQULWSbPewQUOTVEKHJiPK73+JJ4FdFJWCy/iA2J23rAzZdos7ANirmIsf0292r1BY+7bzM0VqnTAAyqCqzwm7d2i6cfQWZzIcpBoc/8=~-1~-1~-1; bm_sz=638C262FF3B7306387C27A5C000A3E1E~YAAQuO1lX3itLymBAQAA+T6NZxDGFlEEgZQY98hT6eE6ukk3HaEhZdkeH8jjQzixqbCW4YdhikvnOXJXt9CqLVJHFL0KOeHb0Jh+dOGhokUFjBTf/oPEBGAwdExMi3t15/cAfxPjzT1Vn6qH3io0k2/zDCasYIFrdjFeDLnU3+eiYash1HBhGrWUrJq/NwvCC4YV1JqnJQuZa3pcTBziypgRF4w2lFNxtdhoZAqskKPUayaRlocu8N56/cu9G3mKRgDhj8bfBvGQ9gF1zwx4gvOnvYrnIPYEzDeF/6LKiJXmsuWFyQ==~3748916~4469042; akacd_RWASP-default-phased-release=3832752517~rv=44~id=f9ad485a3d43049c88018b7b5230b186; PIM-SESSION-ID=EB6lcq0xd4aMCdN9; IR_gbd=waitrose.com; _hjCachedUserAttributes=eyJhdHRyaWJ1dGVzIjp7ImJyYW5jaF9pZCI6bnVsbCwic2hlbGZfbGlmZV90cmlhbCI6ImNvbnRyb2wifSwidXNlcklkIjoiLTEifQ==; mt.sc=%7B%22i%22%3A1655311601748%2C%22d%22%3A%5B%22cs%3Borganic%22%5D%7D; IR_12163=1655311601905%7C0%7C1655311601905%7C%7C; website_csat_session=2022-06-15:9251976723; ak_bmsc=6741DA2DDDF2E54A89DD612A201A7445~000000000000000000000000000000~YAAQJDAQYNN9liSBAQAAIJBCaBDHjls8reJ+NCD9SXcAkn0Hpmi6EcXGb0bAYkNSFsagfLO8fyOfl+7JX8+ang75OsrkKz4NsSdXiWvA3n113V3rD+ZWM/fDt0D567aJe4y1fnfTcwfspmuX253Jr8CClPgcFCbAoHnyDARFH88wq9W/WLI0P1GMlWyzonPVGbBYa0/ggQWKRkmWmWZ2xv73cSGIqUEoVAobIsQVssG6ITjIlhIJ4w6Vw0MWIAkdCKq46swtGCOku2RtNMXyv42h2huxZz+qz5fBoTCXkHQSarZPVHTcUJG6KL4UZ9htp3gZVroLsBD8WJMXKlFRYJiqJF7x8NXSlJaP1ON2Bela1RaIMaFUSFuVgaV0a/e0RZs3AsOyzOfxot49n4NFW13QSzy6BeqQyr1kULmVId0By6x7+0LadYXPtAE5tkroxfAii9/EuGmLmQcIpmaMaHYQWgfWSSyachEuW7Z5067k9CiRvfLGLl0=; _cs_id=5a15352c-7dba-a01f-b6b3-8e54f7bc364f.1655247127.4.1655311602.1655311364.1.1689411127496; _cs_s=2.0.0.1655313402267; _hjIncludedInSessionSample=0; _hjSession_1434770=eyJpZCI6IjRmNzEwN2E0LTk0NWYtNDZjZC04NDg4LTNjY2U1ZmM0OWZjZCIsImNyZWF0ZWQiOjE2NTUzMTE2MDI2ODUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga=GA1.2.550942866.1655247127; _gat_UA-34398547-2=1; _ga_8YN3DG5SKT=GS1.1.1655311600.3.1.1655311836.60; ecos.dt=1655311860282; _abck=2203AED3FEE0BA9218EB4DE5F9FF3D54~-1~YAAQJDAQYCuPliSBAQAAhORIaAgPKdAsqtYqKSVQ9i9OaTog0zAbrukvVHFFAYLD3msofpbfoIfJBcq+te90jl5PubyVSNsmFxaE8PXvmaCC8AIJWZkqWUPpTBUrT1QvxvTiHkp33I9tWu5Hw9wGCCHKkDe+MJqNcVdysmSNmYJZVqHPGCvCvT8uldub7hjW7rcsH46eFtzyp+0oyVq1tl9S9nDBlmhwxxJO5ov7o7K+1VOrgr4mh6d0keOCgC62dM2UNa7/2rBKl9BZWNx1mkWR+KXie+FDr/OCgmGswJjy/eLsbKzYrlc7b61HQY8rN+gpETKhFbsUZdQyBkUM3/DL4BPAhkPRBXvlT4RSx6L23/jE/6reO+lUSczlk4LSuLnk6uMjLtJD04hKf68jf4fJmNID9kafP5Q=~0~-1~-1; bm_sv=55ED2181A31EE80441D590667522501A~YAAQJDAQYCyPliSBAQAAhORIaBAaLVkiRGjMOz8LyliMb0l891U/jW2FaIwNKKw1+clZxMzfvXr8ph8gfNaohHZJEo8WpKtY6iilaumtbW8A1cLyTHE5R5W7hjoCKVCagvFNjHWYGv/deCHG+1/a+Aor9BjU4PuwtXMvNovwfsALS8nlbkrN1wwQwfM6NGH3qA3HjjQLSPB58QNyCCPiHg6Tcmn2faKtC6Jt2AWoUWhpcc3MNjNml1G8sitVy5/Sh/0=~1; bm_sz=4AC3A65FB37AC3D20979288487F2B37D~YAAQuO1lX67xMCmBAQAANzKZZxBD35LORMclH9HPZrVv4J2p6mYq++170bY/yqiuY7eRAtFJhk4ZDRe8fkFKr+tE4LeJ64QGgQtBwiKFV7vLH0M7xpD/zL6TFlpkhDY7Re3rt+FK7jdpe+Bi82dm3Dl8lNznELeud+ZLVsDXJDWCWDQwk2KUGPfRQX43lzXEfZFrsr9T3RSXwwdgK+LQrfMI3lwcF1+rjwBo/H1twWD87EZSotnZ1Srad5z2Haw9hxVnf8EfSTexRaNilFsGo3u3/BXOZXVSGje985fxFvuis9C9Zw==~3748153~4534851',
      'features': 'samosa,enAppleWallet',
      'origin': 'https://www.waitrose.com',
      'referer': 'https://www.waitrose.com/ecom/shop/browse/groceries',
      'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

    startNo += sizeNo
  #cookie will need to be refreshed -- 

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)

    preList.append(data)

  # print(data["componentsAndProducts"])
  #print(preList)


  for dictionary in preList:
    for prod in dictionary["componentsAndProducts"]:
      name = prod["searchProduct"]['name'].replace(" ", "-")
      url = "https://www.waitrose.com/ecom/products/" + name + "/" + prod["searchProduct"]['id']
      listOfProds.append(url)

  return listOfProds
