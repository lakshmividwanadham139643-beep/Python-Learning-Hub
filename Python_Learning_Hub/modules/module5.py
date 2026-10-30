import tkinter as tk
from tkinter import messagebox

import config as cfg
from utils.helpers import center_window, make_button


# ==========================================
# SUPPORTING CLASSES FOR THE MINI APP
# ==========================================

class BankAccount:
    """Demonstrates encapsulation: balance is 'protected' behind methods."""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance   # leading underscore = "protected" by convention
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self.history.append(f"Deposited ₹{amount:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient balance.")
        self._balance -= amount
        self.history.append(f"Withdrew ₹{amount:.2f}")

    @property
    def balance(self):
        return self._balance


class SavingsAccount(BankAccount):
    """Demonstrates inheritance + polymorphism: overrides deposit() to add interest."""

    def __init__(self, owner, balance=0, interest_rate=0.02):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        super().deposit(amount)
        bonus = amount * self.interest_rate
        self._balance += bonus
        self.history.append(f"Interest bonus: ₹{bonus:.2f}")


# ==========================================
# MINI APPLICATION — Bank Account Simulator
# ==========================================

def launch_mini_app(parent):
    """A tiny banking simulator — demonstrates classes, objects, self,
    constructors, encapsulation, inheritance, and polymorphism."""

    win = tk.Toplevel(parent)
    win.title("Mini App — Bank Account Simulator")
    win.configure(bg=cfg.WHITE)
    center_window(win, 440, 520)
    win.resizable(False, False)

    tk.Label(
        win, text="🏛️ Bank Account Simulator", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H3
    ).pack(pady=(20, 4))

    tk.Label(
        win, text="A SavingsAccount object — earns 2% bonus interest on every deposit.",
        bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL, wraplength=380, justify="center"
    ).pack(pady=(0, 15))

    account = SavingsAccount(owner="Demo User", balance=1000)

    balance_label = tk.Label(
        win, text=f"Balance: ₹{account.balance:.2f}", bg=cfg.WHITE, fg=cfg.GREEN,
        font=cfg.FONT_H2
    )
    balance_label.pack(pady=10)

    amount_var = tk.StringVar()
    tk.Entry(win, textvariable=amount_var, font=cfg.FONT_BODY, justify="center").pack(
        padx=40, fill="x", ipady=8
    )

    log = tk.Listbox(win, font=cfg.FONT_SMALL, bd=0, highlightthickness=1, highlightbackground=cfg.BORDER)
    log.pack(fill="both", expand=True, padx=20, pady=15)

    def refresh():
        balance_label.configure(text=f"Balance: ₹{account.balance:.2f}")
        log.delete(0, tk.END)
        for entry in reversed(account.history):
            log.insert(tk.END, entry)

    def parse_amount():
        try:
            return float(amount_var.get())
        except ValueError:
            messagebox.showwarning("Invalid amount", "Enter a valid number.", parent=win)
            return None

    def do_deposit():
        amount = parse_amount()
        if amount is None:
            return
        try:
            account.deposit(amount)
            refresh()
        except ValueError as e:
            messagebox.showerror("Deposit failed", str(e), parent=win)

    def do_withdraw():
        amount = parse_amount()
        if amount is None:
            return
        try:
            account.withdraw(amount)
            refresh()
        except ValueError as e:
            messagebox.showerror("Withdrawal failed", str(e), parent=win)

    btn_row = tk.Frame(win, bg=cfg.WHITE)
    btn_row.pack(fill="x", padx=20, pady=(0, 20))

    make_button(btn_row, "⬆ Deposit", do_deposit, cfg.GREEN).pack(side="left", expand=True, fill="x", padx=2)
    make_button(btn_row, "⬇ Withdraw", do_withdraw, cfg.RED).pack(side="left", expand=True, fill="x", padx=2)

    refresh()


# ==========================================
# MODULE CONTENT
# ==========================================

MODULE = {
    "id": 5,
    "title": "Object-Oriented Programming",
    "description": "Model real-world things as classes and objects — the foundation of scalable Python code.",
    "topics": [
        {
            "id": 1,
            "title": "Introduction to OOP",
            "theory": "Object-Oriented Programming (OOP) organizes code around 'objects' — bundles of data (attributes) and behavior (methods) that model real-world things. Instead of separate variables and functions floating independently, related data and logic live together in one unit.\n\nOOP's four pillars are encapsulation, inheritance, polymorphism, and abstraction — all covered later in this module.",
            "key_points": [
                "OOP bundles data (attributes) with behavior (methods).",
                "A 'class' is a blueprint; an 'object' is a built instance.",
                "Four pillars: encapsulation, inheritance, polymorphism, abstraction.",
                "Helps model real-world entities: a Car, a Student, an Account.",
                "Makes large codebases easier to organize and reuse."
            ],
            "code_example": "# Without OOP — data and logic are disconnected\nname = \"Ana\"\ndef greet(name):\n    return f\"Hello, {name}\"\n\n# With OOP — bundled together (previewed, detailed next topic)\nclass Person:\n    def __init__(self, name):\n        self.name = name\n    def greet(self):\n        return f\"Hello, {self.name}\"",
        },
        {
            "id": 2,
            "title": "Classes",
            "theory": "A class is a blueprint for creating objects, defined with the `class` keyword. It describes what attributes and methods every object built from it will have — but the class itself isn't a usable object; it's the template.",
            "key_points": [
                "Defined with: class ClassName:",
                "By convention, class names use PascalCase (e.g. BankAccount).",
                "A class only becomes usable once you create objects from it.",
                "Holds method definitions shared by every object of that class.",
                "Classes can contain any number of methods and attributes."
            ],
            "code_example": "class Dog:\n    def bark(self):\n        print(\"Woof!\")\n\n# Dog is just the blueprint so far — no dog exists yet",
        },
        {
            "id": 3,
            "title": "Objects",
            "theory": "An object (or 'instance') is a concrete thing built from a class. Creating one is called instantiation, done by calling the class like a function: `my_dog = Dog()`. Each object has its own independent copy of the class's attributes.",
            "key_points": [
                "An object is a specific instance built from a class.",
                "Created (instantiated) by calling the class: obj = ClassName()",
                "Each object has its own independent attribute values.",
                "You can create as many objects from one class as needed.",
                "obj.method() calls a method belonging to that specific object."
            ],
            "code_example": "class Dog:\n    def bark(self):\n        print(\"Woof!\")\n\nmy_dog = Dog()      # an actual object now exists\nyour_dog = Dog()    # a second, separate object\nmy_dog.bark()",
        },
        {
            "id": 4,
            "title": "self",
            "theory": "`self` refers to the specific object a method is being called on — it's how a method accesses that object's own attributes. It's always the first parameter of an instance method, and Python passes it automatically; you don't supply it yourself when calling.",
            "key_points": [
                "self refers to 'this particular object' inside a method.",
                "Always the first parameter of an instance method.",
                "Passed automatically — obj.method() supplies self behind the scenes.",
                "self.attribute accesses/sets that object's own data.",
                "The name 'self' is convention, not a keyword — but always use it."
            ],
            "code_example": "class Dog:\n    def set_name(self, name):\n        self.name = name  # stores on THIS object\n\n    def bark(self):\n        print(f\"{self.name} says Woof!\")\n\nd = Dog()\nd.set_name(\"Rex\")\nd.bark()",
        },
        {
            "id": 5,
            "title": "Constructors",
            "theory": "The constructor is a special method, `__init__`, that runs automatically the moment an object is created. It's where you set up the object's initial attributes, usually from arguments passed in when instantiating.",
            "key_points": [
                "__init__(self, ...) runs automatically on object creation.",
                "Used to set up initial attribute values.",
                "Arguments to ClassName(...) are passed straight into __init__.",
                "Double underscores mark it as a special ('dunder') method.",
                "Every object gets its own __init__ call when created."
            ],
            "code_example": "class Dog:\n    def __init__(self, name, breed):\n        self.name = name\n        self.breed = breed\n\nrex = Dog(\"Rex\", \"Labrador\")\nprint(rex.name, rex.breed)",
        },
        {
            "id": 6,
            "title": "Instance Variables",
            "theory": "Instance variables belong to one specific object — set via `self.variable = value`, usually inside `__init__`. Two objects of the same class can have completely different instance variable values, since each object stores its own copy.",
            "key_points": [
                "Set with self.name = value, typically in __init__.",
                "Each object has its own independent copy.",
                "Changing one object's instance variable doesn't affect others.",
                "Accessed from outside as obj.variable_name.",
                "Most of an object's 'state' lives in instance variables."
            ],
            "code_example": "class Dog:\n    def __init__(self, name):\n        self.name = name  # instance variable\n\na = Dog(\"Rex\")\nb = Dog(\"Buddy\")\nprint(a.name, b.name)  # different per object",
        },
        {
            "id": 7,
            "title": "Class Variables",
            "theory": "A class variable is shared by every object of a class, defined directly inside the class body (not inside `__init__`). Changing it through the class affects all objects; changing it through one specific object usually just creates a new instance variable that shadows it for that object only.",
            "key_points": [
                "Defined directly in the class body, shared by all instances.",
                "Access via ClassName.variable or obj.variable.",
                "Good for constants or counters shared across all objects.",
                "Changing via the class updates it for every object.",
                "Changing via an instance usually creates a separate instance copy."
            ],
            "code_example": "class Dog:\n    species = \"Canis familiaris\"  # class variable\n\n    def __init__(self, name):\n        self.name = name  # instance variable\n\na = Dog(\"Rex\")\nb = Dog(\"Buddy\")\nprint(a.species, b.species)  # same for both",
        },
        {
            "id": 8,
            "title": "Methods",
            "theory": "A method is a function defined inside a class — it describes an action an object can perform, and always takes `self` as its first parameter. Methods can read and modify the object's own attributes, and can be called on any object built from that class.",
            "key_points": [
                "A method is a function defined inside a class.",
                "Always takes self as the first parameter.",
                "Called via obj.method(args) — self is passed automatically.",
                "Can read/modify the object's own attributes via self.",
                "Different objects run the same method independently."
            ],
            "code_example": "class Dog:\n    def __init__(self, name):\n        self.name = name\n        self.energy = 100\n\n    def play(self):\n        self.energy -= 10\n        print(f\"{self.name} played! Energy: {self.energy}\")\n\nrex = Dog(\"Rex\")\nrex.play()\nrex.play()",
        },
        {
            "id": 9,
            "title": "Encapsulation",
            "theory": "Encapsulation means keeping an object's internal data protected and controlling access to it through methods, rather than letting outside code change it directly. Python signals 'internal use only' by convention with a leading underscore (`_balance`), or stronger privacy with a double underscore (`__balance`).\n\nThis prevents invalid states — e.g. a bank balance going negative because something bypassed the withdrawal rules.",
            "key_points": [
                "Hides internal data, exposes controlled access via methods.",
                "_name = 'protected by convention' (single underscore).",
                "__name = name-mangled, stronger privacy (double underscore).",
                "Prevents invalid states by validating inside methods.",
                "@property lets you expose a controlled 'read-only' attribute."
            ],
            "code_example": "class Account:\n    def __init__(self, balance):\n        self._balance = balance  # protected\n\n    def withdraw(self, amount):\n        if amount > self._balance:\n            raise ValueError(\"Insufficient funds\")\n        self._balance -= amount\n\n    @property\n    def balance(self):\n        return self._balance",
        },
        {
            "id": 10,
            "title": "Inheritance",
            "theory": "Inheritance lets a new class (the 'child' or 'subclass') reuse and extend the attributes/methods of an existing class (the 'parent' or 'superclass'). This avoids rewriting shared logic — the child gets everything the parent has, plus whatever new behavior it adds.\n\n`super().__init__(...)` calls the parent's constructor from inside the child's.",
            "key_points": [
                "class Child(Parent): inherits everything from Parent.",
                "super().method() calls the parent class's version.",
                "Avoids duplicating shared logic across related classes.",
                "A child can add new methods/attributes the parent lacks.",
                "A child can override a parent's method (see Polymorphism)."
            ],
            "code_example": "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        print(f\"{self.name} makes a sound.\")\n\nclass Dog(Animal):        # Dog inherits from Animal\n    def speak(self):\n        print(f\"{self.name} barks!\")\n\nDog(\"Rex\").speak()",
        },
        {
            "id": 11,
            "title": "Polymorphism",
            "theory": "Polymorphism ('many forms') means different classes can implement the same method name in their own way, and calling it produces behavior appropriate to each object's actual class — without the calling code needing to know which subclass it's dealing with.",
            "key_points": [
                "Same method name, different behavior per class.",
                "A child class overriding a parent's method is polymorphism.",
                "Calling code just does obj.method() — behavior varies by type.",
                "Makes code flexible: one loop can handle many related types.",
                "The Mini App above shows this: SavingsAccount overrides deposit()."
            ],
            "code_example": "class Cat(Animal):\n    def speak(self):\n        print(f\"{self.name} meows!\")\n\nanimals = [Dog(\"Rex\"), Cat(\"Whiskers\")]\nfor a in animals:\n    a.speak()  # each calls its own version of speak()",
        },
        {
            "id": 12,
            "title": "Abstraction",
            "theory": "Abstraction means exposing only what's necessary to use an object, while hiding the complex implementation details behind simple method calls. When you call `account.withdraw(50)`, you don't need to know how the balance check or storage works internally — just that it does.\n\nPython's `abc` module can enforce this formally with abstract base classes, requiring subclasses to implement certain methods.",
            "key_points": [
                "Hides complexity behind a simple interface (method calls).",
                "The user of a class doesn't need its internal details.",
                "abc.ABC + @abstractmethod enforce it formally, if needed.",
                "Every method call so far has been abstraction in action.",
                "Good abstraction makes code easier to use correctly."
            ],
            "code_example": "from abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass  # subclasses MUST implement this\n\nclass Circle(Shape):\n    def __init__(self, r):\n        self.r = r\n    def area(self):\n        return 3.1416 * self.r ** 2\n\nprint(Circle(4).area())",
        },
        {
            "id": 13,
            "title": "Practice Project",
            "theory": "Build a 'Vehicle Fleet' system:\n\n1. Create a base class Vehicle with __init__(self, make, model) and a method info().\n2. Create Car and Motorbike subclasses that inherit from Vehicle and override info() to add their own detail (polymorphism).\n3. Encapsulate an odometer as a protected _mileage attribute, only changeable through a drive(km) method that rejects negative values.\n4. Store several vehicles in a list and loop through calling info() on each.\n\nThis exercises every OOP pillar covered in this module.",
            "key_points": [
                "Combines classes, inheritance, polymorphism, and encapsulation.",
                "A base class + subclasses model a real 'family' of related things.",
                "Encapsulation protects _mileage from invalid direct changes.",
                "One loop, many object types — that's polymorphism in practice.",
                "Try the Bank Account Mini App above for a similar working example."
            ],
            "code_example": "class Vehicle:\n    def __init__(self, make, model):\n        self.make = make\n        self.model = model\n        self._mileage = 0\n\n    def drive(self, km):\n        if km < 0:\n            raise ValueError(\"km can't be negative\")\n        self._mileage += km\n\n    def info(self):\n        return f\"{self.make} {self.model} — {self._mileage} km\"\n\nclass Car(Vehicle):\n    def info(self):\n        return super().info() + \" (Car)\"\n\nfleet = [Car(\"Toyota\", \"Corolla\")]\nfor v in fleet:\n    v.drive(120)\n    print(v.info())",
        },
    ],
    "quiz": [
        {"question": "What is a class?", "options": ["A built object", "A blueprint for creating objects", "A loop type", "A built-in function"], "answer_index": 1},
        {"question": "How do you create an object from a class?", "options": ["ClassName.new()", "ClassName()", "new ClassName", "object(ClassName)"], "answer_index": 1},
        {"question": "What does 'self' refer to?", "options": ["The class itself", "The specific object the method is called on", "A global variable", "The parent class"], "answer_index": 1},
        {"question": "Which method runs automatically when an object is created?", "options": ["__main__", "__init__", "__self__", "__new__"], "answer_index": 1},
        {"question": "What is a class variable shared by?", "options": ["Only one object", "All objects of that class", "No objects", "Only the parent class"], "answer_index": 1},
        {"question": "What does encapsulation help prevent?", "options": ["Slow code", "Invalid/uncontrolled state changes", "Long variable names", "Extra imports"], "answer_index": 1},
        {"question": "What does 'class Dog(Animal):' mean?", "options": ["Dog replaces Animal", "Dog inherits from Animal", "Animal inherits from Dog", "They are unrelated"], "answer_index": 1},
        {"question": "What best describes polymorphism?", "options": ["One class, one method", "Same method name behaving differently per class", "Hiding all data", "Deleting unused code"], "answer_index": 1},
        {"question": "What does abstraction do?", "options": ["Deletes code", "Hides complexity behind a simple interface", "Speeds up loops", "Removes all comments"], "answer_index": 1},
        {"question": "What does super().__init__() do?", "options": ["Creates a new class", "Calls the parent class's constructor", "Deletes the parent class", "Restarts the program"], "answer_index": 1},
    ],
    "mini_app": {
        "title": "Bank Account Simulator",
        "description": "A SavingsAccount object demonstrating classes, encapsulation, inheritance, and polymorphism live.",
        "launch": launch_mini_app,
    },
}
