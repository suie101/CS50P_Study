class Jar:
    def __init__(self, capacity=12):
        # __init__ is called automatically when creating a Jar object.
        # Example: jar = Jar(10)
        # self means "this object". These assignments call the setters below.
        self.size = 0
        self.capacity = capacity

    def __str__(self) -> str:
        # __str__ controls what print(jar) displays.
        # "🍪" * 3 becomes "🍪🍪🍪".
        return "🍪🍪"*self.size
        
    def deposit(self, n) -> None:
        # Add n cookies to the jar.
        # Note: this currently changes size first, then checks capacity.
        # A stricter version could check self.size + n before assigning.
        self.size += n
        if self.size > self.capacity:
            raise ValueError("Out of capacity! ")

    def withdraw(self, n) -> None:
        # Remove n cookies from the jar.
        # Because size uses a setter, setting it below 0 can raise ValueError.
        self.size -= n
        if self.size < 0:
            raise ValueError("Cant be smaller than 0!")

    @property
    def capacity(self):
        # @property lets us read jar.capacity like an attribute,
        # while actually returning the private variable self._capacity.
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        # @capacity.setter lets us assign jar.capacity = value.
        # This is where we validate the value before storing it.
        if capacity < 0:
            raise ValueError ("capacity should be a non-negative int ")
        else:
            # Prefixing with _ is a convention: _capacity is for internal use.
            self._capacity = capacity

    @property
    def size(self):
        # Same idea as capacity: jar.size reads from self._size.
        return self._size
    
    @size.setter
    def size(self, n):
        # This setter protects size from becoming negative.
        if n < 0:
            raise ValueError ("size should be a non-negative int ")
        else:
            self._size = n
