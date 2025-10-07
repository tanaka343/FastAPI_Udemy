import requests

url = 'https://jsonplaceholder.typicode.com/posts'
#すべてのポストを取得
# res=requests.get(url)

# print(res.status_code)
# datum =res.json()[0]
# print(datum['body'])

#id is 3 only
params = {
    'id':3

}

res =requests.get(url,params)
print(res.status_code)

print(res.json())