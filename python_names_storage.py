from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  
  "type": "service_account",
  "project_id": "optimum-mode-382118",
  "private_key_id": "59b88f77535186f5af5bcc394af92f5a2dc26708",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDXXWZ0+mMrcUhD\nq3mJmkiB/QYaa3PSPsXW0pR4cx4nTOGTh2SpZVnLXeGmWfpnp9KBbLUIMSv6b1aR\nsaFjpMTnp7IKBDKd4J3dBR/dRllB3wKbZFuuAygZ7STZk5I02qOF6OCWF792AQFY\n60MyHiarqKyUVSo61oMIzZsXMffB+FVm0K71Mh0zEfvxnWrNoEj/W6CHxba0cFrt\nzd5hJgFzWaiVf/m+yCkBTwLam5fvqFvO00KMGNFuyZp0GQTbp/y0K884YRcfM5fx\nk21XbfF6+5D/WPpXcwZESl3veoeKyF5Ks0+oqA7qVFPfAT4KJXdQtD9Vt4K0VSQv\nc4GXA38pAgMBAAECggEAAP1XvAkPGldMJFdQX/3BKwWrxep9vvqBA1ZTRP8D58Cf\nUS5XT/ZUHVbI1xF6jmJE2bHYEquZ1w8rP3H+EU3HYDj8WAuDVmaa+jW5tQ4JOBLm\nFMwye1rZUkmfKRjvksvcecKRocYK1EI+xo/ctb1lD9+cgs/CaP39WduPaox/0up1\nFxB6sgrU55IVR6IPi4YUtew/cdpthGqu38KCwCyhZHOEoZpPL/Pf5YQVtUaz55yu\nSQ1lqwuYJkSJ99wUoFON9MvFgphjDWNDzCkpwaFFhibLZMDhiOyRd5p23BhRgAvV\nbr29hPTY/ETJj4QAqaC44uhmltAncGGckSjVjKInAQKBgQD3N4bvCOlSbK/a+jap\nbWKxkEpSVKU++j/8Ws1/IvFV7QDnHxNlenG0Yt9mStqt/mBWJSoT0YmOpodF+k7u\nIB4kpFJ76dvropUgj0N8J6fIWl/sgGzNdDp6MBYoyaBD10uQWq48/MHwb/a0/j2G\n2v2iG4+cvrU6G+I3SG4iLxvo4QKBgQDfBCyUMEB+bfQ3wCPbY5TC+UGzDYxdYYwe\nqYAkilNzynXvQ6CUvKZtpMe8Jf6QYpF/5E2MbZvgwzP+LzFanQikukkGHCNdLABJ\n14/1G/JUDw1fjSP4+l5nuda+87xB8WKstH5BZnqF7nP+ZWbnw5erVTvLZp2CClEP\ngm73lP33SQKBgHxFPV8La74zRHMfNDsW8XWwwquAQVDXGzMPsh0mw4oeCUYlKOrq\nEh5LVWFmX2b3aBXluLEds7gxne5fVS3+lyh0McJ4XESnBa/IVHQkuwLL60xHgmoE\n8yBY68q1EAsKPsHh05R0ukjS/4EcDHGtw7GpiReSBiefvKdtkW89nxoBAoGAQ14K\nbVVKFib2z+R9sGcbZ+5Nl13vWcH+xsBjEiaq4N5206j1GBkImTRelYpQpKLx2tVH\nS7VMkg/FY/IzkXDATKptJqhXUmzZRXUVanBful61pniHNk3DOMgdg58y7iSRryPy\nw6TGPDD03xMYi8g8x6e+oUnFKKQfKnU3OhjKwukCgYB6Eo2Nkh9/SasXpaVoXjiu\n+NMUOG3Yj8xxDRWC8kcXApIvK4MH6aLWuqTpn5pfBi0zLomgODRJLiTx+iv9wpaj\noZPqhZknHv3LZA8HPdGnTP+5FaATh06i46bw+U3905bPtehFfJ26v3YM4erv/E4a\nwj32OBIy0RqredocLqiNaQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "pedroz@optimum-mode-382118.iam.gserviceaccount.com",
  "client_id": "103505337958841825447",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pedroz%40optimum-mode-382118.iam.gserviceaccount.com"

}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('ativ4_dataops') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
