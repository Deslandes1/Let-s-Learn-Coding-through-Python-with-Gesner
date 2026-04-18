import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- Audio setup with edge-tts -----
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

def run_async_with_timeout(coro, timeout=30):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(asyncio.wait_for(coro, timeout=timeout))
    finally:
        loop.close()

async def save_speech(text, file_path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)

def generate_audio(text, output_path, voice):
    if not EDGE_TTS_AVAILABLE:
        raise Exception("edge-tts not installed")
    run_async_with_timeout(save_speech(text, output_path, voice))

VOICE = "en-US-GuyNeural"

st.set_page_config(page_title="Let's Learn Coding through Python with Gesner", layout="wide")

# ========== STYLING (code in black on light background) ==========
def set_coding_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
        .main-header { background: linear-gradient(135deg, #f7971e, #ffd200); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: white !important; }
        /* Code blocks: black text on light background */
        .stCodeBlock, .stCodeBlock pre, pre, code, .stCode {
            background-color: #f4f4f4 !important;
            color: #000000 !important;
            border-radius: 10px;
            padding: 0.2rem 0.4rem;
            font-family: monospace;
        }
        .stCodeBlock pre, pre {
            padding: 1rem;
            overflow-x: auto;
        }
        .stCodeBlock code, pre code {
            color: #000000 !important;
            background-color: transparent !important;
        }
        .stText code {
            background-color: #f4f4f4 !important;
            color: #000000 !important;
            padding: 0.2rem 0.4rem;
            border-radius: 6px;
        }
        .stTabs [role="tab"] { color: white !important; background: rgba(255,210,0,0.2); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: #ffd200; color: black !important; }
        .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: white !important; }
        .stButton button { background-color: #f7971e; color: white; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #ffd200; color: black; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #0f2027, #203a43); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #203a43; border: 1px solid #ffd200; border-radius: 10px; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox svg { fill: white; }
        div[data-baseweb="popover"] ul { background-color: #203a43; border: 1px solid #ffd200; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #203a43; }
        div[data-baseweb="popover"] li:hover { background-color: #f7971e; }
        </style>
    """, unsafe_allow_html=True)

def show_python_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffd200" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#306998"/>
                    <stop offset="100%" stop-color="#ffd200"/>
                </linearGradient></defs>
                <text x="50" y="70" font-size="50" text-anchor="middle" fill="white" font-weight="bold">🐍</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ========== AUTHENTICATION ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_coding_style()
    st.title("🔐 Access Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_python_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn Coding through Python with Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #ffd200;'>20 lessons – from beginner to advanced. Build like Silicon Valley.</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

set_coding_style()
st.markdown("""
<div class="main-header">
    <h1>🐍 Let's Learn Coding through Python with Gesner</h1>
    <p>20 interactive lessons | Basic to advanced | Audio support | Coding practice</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    show_python_logo()
    st.markdown("## 🎯 Select a lesson")
    lesson_number = st.selectbox("Lesson", list(range(1, 21)), index=0)
    st.markdown("---")
    st.markdown("### 📚 Your progress")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ Lesson {lesson_number} of 20 completed")
    st.markdown("---")
    st.markdown("**Founder & Developer:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown("**$299 USD** (full book – 20 lessons, source code, certificate)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ========== LESSON DATA ==========
topics = [
    "Hello, World! – Your First Python Program",
    "Variables and Data Types",
    "Basic Input and Output",
    "Conditional Statements (if, elif, else)",
    "Loops (for and while)",
    "Lists and List Operations",
    "Tuples and Dictionaries",
    "Functions – Defining and Calling",
    "Function Arguments and Return Values",
    "String Manipulation",
    "File Handling – Reading and Writing Files",
    "Exception Handling (try, except)",
    "Modules and Packages",
    "List Comprehensions and Lambda Functions",
    "Object-Oriented Programming – Classes and Objects",
    "Inheritance and Polymorphism",
    "Working with Dates and Times",
    "Introduction to NumPy",
    "Basic Data Visualization with Matplotlib",
    "Final Project – Build a Mini Calculator App"
]

explanations = [
    "**Lesson 1: Hello, World!**\nPython is a powerful, easy-to-learn programming language. The first program everyone writes is 'Hello, World!' which prints that text to the screen.\nUse the `print()` function to output text. Strings are written inside quotes.",
    "**Lesson 2: Variables and Data Types**\nVariables store data. Python has several data types: integers (whole numbers), floats (decimals), strings (text), and booleans (True/False). You don't need to declare the type; Python infers it.",
    "**Lesson 3: Basic Input and Output**\nUse `input()` to get user input (always returns a string). Use `print()` to display output. Convert input to numbers using `int()` or `float()`.",
    "**Lesson 4: Conditional Statements**\n`if`, `elif`, `else` allow your program to make decisions based on conditions. Conditions use comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`.",
    "**Lesson 5: Loops**\n`for` loops iterate over a sequence (like a list or range). `while` loops repeat as long as a condition is true. Use `break` to exit early, `continue` to skip.",
    "**Lesson 6: Lists**\nLists store multiple items in a single variable. They are ordered, changeable, and allow duplicates. Access items by index (starting at 0). Methods: `append()`, `remove()`, `sort()`.",
    "**Lesson 7: Tuples and Dictionaries**\nTuples are immutable lists (cannot be changed). Dictionaries store key-value pairs, great for structured data. Access values using keys.",
    "**Lesson 8: Functions**\nFunctions group code that performs a specific task. Define with `def`, give it a name, and call it later. They help avoid repetition.",
    "**Lesson 9: Function Arguments**\nFunctions can take arguments (inputs) and return values. Default arguments, keyword arguments, and variable-length arguments (`*args`, `**kwargs`) give flexibility.",
    "**Lesson 10: String Manipulation**\nStrings have many methods: `upper()`, `lower()`, `strip()`, `replace()`, `split()`, `join()`. Slicing extracts parts: `[start:end:step]`.",
    "**Lesson 11: File Handling**\nOpen files using `open()` in read (`'r'`), write (`'w'`), or append (`'a'`) mode. Always close files or use `with` statement for automatic closing.",
    "**Lesson 12: Exception Handling**\nUse `try` and `except` to catch errors gracefully. You can also use `else` (if no error) and `finally` (always runs). Prevents crashes.",
    "**Lesson 13: Modules and Packages**\nModules are Python files containing functions and variables. Import them with `import`. The standard library has many modules (math, random, datetime). You can create your own.",
    "**Lesson 14: List Comprehensions**\nA concise way to create lists. Syntax: `[expression for item in iterable if condition]`. Lambda functions are small anonymous functions: `lambda x: x*2`.",
    "**Lesson 15: Object-Oriented Programming**\nClasses are blueprints for objects. Define a class with `class`, then create instances. Attributes are variables inside a class, methods are functions.",
    "**Lesson 16: Inheritance**\nA class can inherit attributes and methods from another class. Use `class Child(Parent):`. Override methods, use `super()` to call parent methods.",
    "**Lesson 17: Dates and Times**\nThe `datetime` module provides classes for manipulating dates and times. Get current date/time, format strings, calculate differences.",
    "**Lesson 18: NumPy Basics**\nNumPy is a library for numerical computing. It provides arrays (ndarray) that are faster than lists and support vectorized operations.",
    "**Lesson 19: Matplotlib Basics**\nMatplotlib is a plotting library. Create line plots, bar charts, scatter plots, and customize with labels, titles, colors.",
    "**Lesson 20: Final Project – Mini Calculator**\nApply everything you've learned to build a calculator that can add, subtract, multiply, divide, and handle errors. This project showcases your skills."
]

demo_codes = [
    "print('Hello, World!')",
    "name = 'Gesner'\nage = 35\nheight = 5.9\nis_student = True\nprint(name, age, height, is_student)",
    "user_name = input('Enter your name: ')\nprint('Hello,', user_name)\nage = int(input('Enter your age: '))\nprint('Next year you will be', age+1)",
    "score = 85\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelse:\n    print('C')",
    "for i in range(5):\n    print('Number:', i)\ncount = 0\nwhile count < 3:\n    print('While loop', count)\n    count += 1",
    "fruits = ['apple', 'banana', 'cherry']\nfruits.append('orange')\nprint(fruits)\nprint(fruits[1])",
    "person = {'name': 'Alice', 'age': 30}\nprint(person['name'])\ntuple_ex = (1, 2, 3)\nprint(tuple_ex[0])",
    "def greet():\n    print('Hello!')\ngreet()",
    "def add(a, b):\n    return a + b\nresult = add(5, 3)\nprint(result)",
    "text = '  Python Programming  '\nprint(text.strip())\nprint(text.upper())\nprint(text.replace('P', 'J'))",
    "with open('sample.txt', 'w') as f:\n    f.write('Hello file!')\nwith open('sample.txt', 'r') as f:\n    content = f.read()\n    print(content)",
    "try:\n    num = int(input('Enter a number: '))\n    print(10/num)\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')\nexcept ValueError:\n    print('Invalid input')",
    "import math\nprint(math.sqrt(16))\nprint(math.pi)\nimport random\nprint(random.randint(1,10))",
    "squares = [x**2 for x in range(10) if x % 2 == 0]\nprint(squares)\ndouble = lambda x: x*2\nprint(double(5))",
    "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return 'Woof!'\nmy_dog = Dog('Rex')\nprint(my_dog.name, my_dog.bark())",
    "class Animal:\n    def speak(self):\n        return 'Sound'\nclass Cat(Animal):\n    def speak(self):\n        return 'Meow'\ncat = Cat()\nprint(cat.speak())",
    "from datetime import datetime, timedelta\nnow = datetime.now()\nprint('Now:', now)\ntomorrow = now + timedelta(days=1)\nprint('Tomorrow:', tomorrow)",
    "import numpy as np\narr = np.array([1, 2, 3, 4])\nprint(arr * 2)\nprint(np.mean(arr))",
    "import matplotlib.pyplot as plt\nx = [1, 2, 3, 4]\ny = [10, 20, 25, 30]\nplt.plot(x, y)\nplt.title('Sample Plot')\nplt.show()",
    "# Mini Calculator Project\n# See practice exercises for full code"
]

def get_practice_exercises(lesson_num):
    # Full exercises for all 20 lessons (same as previous correct version)
    exercises = {
        1: [
            {"desc": "Print 'Welcome to Python'", "solution": "print('Welcome to Python')"},
            {"desc": "Print your name and age using two print statements", "solution": "print('Name: Gesner')\nprint('Age: 35')"},
            {"desc": "Print the result of 5 + 3", "solution": "print(5 + 3)"},
            {"desc": "Print 'Python' five times using a loop", "solution": "for i in range(5):\n    print('Python')"},
            {"desc": "Print a sentence that contains a newline (\\n) and a tab (\\t)", "solution": "print('Line1\\n\\tIndented line')"}
        ],
        2: [
            {"desc": "Create a variable 'city' with your city name and print it", "solution": "city = 'Port-au-Prince'\nprint(city)"},
            {"desc": "Create two variables 'a' and 'b' with numbers, then print their sum", "solution": "a = 10\nb = 20\nprint(a + b)"},
            {"desc": "Create a float variable 'pi' with value 3.1416 and print it", "solution": "pi = 3.1416\nprint(pi)"},
            {"desc": "Create a boolean variable 'is_sunny' and set to False, then print", "solution": "is_sunny = False\nprint(is_sunny)"},
            {"desc": "Swap two variables x=5 and y=10 without using a temporary variable", "solution": "x, y = 5, 10\nx, y = y, x\nprint(x, y)"}
        ],
        3: [
            {"desc": "Ask user for their favorite color and print 'Your favorite color is X'", "solution": "color = input('Enter favorite color: ')\nprint('Your favorite color is', color)"},
            {"desc": "Ask for two numbers and print their product", "solution": "a = int(input('First: '))\nb = int(input('Second: '))\nprint(a * b)"},
            {"desc": "Ask for a number and print its square", "solution": "num = float(input('Number: '))\nprint(num ** 2)"},
            {"desc": "Ask for a sentence and print it in uppercase", "solution": "text = input('Sentence: ')\nprint(text.upper())"},
            {"desc": "Ask for a floating-point number and print its integer part", "solution": "num = float(input('Float: '))\nprint(int(num))"}
        ],
        4: [
            {"desc": "Check if a number is positive or negative", "solution": "num = int(input('Enter number: '))\nif num > 0:\n    print('Positive')\nelif num < 0:\n    print('Negative')\nelse:\n    print('Zero')"},
            {"desc": "Check if a year is a leap year", "solution": "year = int(input('Year: '))\nif (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):\n    print('Leap year')\nelse:\n    print('Not leap year')"},
            {"desc": "Check if a number is even or odd", "solution": "num = int(input('Number: '))\nif num % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')"},
            {"desc": "Compare two numbers and print the larger one", "solution": "a = int(input('First: '))\nb = int(input('Second: '))\nif a > b:\n    print(a)\nelse:\n    print(b)"},
            {"desc": "Ask for age and print 'Adult' if >=18 else 'Minor'", "solution": "age = int(input('Age: '))\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')"}
        ],
        5: [
            {"desc": "Print numbers from 1 to 10 using a for loop", "solution": "for i in range(1, 11):\n    print(i)"},
            {"desc": "Print even numbers between 1 and 20", "solution": "for i in range(2, 21, 2):\n    print(i)"},
            {"desc": "Use a while loop to print 'Hello' 5 times", "solution": "count = 0\nwhile count < 5:\n    print('Hello')\n    count += 1"},
            {"desc": "Sum all numbers from 1 to 100 using a loop", "solution": "total = 0\nfor i in range(1, 101):\n    total += i\nprint(total)"},
            {"desc": "Print the multiplication table of a given number (1 to 10)", "solution": "num = int(input('Number: '))\nfor i in range(1, 11):\n    print(f'{num} x {i} = {num*i}')"}
        ],
        6: [
            {"desc": "Create a list of three favorite movies and print the second one", "solution": "movies = ['Inception', 'Matrix', 'Avatar']\nprint(movies[1])"},
            {"desc": "Add a new item to the list and print the entire list", "solution": "fruits = ['apple', 'banana']\nfruits.append('orange')\nprint(fruits)"},
            {"desc": "Remove an item from the list by value", "solution": "colors = ['red', 'blue', 'green']\ncolors.remove('blue')\nprint(colors)"},
            {"desc": "Sort a list of numbers in ascending order", "solution": "nums = [5, 2, 8, 1]\nnums.sort()\nprint(nums)"},
            {"desc": "Find the length of a list", "solution": "items = [1, 2, 3, 4, 5]\nprint(len(items))"}
        ],
        7: [
            {"desc": "Create a tuple with numbers 10, 20, 30 and print the first element", "solution": "tup = (10, 20, 30)\nprint(tup[0])"},
            {"desc": "Create a dictionary with keys 'name', 'age' and print the name", "solution": "person = {'name': 'Maria', 'age': 25}\nprint(person['name'])"},
            {"desc": "Add a new key-value pair to an existing dictionary", "solution": "person = {'name': 'John'}\nperson['city'] = 'New York'\nprint(person)"},
            {"desc": "Check if a key exists in a dictionary", "solution": "d = {'a': 1, 'b': 2}\nif 'a' in d:\n    print('Exists')"},
            {"desc": "Convert a list into a tuple", "solution": "my_list = [1, 2, 3]\nmy_tuple = tuple(my_list)\nprint(my_tuple)"}
        ],
        8: [
            {"desc": "Define a function that prints 'Hello Function'", "solution": "def say_hello():\n    print('Hello Function')\nsay_hello()"},
            {"desc": "Create a function that takes a name and prints 'Hello, [name]'", "solution": "def greet(name):\n    print(f'Hello, {name}')\ngreet('Anna')"},
            {"desc": "Write a function that returns the square of a number", "solution": "def square(x):\n    return x * x\nprint(square(4))"},
            {"desc": "Create a function with no arguments that returns the string 'Python'", "solution": "def get_lang():\n    return 'Python'\nprint(get_lang())"},
            {"desc": "Call a function inside another function", "solution": "def add(a, b):\n    return a + b\ndef calculate():\n    return add(3, 4)\nprint(calculate())"}
        ],
        9: [
            {"desc": "Define a function with two arguments that returns their product", "solution": "def multiply(a, b):\n    return a * b\nprint(multiply(4, 5))"},
            {"desc": "Use a default argument: function greet(name='Guest')", "solution": "def greet(name='Guest'):\n    return f'Hello {name}'\nprint(greet())\nprint(greet('Gesner'))"},
            {"desc": "Write a function that accepts any number of arguments using *args", "solution": "def sum_all(*args):\n    return sum(args)\nprint(sum_all(1, 2, 3, 4))"},
            {"desc": "Use keyword arguments **kwargs to print a dictionary", "solution": "def print_info(**kwargs):\n    for key, value in kwargs.items():\n        print(f'{key}: {value}')\nprint_info(name='Gesner', age=35)"},
            {"desc": "Return multiple values from a function", "solution": "def get_stats(a, b):\n    return a+b, a-b\nsum_val, diff = get_stats(10, 3)\nprint(sum_val, diff)"}
        ],
        10: [
            {"desc": "Convert a string to uppercase", "solution": "text = 'python'\nprint(text.upper())"},
            {"desc": "Remove whitespace from the beginning and end of a string", "solution": "text = '  hello  '\nprint(text.strip())"},
            {"desc": "Replace 'cat' with 'dog' in a sentence", "solution": "sentence = 'I like cats'\nprint(sentence.replace('cat', 'dog'))"},
            {"desc": "Split a sentence into words", "solution": "sentence = 'Hello world from Python'\nwords = sentence.split()\nprint(words)"},
            {"desc": "Join a list of words with a space", "solution": "words = ['Join', 'these', 'words']\nprint(' '.join(words))"}
        ],
        11: [
            {"desc": "Write 'Hello' to a file named 'test.txt'", "solution": "with open('test.txt', 'w') as f:\n    f.write('Hello')"},
            {"desc": "Read the content of 'test.txt' and print it", "solution": "with open('test.txt', 'r') as f:\n    content = f.read()\n    print(content)"},
            {"desc": "Append ' World' to the same file", "solution": "with open('test.txt', 'a') as f:\n    f.write(' World')"},
            {"desc": "Count the number of lines in a file", "solution": "with open('test.txt', 'r') as f:\n    lines = f.readlines()\n    print(len(lines))"},
            {"desc": "Write a list of strings to a file, each on a new line", "solution": "lines = ['line1', 'line2', 'line3']\nwith open('output.txt', 'w') as f:\n    for line in lines:\n        f.write(line + '\\n')"}
        ],
        12: [
            {"desc": "Use try-except to handle division by zero", "solution": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')"},
            {"desc": "Catch a ValueError when converting non-numeric string to int", "solution": "try:\n    num = int('abc')\nexcept ValueError:\n    print('Invalid number')"},
            {"desc": "Use else clause when no exception occurs", "solution": "try:\n    num = int('5')\nexcept ValueError:\n    print('Error')\nelse:\n    print('Success:', num)"},
            {"desc": "Use finally to always print 'Done'", "solution": "try:\n    x = 1 / 1\nexcept:\n    print('Error')\nfinally:\n    print('Done')"},
            {"desc": "Raise a custom exception if a number is negative", "solution": "def check_positive(n):\n    if n < 0:\n        raise ValueError('Negative number')\n    return n\ntry:\n    check_positive(-5)\nexcept ValueError as e:\n    print(e)"}
        ],
        13: [
            {"desc": "Import the math module and print pi", "solution": "import math\nprint(math.pi)"},
            {"desc": "Use random.randint to generate a random number between 1 and 100", "solution": "import random\nprint(random.randint(1, 100))"},
            {"desc": "Import only the sqrt function from math", "solution": "from math import sqrt\nprint(sqrt(16))"},
            {"desc": "Create your own module (write a simple function in a separate file) - describe the steps", "solution": "# Save as mymodule.py with:\n# def hello(): print('Hello')\n# Then in main: import mymodule\n# mymodule.hello()"},
            {"desc": "Use the datetime module to print today's date", "solution": "from datetime import date\nprint(date.today())"}
        ],
        14: [
            {"desc": "Create a list of squares for numbers 1 to 5 using list comprehension", "solution": "squares = [x**2 for x in range(1, 6)]\nprint(squares)"},
            {"desc": "Use list comprehension to filter even numbers from 1 to 10", "solution": "evens = [x for x in range(1, 11) if x % 2 == 0]\nprint(evens)"},
            {"desc": "Write a lambda function that doubles a number", "solution": "double = lambda x: x * 2\nprint(double(5))"},
            {"desc": "Use map with lambda to double all numbers in a list", "solution": "nums = [1, 2, 3]\ndoubled = list(map(lambda x: x*2, nums))\nprint(doubled)"},
            {"desc": "Use filter with lambda to get numbers greater than 3", "solution": "nums = [1, 4, 2, 5, 3]\nfiltered = list(filter(lambda x: x > 3, nums))\nprint(filtered)"}
        ],
        15: [
            {"desc": "Define a class 'Car' with attributes brand and model, and a method 'info' that prints them", "solution": "class Car:\n    def __init__(self, brand, model):\n        self.brand = brand\n        self.model = model\n    def info(self):\n        print(f'{self.brand} {self.model}')\nmy_car = Car('Toyota', 'Corolla')\nmy_car.info()"},
            {"desc": "Create an instance of the Car class and call its method", "solution": "class Car:\n    def __init__(self, brand):\n        self.brand = brand\n    def honk(self):\n        print('Beep!')\nc = Car('Honda')\nc.honk()"},
            {"desc": "Add a class variable 'wheels' set to 4 and access it", "solution": "class Vehicle:\n    wheels = 4\nprint(Vehicle.wheels)"},
            {"desc": "Use __str__ method to return a readable string for the class", "solution": "class Person:\n    def __init__(self, name):\n        self.name = name\n    def __str__(self):\n        return f'Person: {self.name}'\np = Person('Gesner')\nprint(p)"},
            {"desc": "Create a method that modifies an attribute", "solution": "class BankAccount:\n    def __init__(self, balance):\n        self.balance = balance\n    def deposit(self, amount):\n        self.balance += amount\nacc = BankAccount(100)\nacc.deposit(50)\nprint(acc.balance)"}
        ],
        16: [
            {"desc": "Create a parent class Animal with method speak, and child class Dog that overrides speak", "solution": "class Animal:\n    def speak(self):\n        return 'Sound'\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof'\nd = Dog()\nprint(d.speak())"},
            {"desc": "Use super() to call parent method from child", "solution": "class Parent:\n    def greet(self):\n        return 'Hello from Parent'\nclass Child(Parent):\n    def greet(self):\n        return super().greet() + ' and Child'\nc = Child()\nprint(c.greet())"},
            {"desc": "Create a class with inheritance and add a new method in child", "solution": "class Vehicle:\n    def start(self):\n        return 'Starting'\nclass Bike(Vehicle):\n    def ring_bell(self):\n        return 'Ring ring'\nb = Bike()\nprint(b.start(), b.ring_bell())"},
            {"desc": "Multiple inheritance: create class C that inherits from A and B", "solution": "class A:\n    def a(self):\n        return 'A'\nclass B:\n    def b(self):\n        return 'B'\nclass C(A, B):\n    pass\nc = C()\nprint(c.a(), c.b())"},
            {"desc": "Check if an object is an instance of a class", "solution": "class X:\n    pass\nobj = X()\nprint(isinstance(obj, X))"}
        ],
        17: [
            {"desc": "Print the current date and time", "solution": "from datetime import datetime\nnow = datetime.now()\nprint(now)"},
            {"desc": "Print only the current year", "solution": "from datetime import datetime\nprint(datetime.now().year)"},
            {"desc": "Create a date object for your birthday", "solution": "from datetime import date\nbday = date(1990, 5, 15)\nprint(bday)"},
            {"desc": "Calculate the difference between two dates", "solution": "from datetime import date\nd1 = date(2025, 1, 1)\nd2 = date(2025, 12, 31)\ndelta = d2 - d1\nprint(delta.days)"},
            {"desc": "Format a date as 'Month Day, Year'", "solution": "from datetime import datetime\nnow = datetime.now()\nprint(now.strftime('%B %d, %Y'))"}
        ],
        18: [
            {"desc": "Create a NumPy array from a list", "solution": "import numpy as np\narr = np.array([1, 2, 3])\nprint(arr)"},
            {"desc": "Create a 2D NumPy array (matrix)", "solution": "import numpy as np\nmatrix = np.array([[1, 2], [3, 4]])\nprint(matrix)"},
            {"desc": "Multiply all elements of a NumPy array by 2", "solution": "import numpy as np\narr = np.array([1, 2, 3])\nprint(arr * 2)"},
            {"desc": "Compute the mean of a NumPy array", "solution": "import numpy as np\narr = np.array([10, 20, 30])\nprint(np.mean(arr))"},
            {"desc": "Create an array of zeros with shape (3,4)", "solution": "import numpy as np\nzeros = np.zeros((3, 4))\nprint(zeros)"}
        ],
        19: [
            {"desc": "Plot a simple line graph with x = [1,2,3] and y = [2,4,6]", "solution": "import matplotlib.pyplot as plt\nx = [1,2,3]\ny = [2,4,6]\nplt.plot(x, y)\nplt.show()"},
            {"desc": "Add title and labels to a plot", "solution": "import matplotlib.pyplot as plt\nplt.plot([1,2,3], [1,4,9])\nplt.title('Squares')\nplt.xlabel('x')\nplt.ylabel('y')\nplt.show()"},
            {"desc": "Create a bar chart", "solution": "import matplotlib.pyplot as plt\ncategories = ['A', 'B', 'C']\nvalues = [10, 20, 15]\nplt.bar(categories, values)\nplt.show()"},
            {"desc": "Create a scatter plot", "solution": "import matplotlib.pyplot as plt\nx = [1,2,3,4]\ny = [2,3,5,7]\nplt.scatter(x, y)\nplt.show()"},
            {"desc": "Save a plot as an image file", "solution": "import matplotlib.pyplot as plt\nplt.plot([1,2,3], [1,4,9])\nplt.savefig('plot.png')"}
        ],
        20: [
            {"desc": "Build a calculator function that adds two numbers", "solution": "def add(a, b): return a + b"},
            {"desc": "Build a calculator function that subtracts two numbers", "solution": "def subtract(a, b): return a - b"},
            {"desc": "Build a calculator function that multiplies two numbers", "solution": "def multiply(a, b): return a * b"},
            {"desc": "Build a calculator function that divides two numbers, handling division by zero", "solution": "def divide(a, b):\n    if b == 0:\n        return 'Error: division by zero'\n    return a / b"},
            {"desc": "Create a menu-driven calculator that asks user for operation and numbers", "solution": "def calculator():\n    print('1. Add\\n2. Subtract\\n3. Multiply\\n4. Divide')\n    choice = input('Choose operation: ')\n    a = float(input('First number: '))\n    b = float(input('Second number: '))\n    if choice == '1':\n        print(a + b)\n    elif choice == '2':\n        print(a - b)\n    elif choice == '3':\n        print(a * b)\n    elif choice == '4':\n        if b != 0:\n            print(a / b)\n        else:\n            print('Cannot divide by zero')\n    else:\n        print('Invalid choice')\ncalculator()"}
        ]
    }
    return exercises.get(lesson_num, exercises[1])  # fallback to lesson 1 if not found

def build_lesson(num):
    return {
        "title": topics[num-1],
        "explanation": explanations[num-1],
        "demo_code": demo_codes[num-1],
        "exercises": get_practice_exercises(num)
    }

lessons = {i: build_lesson(i) for i in range(1, 21)}

# ========== AUDIO FUNCTION ==========
def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Audio disabled. Please install edge-tts.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                generate_audio(text, tmp.name, VOICE)
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Audio error: {e}")
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ========== DISPLAY LESSON ==========
lesson = lessons[lesson_number]
st.markdown(f"## 📖 Lesson {lesson_number}: {lesson['title']}")

tab1, tab2, tab3 = st.tabs(["📘 Explanation & Demo", "💻 Practice Exercises", "📝 Notes"])

# ----- TAB 1: Explanation and Demo -----
with tab1:
    st.markdown(lesson['explanation'])
    play_audio(lesson['explanation'], f"exp_{lesson_number}")
    st.markdown("---")
    st.subheader("🎬 Demo Code")
    st.code(lesson['demo_code'], language="python")
    # Audio for demo code description
    demo_audio_text = f"Demo code for {lesson['title']}: {lesson['demo_code']}"
    play_audio(demo_audio_text, f"demo_audio_{lesson_number}")
    st.info("Copy this code and run it in your Python environment to see the output. You can also use online playgrounds like replit.com.")
    st.caption("💡 Tip: Modify the code to experiment and deepen your understanding.")

# ----- TAB 2: Practice Exercises (audio for each exercise) -----
with tab2:
    st.markdown("### 🧠 Try these 5 exercises")
    st.caption("Write your code in a Python environment. Click 'Show Solution' to see the answer.")
    for i, ex in enumerate(lesson['exercises'], 1):
        st.markdown(f"**Exercise {i}:** {ex['desc']}")
        play_audio(ex['desc'], f"ex_desc_{lesson_number}_{i}")
        if st.button(f"Show Solution {i}", key=f"sol_{lesson_number}_{i}"):
            st.code(ex['solution'], language="python")
        st.markdown("---")

# ----- TAB 3: Notes (with audio) -----
with tab3:
    notes_text = f"""
    Lesson focus: {lesson['title']}
    Key concepts covered: {lesson['explanation'].split('**')[1] if '**' in lesson['explanation'] else lesson['explanation'][:100]}
    Next steps: Practice the exercises and modify the demo code to experiment.
    Remember: Coding is learned by doing. Write code every day!
    """
    st.markdown("### 📝 Study Notes")
    st.markdown(notes_text)
    play_audio(notes_text, f"notes_audio_{lesson_number}")

# ========== END OF BOOK ==========
if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 Congratulations! You have completed the Python Coding Course.")
    st.markdown("""
    ### 📞 To continue with advanced projects or get support:
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Keep coding, keep building. You are now ready to create real-world Python applications!
    """)
