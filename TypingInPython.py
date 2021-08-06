class standardClass:
# cant variable without typing or default value
    dec: int
    dec2: float = 6
    def __init__(self,dec: int,dec3: str,dec4: int=0):
        self.dec = dec
        self.dec3 = dec3
        self.dec4 = dec4
    def varis(self) -> None:
        print(self.dec,self.dec2,self.dec3,self.dec4)

t= standardClass()
def typingFunction(accept: bool, accept2: str = "") -> str:
    return f"Congratulations, you {'Passed' if accept else 'Failed'}. {accept2}"