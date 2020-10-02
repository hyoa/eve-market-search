from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests
import socket

class ConcurrentFetcher:

  def __init__(self, parser=None):
    self.result = []
    self.parser = parser
    pass

  def pull(self, urls):
    with PoolExecutor(max_workers=4) as executor:
      for data in executor.map(self.fetch, urls):
        if isinstance(data, list):
          self.result = self.result + data
        elif isinstance(data, dict):
          self.result.append(data)
        
    return self.result
  
  def fetch(self, url):
    try:
      response = requests.get(url, timeout=1)

      if self.parser:
        return self.parser(response.json(), url)

      return response.json()
    except requests.exceptions.RequestException:
      print('error')
      return list()
    except:
      print('error 2')
      return list()