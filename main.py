import os
from dotenv import load_dotenv
import requests

load_dotenv()

username = os.getenv('EARTHDATA_USERNAME')
password = os.getenv('EARTHDATA_PASSWORD')
url = "https://discnrt1.gesdisc.eosdis.nasa.gov/data/Aqua_NRT/AIRIBQAP_NRT.005/2015/059/AIRS.2015.02.28.047.L1B.AIRS_QaSub.v5.0.22.0.R15059002902.hdf"

class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname != self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return


session = SessionWithHeaderRedirection(username, password)
filename = url[url.rfind('/') + 1:]
try:
    response = session.get(url, stream=True)
    print(response.status_code)
    response.raise_for_status()
    with open(filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            fd.write(chunk)
except requests.exceptions.HTTPError as e:
    print(e)