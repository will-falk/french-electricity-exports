import requests

headers = {
    'Authorization' : 'Bearer sk_a0ec55ce660f54143b752cf22fc5b7adb916e61ec2b50ecc'
}

get_response = requests.get(
    'https://free.mockerapi.com/mock/d00423bb-4fdb-4bc8-914d-0ce014d6723e',
    headers=headers)

print(get_response.json())


headers = {
    'Authorization' : 'Bearer sk_4ce197b9ded37904a3da3dc14361d23ab49f8dd9e9d4916d'
}

post_response = requests.post(
    'https://free.mockerapi.com/mock/fb8ba731-3b7c-49f7-9555-fe6f6e947fba',
    headers=headers,
    json={'country': 'DE', 'flow': 1200})

print(post_response.json())
