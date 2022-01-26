import requests

resp = requests.get('http://pd-scripts.herokuapp.com/getScheduleForYear&token=d%2BOECWrwh4sVizxuOf6A3zhCrXz2XGtx5jzAtKabSewJmCJs9HQq6TC61qiEtfnCKB1QjAWeLOA0b0aPIFi%2BE%2ByxUeHElWc1pxlKNjW5Ef1%2FYQGPU895dPsJl6PKnt5YvNqsUBCi%2BPyZwYaK%2FPPUI8KQi5IuwK1ctRpGUtw9Lqg%3D')

print(resp.content)
