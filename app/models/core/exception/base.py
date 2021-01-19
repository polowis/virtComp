


class CannotBuyBuildingOnRentLandscape(Exception):
    """
    Raise if unable to buy building on rent landscape
    """
    def __init__(self, message: str = 'Cannot buy building on a landscape that on rent'):
        self.message = message
        super().__init__(self.message)


class NegativeLevel(Exception):
    """
    Raise negavtive level exception
    """
    def __init__(self, level: int, message: str = 'Expect positive number but got negavtive number'):
        self.level = level
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} but got {self.level}'


class IncorrectOnwer(Exception):
    def __init__(self, message: str = 'Wrong owner'):
        self.message = message
        super().__init__(self.message)


class UnableToConstructBuilding(Exception):
    """Throws if unable to construct a building"""
    def __init__(self, message: str = 'Unable to construct building'):
        self.message = message
        super().__init__(self.message)


class UnableToOwnLandscape(Exception):
    """Throws if unable to own a landscape"""
    def __init__(self, message: str = 'Unable to rent landscape'):
        self.message = message
        super().__init__(self.message)
    

class UnableToAssignEmployee(Exception):
    def __init__(self, message: str = 'Unable to assign employee'):
        self.message = message
        super().__init__(self.message)