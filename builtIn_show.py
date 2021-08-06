#Setup  
#%%
import math
list_of_num = [1,2,3]
#%%
print(abs(-1)) # returns 1
#%%
print(bin(13),hex(13),oct(13))
#%%
print(int(13.1),float(13),str(13))

#%%
print(bool(1),bool(0))

#%%
print(bool(""),bool("Empty"))

#%%
print(chr(1200),ord(chr(1200)))
#%%
print(dir(math))
#%%
for x,y in enumerate(list_of_num):
    print(x,y)
#%%
print(eval("list_of_num")) #get varible
#%%
exec("print('printed from a string')") #run code
#%%
for x in filter(lambda x: x%2 == 0,list_of_num):
    print(x)
#%%
print(isinstance(13.0,(int,float)),isinstance(13.0,int))

#%%
print(len(list_of_num))
#%%
print(max(list_of_num),min(list_of_num))

#%%
t = iter(list_of_num)
print(next(t,-1),next(t,-1),next(t,-1),next(t,-1),next(t,-1))
#t.__next__

#%%
# open
#%%
print(list_of_num, list(reversed(list_of_num)))
#%%
print(round(13.4),round(13.5),round(13.56456464645416541,3))

#%%
print(list_of_num[slice(0,3,2)])
#%%
names = ["Michael","Christopher","Jessica","Matthew","ashley","Jennifer","joshua","Amanda","Daniel","David","James","robert","John","Joseph","Andrew","Ryan","brandon","Jason","iustin","Sarah","William"]

print(sorted(names))
#%%
print(sorted(names, key=str.lower))
#%%
print(sum(list_of_num))
#%%
print(type(list_of_num),type(13),type(13.0))
#%%
print(list(zip(list_of_num,names)))
# %%
