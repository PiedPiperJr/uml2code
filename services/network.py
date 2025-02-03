import os
import requests

def download_file(url: str, output_dir: str) -> None:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(os.path.join(output_dir, 'pom.xml'), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)