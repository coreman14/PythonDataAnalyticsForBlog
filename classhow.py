#%%
class standardClass:
# cant variable without typing or default value
    dec: int
    dec2 = 6
    def __init__(self,dec,dec3,dec4=0):
        self.dec = dec
        self.dec3 = dec3
        self.dec4 = dec4
    def varis(self):
        print(self.dec,self.dec2,self.dec3,self.dec4)
#%%        
t = standardClass(1,2)
t.varis()
#%%
class sharedVaries:
    listvalue = [1,2,3]
#%%
t2 = sharedVaries()
t3 = sharedVaries()
t2.listvalue.append(4)
print(t3.listvalue)
#%%
t3.listvalue.clear()
print(t2.listvalue)



#%%
class Person:
    agent = "Mikey"
    age = 10
    pet = "dog"
    
    def __init__(self,snack="Cookies"):
        self.snack = snack
    
    def greet(self):
        print(f"Hello my name is {self.agent}, i am {self.age} old and i have a pet {self.pet}")
#%%        
p1 = Person()
p2 = Person()
p1.greet()
#%%
p1.age = 11
p1.greet()

#%%
print(p1.snack)
del p1.snack
try:
    print(p1.snack)
except:
    print("Missing attribute snack")
#%%  
print(Person.age)
del Person.age
try:
    print(Person.age)
except:
    print("Missing attribute age")
#%%
try:
    print(p2.age)
except:
    print("Missing attribute age")

#%%
p3 = Person()
p3.age = 11
print(p3.age)
#%%
try:
    print(Person.age)
except:
    print("Missing attribute age")
#%%
Person.age = 10
print(Person.age)
#%%
print(p2.age)

#%%
def greetEvil():
    print("HAHA, it was me, DIO")
#%%
p3.greet = greetEvil
p3.greet()
#%%
p2.greet()
#%%
Person.greet = greetEvil
try:
    p1.greet()
except Exception as e:
    print(e)
#%%
def greetEvilForClass(self=None):
    print("HAHA, it was me, DIO")
    
#%%
Person.greet = greetEvilForClass
p1.greet()