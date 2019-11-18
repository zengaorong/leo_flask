import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("IPdetail.config")

cityIP = cf.get("IP", "cityIP")
townIP = cf.get("IP", "townIP")

print cityIP,townIP



cf.set("IP","cityIP","123")
cityIP = cf.get("IP", "cityIP")

with open("IPdetail.config",'w') as fw:
    cf.write(fw)

print cityIP