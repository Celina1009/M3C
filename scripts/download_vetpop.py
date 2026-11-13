from pathlib import Path
import hashlib
import urllib.request

URL = "https://uofi.box.com/shared/static/claymwl2hzbzxdkp6yc5q6vaee59hsnp.csv"
EXPECTED_SHA256 = "b0787e318ca6d5abc648c11068f7c9de3997c44a1e3484010701d6472b4c47ed"

root = Path(__file__).resolve().parent.parent
data_dir = root / "data" / "raw"
destination = data_dir / "VetPop2023 county data.csv"
temp = data_dir / "VetPop2023 county data.csv.part"

data_dir.mkdir(parents=True, exist_ok=True)
print("Downloading VetPop from Box...")
urllib.request.urlretrieve(URL, temp)

actual = hashlib.sha256(temp.read_bytes()).hexdigest()

if actual != EXPECTED_SHA256:
    temp.unlink()
    raise ValueError("Checksum mismatch!")

temp.replace(destination)
print("Download and checksum verification successful!")