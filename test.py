class School:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name
    
    # def __str__(self) -> str:
    #     return self.name
    
obj = School("MIT")
print(obj)
