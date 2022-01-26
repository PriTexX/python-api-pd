import requests

resp = requests.get('http://pd-scripts.herokuapp.com/getScheduleForYear?token=d%252BOECWrwh4sVizxuOf6A3zhCrXz2XGtx5jzAtKabSewJmCJs9HQq6TC61qiEtfnCKB1QjAWeLOA0b0aPIFi%252BE%252ByxUeHElWc1pxlKNjW5Ef1%252FYQGPU895dPsJl6PKnt5YvNqsUBCi%252BPyZwYaK%252FPPUI8KQi5IuwK1ctRpGUtw9Lqg%253D')

print(resp.content)
