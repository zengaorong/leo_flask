import requests



data = {
    'METHOD' : '19',
    'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJUSU1FIjoxNTQzNDg3NDk0LCJTSEFSRElOR19JRCI6Ijc5NiIsIlVTRVJOQU1FIjoiY2FyMTM2MDA4In0.Ew-EJgXz3o-_E3ICPi8IDa_7st61RnFD_MacCjjwM_A',
    'ACTION' : '671',
    'CODE' : 'JX_JA_ROOM_100653470',
    'SHARDING_ID' : '796'
}

headers = {
    'Content-Type' : 'application/x-www-form-urlencoded',
    'User-Agent' : 'Dalvik/2.1.0 (Linux; U; Android 6.0; EVA-AL10 Build/HUAWEIEVA-AL10)'
}
respoons = requests.get("http://127.0.0.1:8088/telecom/retired/test", data=data, headers=headers)
print respoons.text