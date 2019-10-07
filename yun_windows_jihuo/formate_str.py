#coding=utf-8
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cf = ConfigParser.ConfigParser()
cf.read("omg.config")
print cf
front = cf.get("around", "front")
back = cf.get("around", "back")


show_out_list = ""
with open('strs.txt','r') as f:
    show_out_list = f.readlines()

out_list = []
dict_check = {}
for str_out in show_out_list:
    if dict_check.has_key(str_out):
        continue
    else:
        dict_check[str_out] = str_out
    str_out = str(front) + str_out.replace('\n',"") + str(back) + '\n'
    out_list.append(str_out)

print out_list

with open('out.txt','w') as f:
    f.writelines(out_list)


