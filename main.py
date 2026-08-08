import asyncio

import flet as ft

# --- Quiz Content (data-driven: edit this dict to add/change questions) ---
# Each topic has 50 questions. The majority are "real code" questions
# (predict the output / find the bug / what does this do), with a smaller
# set of pure concept questions mixed in.
QUIZ_DATA = {
    "Python Fundamentals and Setup": [
        ("What is Python?", "Python is a high-level, interpreted, general-purpose programming language known for its readability."),
        ("Who created Python?", "Guido van Rossum, first released in 1991."),
        ("Is Python interpreted or compiled?", "Python is primarily interpreted, though CPython first compiles source code to bytecode."),
        ("What is pip?", "pip is Python's package manager, used to install and manage third-party libraries."),
        ("What is a virtual environment?", "An isolated Python environment (created with venv) that keeps project dependencies separate."),
        ("What is PEP 8?", "The official style guide for writing readable, consistent Python code."),
        ("What is CPython?", "The reference (default) implementation of Python, written in C."),
        ("Code:\nprint(__name__)\n\nWhat does this print when the file is run directly?", "'__main__'"),
        ("Code:\nif __name__ == '__main__':\n    print('run directly')\n\nWhy is this pattern used?", "It ensures the code only runs when the file is executed directly, not when imported as a module."),
        ("Code:\nimport sys\nprint(sys.version_info.major)\n\nWhat does this print (on Python 3)?", "3"),
        ("Code:\n# pip install requests\nimport requests\n\nWhat must happen before this import works?", "The 'requests' package must be installed via pip first, or an ImportError is raised."),
        ("Code:\nprint(type(3))\n\nWhat is the output?", "<class 'int'>"),
        ("Command: python3 --version\n\nWhat does this show?", "The installed Python 3 interpreter version."),
        ("Command: python -m venv myenv\n\nWhat does this do?", "Creates a new virtual environment named 'myenv'."),
        ("Command (Linux/Mac): source myenv/bin/activate\n\nWhat does this do?", "Activates the virtual environment so installed packages are isolated to it."),
        ("Code:\nimport this\n\nWhat happens when this runs?", "It prints 'The Zen of Python', a set of guiding principles for Python design."),
        ("Code:\nprint(1_000_000)\n\nWhat is the output?", "1000000 — underscores in numeric literals are ignored and just aid readability."),
        ("Command: pip freeze > requirements.txt\n\nWhat does this do?", "Writes all installed package names and versions to a requirements.txt file."),
        ("Command: pip install -r requirements.txt\n\nWhat does this do?", "Installs all packages listed in requirements.txt."),
        ("Code:\nimport platform\nprint(platform.python_version())\n\nWhat does this print?", "The current Python version as a string, e.g. '3.12.1'."),
        ("What file extension do Python scripts use?", ".py"),
        ("How do you run a Python script from the terminal?", "python filename.py"),
        ("Code:\n# comment\nprint('hi')  # inline comment\n\nDoes the comment affect execution?", "No, everything after # on that logical line is ignored by the interpreter."),
        ("Code:\n'''\nThis is a docstring/comment block\n'''\nprint('after')\n\nWhat prints?", "after — the triple-quoted string is just an unused expression, effectively a comment."),
        ("What is the Python REPL?", "The interactive shell (Read-Eval-Print Loop) used to test code line by line."),
        ("Name two popular Python IDEs/editors.", "PyCharm and VS Code (also Jupyter Notebook and IDLE)."),
        ("Code:\nimport sys\nsys.exit(1)\n\nWhat does this do?", "Terminates the program immediately with exit status 1."),
        ("Code:\nprint(sys.path)\n\n(assuming import sys was done) What does sys.path contain?", "A list of directories Python searches for modules to import."),
        ("Command: which python3 (Linux/Mac)\n\nWhat does this show?", "The filesystem path to the python3 executable currently in use."),
        ("Code:\nimport os\nprint(os.getcwd())\n\nWhat does this print?", "The current working directory of the running script."),
        ("Command: deactivate\n\nWhat does this do inside an active virtual environment?", "Exits the virtual environment, returning to the system Python."),
        ("Code:\nx = 5\ndel x\nprint(x)\n\nWhat happens?", "NameError: name 'x' is not defined, because del removed the binding."),
        ("Code:\nprint(2 ** 10)\n\nWhat is the output?", "1024"),
        ("Code:\nimport random\nprint(type(random.random()))\n\nWhat does this print?", "<class 'float'>"),
        ("Command: python -c \"print('hi')\"\n\nWhat does this do?", "Runs the given string as a Python program directly from the command line, printing 'hi'."),
        ("Code:\nimport keyword\nprint(keyword.iskeyword('class'))\n\nWhat is the output?", "True"),
        ("What is a module in the context of setup and imports?", "A single .py file containing Python code that can be imported elsewhere."),
        ("What is a package (as opposed to a module)?", "A directory of Python modules containing an __init__.py file (or namespace package), allowing grouped imports."),
        ("Code:\nprint(3 / 0)\n\nWhat happens?", "ZeroDivisionError is raised, halting the program unless caught."),
        ("Code:\nimport math\nprint(math.pi)\n\nWhat is the output (approximately)?", "3.141592653589793"),
        ("Command: pip list\n\nWhat does this show?", "All packages currently installed in the active Python environment."),
        ("Code:\nprint(id(5) == id(5))\n\nWhat is the output and why?", "True — small integers are cached/interned by CPython, so both refer to the same object."),
        ("What is a linter, and name one for Python?", "A tool that analyzes code for style and potential errors without running it; examples include pylint and flake8."),
        ("Code:\nassert 1 == 1, 'should be true'\nprint('passed')\n\nWhat prints?", "passed — the assertion succeeds silently since the condition is True."),
        ("Code:\nassert 1 == 2, 'mismatch'\n\nWhat happens?", "AssertionError: mismatch is raised, since the condition is False."),
        ("Command: python -O script.py\n\nWhat does the -O flag do?", "Runs the script with basic optimizations and disables assert statements."),
        ("Code:\nimport sys\nprint(sys.argv)\n\nWhat does sys.argv contain when running 'python script.py a b'?", "['script.py', 'a', 'b'] — the script name followed by command-line arguments."),
        ("What is bytecode in the context of CPython?", "A low-level, platform-independent set of instructions that CPython compiles source code into before execution."),
        ("Code:\nprint(dir(str))\n\nWhat does this show?", "A list of all attributes and methods available on the str type."),
        ("What does the .pyc file extension represent?", "Compiled Python bytecode cached by CPython to speed up subsequent imports."),
    ],
    "Python Basics and Syntax": [
        ("How does Python define code blocks?", "Using indentation (whitespace), not curly braces."),
        ("What is a variable?", "A named reference used to store a value in memory."),
        ("Do you need to declare variable types in Python?", "No, Python is dynamically typed; types are inferred at runtime."),
        ("Code:\nx = 5\nx = 'hello'\nprint(x)\n\nWhat is the output?", "hello — Python variables can be reassigned to any type."),
        ("Code:\nprint('Hello' + ' ' + 'World')\n\nWhat is the output?", "Hello World"),
        ("Code:\nname = 'Amy'\nprint(f'Hi {name}!')\n\nWhat is the output?", "Hi Amy!"),
        ("Code:\nprint(type(5), type(5.0), type('5'))\n\nWhat is the output?", "<class 'int'> <class 'float'> <class 'str'>"),
        ("Code:\nx = input()\nprint(type(x))\n\n(user enters 42) What is the printed type?", "<class 'str'> — input() always returns a string, even if it looks numeric."),
        ("Code:\nprint(int('42') + 8)\n\nWhat is the output?", "50"),
        ("Code:\nprint(str(42) + '8')\n\nWhat is the output?", "428 — concatenation of strings, not addition."),
        ("Code:\nmy_variable = 10\nMyVariable = 20\nprint(my_variable, MyVariable)\n\nWhat is the output?", "10 20 — Python is case-sensitive, so these are different variables."),
        ("Code:\nx, y = 1, 2\nx, y = y, x\nprint(x, y)\n\nWhat is the output?", "2 1 — tuple unpacking swaps the values."),
        ("Code:\nprint('''line1\nline2''')\n\nWhat is the output?", "line1\\nline2 printed as two lines, since triple quotes preserve the embedded newline."),
        ("Code:\nprint(5 == '5')\n\nWhat is the output?", "False — different types are never equal in this comparison."),
        ("Code:\nx = None\nprint(x is None)\n\nWhat is the output?", "True"),
        ("Code:\nprint(bool(0), bool(1), bool(''), bool('a'))\n\nWhat is the output?", "False True False True"),
        ("Code:\nprint(len('hello'))\n\nWhat is the output?", "5"),
        ("Code:\nname = 'Bob'\nage = 30\nprint(f'{name} is {age} years old')\n\nWhat is the output?", "Bob is 30 years old"),
        ("Code:\nprint(10 // 3, 10 % 3)\n\nWhat is the output?", "3 1"),
        ("Code:\nx = '5'\ny = 5\nprint(x == y)\n\nWhat is the output?", "False"),
        ("What is the naming convention for variables?", "snake_case, e.g., my_variable."),
        ("Code:\nprint(type(True))\n\nWhat is the output?", "<class 'bool'>"),
        ("Code:\nprint(1 + True)\n\nWhat is the output and why?", "2 — bool is a subclass of int, so True behaves as 1."),
        ("Code:\nprint('Py' 'thon')\n\nWhat is the output?", "Python — adjacent string literals are automatically concatenated."),
        ("Code:\nx = 3.14159\nprint(round(x, 2))\n\nWhat is the output?", "3.14"),
        ("Code:\nprint(float('3.5') + 1)\n\nWhat is the output?", "4.5"),
        ("Code:\nprint('abc'.upper())\n\nWhat is the output?", "ABC"),
        ("Code:\nprint('  hi  '.strip())\n\nWhat is the output?", "hi — leading and trailing whitespace removed."),
        ("Code:\nx = 7\nprint(f'{x:03d}')\n\nWhat is the output?", "007 — zero-padded to 3 digits."),
        ("Code:\npi = 3.14159\nprint(f'{pi:.2f}')\n\nWhat is the output?", "3.14"),
        ("Code:\nprint(int(3.9))\n\nWhat is the output?", "3 — int() truncates toward zero, it doesn't round."),
        ("Code:\nprint('10' + '20')\n\nWhat is the output?", "1020 — string concatenation, not addition."),
        ("What does the len() function do?", "Returns the number of items in an object such as a string, list, or dictionary."),
        ("Code:\nprint('hello'[1])\n\nWhat is the output?", "e — string indexing is zero-based."),
        ("Code:\nprint('hello'[-1])\n\nWhat is the output?", "o — negative indices count from the end."),
        ("Code:\nx = 5\nprint(f'{x=}')\n\nWhat is the output?", "x=5 — the '=' specifier in f-strings shows both the expression and its value."),
        ("Code:\nprint(type(None))\n\nWhat is the output?", "<class 'NoneType'>"),
        ("Code:\nx = 1; y = 2; print(x, y)\n\nWhat is the output and what does the semicolon do?", "1 2 — semicolons separate multiple statements on one line."),
        ("Code:\nprint('Line1\\nLine2')\n\nWhat is the output?", "Line1 and Line2 printed on two separate lines."),
        ("Code:\nprint('It\\'s here')\n\nWhat is the output?", "It's here — the backslash escapes the apostrophe."),
        ("What is the difference between = and ==?", "= assigns a value; == compares two values for equality."),
        ("Code:\nx = 10\ny = x\ny += 5\nprint(x, y)\n\nWhat is the output?", "10 15 — integers are immutable, so rebinding y doesn't affect x."),
        ("Code:\nprint(str([1, 2, 3]))\n\nWhat is the output?", "'[1, 2, 3]' — a string representation of the list."),
        ("Code:\nprint(9 ** 0.5)\n\nWhat is the output?", "3.0"),
        ("Code:\nname = 'World'\nprint('Hello, %s!' % name)\n\nWhat is the output?", "Hello, World! — old-style % string formatting."),
        ("Code:\nprint('{} and {}'.format('cats', 'dogs'))\n\nWhat is the output?", "cats and dogs"),
        ("What is a docstring's purpose at the top of a module?", "It documents the module's purpose and can be accessed via the module's __doc__ attribute."),
        ("Code:\nx = 0b101\nprint(x)\n\nWhat is the output?", "5 — 0b101 is binary literal notation for the number 5."),
        ("Code:\nx = 0x1A\nprint(x)\n\nWhat is the output?", "26 — 0x1A is hexadecimal notation."),
        ("Code:\nprint(type(3 + 4j))\n\nWhat is the output?", "<class 'complex'>"),
    ],
    "Operators and Expressions": [
        ("Code:\nprint(7 / 2)\n\nWhat is the output?", "3.5"),
        ("Code:\nprint(7 // 2)\n\nWhat is the output?", "3"),
        ("Code:\nprint(-7 // 2)\n\nWhat is the output and why?", "-4 — floor division rounds toward negative infinity, not toward zero."),
        ("Code:\nprint(7 % 2)\n\nWhat is the output?", "1"),
        ("Code:\nprint(-7 % 2)\n\nWhat is the output and why?", "1 — Python's modulus result takes the sign of the divisor."),
        ("Code:\nprint(2 ** 3 ** 2)\n\nWhat is the output and why?", "512 — exponentiation is right-associative, so it evaluates as 2 ** (3 ** 2)."),
        ("Code:\nprint(2 + 3 * 4)\n\nWhat is the output?", "14 — multiplication has higher precedence than addition."),
        ("Code:\nprint((2 + 3) * 4)\n\nWhat is the output?", "20"),
        ("Code:\nprint(5 == 5.0)\n\nWhat is the output?", "True — numeric equality compares value, not type."),
        ("Code:\nprint(5 is 5.0)\n\nWhat is the output and why?", "False — 'is' checks identity, and int/float are different objects."),
        ("Code:\na = [1, 2]\nb = [1, 2]\nprint(a == b, a is b)\n\nWhat is the output?", "True False — equal values but different objects in memory."),
        ("Code:\nprint(True and False)\nprint(True or False)\nprint(not True)\n\nWhat is the output?", "False\nTrue\nFalse"),
        ("Code:\nprint(1 and 2)\n\nWhat is the output and why?", "2 — 'and' returns the second operand if the first is truthy."),
        ("Code:\nprint(0 or 5)\n\nWhat is the output and why?", "5 — 'or' returns the first truthy value, or the last if none are truthy."),
        ("Code:\nprint([] or 'default')\n\nWhat is the output?", "default — an empty list is falsy."),
        ("Code:\nx = 5\nprint(x > 3 and x < 10)\n\nWhat is the output?", "True"),
        ("Code:\nprint(3 in [1, 2, 3])\n\nWhat is the output?", "True"),
        ("Code:\nprint('a' not in 'banana')\n\nWhat is the output?", "False — 'a' is in 'banana'."),
        ("Code:\nx = 5\nx += 3\nprint(x)\n\nWhat is the output?", "8"),
        ("Code:\nx = 10\nx //= 3\nprint(x)\n\nWhat is the output?", "3"),
        ("Code:\nx = 2\nx **= 4\nprint(x)\n\nWhat is the output?", "16"),
        ("Code:\nprint(5 & 3)\n\nWhat is the output?", "1 — bitwise AND: 0101 & 0011 = 0001."),
        ("Code:\nprint(5 | 2)\n\nWhat is the output?", "7 — bitwise OR: 0101 | 0010 = 0111."),
        ("Code:\nprint(5 ^ 1)\n\nWhat is the output?", "4 — bitwise XOR: 0101 ^ 0001 = 0100."),
        ("Code:\nprint(1 << 3)\n\nWhat is the output?", "8 — left shift multiplies by 2 per shifted bit."),
        ("Code:\nprint(16 >> 2)\n\nWhat is the output?", "4 — right shift divides by 2 per shifted bit."),
        ("Code:\nprint(~5)\n\nWhat is the output and why?", "-6 — bitwise NOT computes -(x + 1)."),
        ("Code:\nprint(1 < 2 < 3)\n\nWhat is the output and why?", "True — Python supports chained comparisons, equivalent to (1<2) and (2<3)."),
        ("Code:\nx = (y := 5) + 1\nprint(x, y)\n\nWhat is the output?", "6 5 — the walrus operator assigns y while returning its value for use in the expression."),
        ("What does the walrus operator (:=) do?", "Assigns a value to a variable as part of a larger expression (Python 3.8+)."),
        ("Code:\nprint('ab' * 3)\n\nWhat is the output?", "ababab — strings support repetition with *."),
        ("Code:\nprint([1, 2] * 2)\n\nWhat is the output?", "[1, 2, 1, 2]"),
        ("Code:\nprint([1, 2] + [3, 4])\n\nWhat is the output?", "[1, 2, 3, 4] — list concatenation."),
        ("Code:\nprint(10 != 10.0)\n\nWhat is the output?", "False"),
        ("Code:\nprint(not [])\n\nWhat is the output and why?", "True — an empty list is falsy, so 'not' flips it to True."),
        ("Code:\nprint(3 + 4 == 7 and 2 * 2 == 4)\n\nWhat is the output?", "True"),
        ("Code:\nx = 5\nprint(x == 5 or 1 / 0)\n\nWhat is the output and why no error?", "True — short-circuit evaluation skips the second operand once 'or' finds a truthy first operand."),
        ("Code:\nprint(10 / 4)\n\nWhat is the output?", "2.5"),
        ("What is operator precedence?", "The order in which operations are evaluated, e.g. ** before * before +."),
        ("Code:\nprint(bool('False'))\n\nWhat is the output and why?", "True — any non-empty string is truthy, regardless of its content."),
        ("Code:\nprint(2 == 2 == 2)\n\nWhat is the output?", "True — chained equality checks 2==2 and 2==2."),
        ("Code:\nprint(5 // 2.0)\n\nWhat is the output and why?", "2.0 — floor division with a float operand returns a float."),
        ("Code:\nprint(4 % 2 == 0 and 4 > 0)\n\nWhat is the output?", "True"),
        ("Code:\nx = 'abc'\ny = 'abc'\nprint(x is y)\n\nWhat is the output and why?", "True — CPython interns short string literals so identical ones share memory."),
        ("Code:\nprint(1_000 + 1_000)\n\nWhat is the output?", "2000 — underscores in numeric literals are purely visual."),
        ("Code:\nprint('5' * 3)\n\nWhat is the output?", "555 — string repetition, not multiplication."),
        ("Code:\nprint(abs(-7))\n\nWhat is the output?", "7"),
        ("Code:\nprint(divmod(17, 5))\n\nWhat is the output?", "(3, 2) — quotient and remainder as a tuple."),
        ("Code:\nprint(max(3, 7, 2), min(3, 7, 2))\n\nWhat is the output?", "7 2"),
        ("What are membership operators?", "'in' and 'not in', used to test whether a value exists in a sequence."),
    ],
    "Control Flow and Loops": [
        ("Code:\nx = 5\nif x > 3:\n    print('big')\nelse:\n    print('small')\n\nWhat is the output?", "big"),
        ("Code:\nfor i in range(3):\n    print(i)\n\nWhat is the output?", "0\n1\n2"),
        ("Code:\nfor i in range(2, 8, 2):\n    print(i)\n\nWhat is the output?", "2\n4\n6"),
        ("Code:\ni = 0\nwhile i < 3:\n    print(i)\n    i += 1\n\nWhat is the output?", "0\n1\n2"),
        ("Code:\nfor i in range(5):\n    if i == 3:\n        break\n    print(i)\n\nWhat is the output?", "0\n1\n2"),
        ("Code:\nfor i in range(5):\n    if i % 2 == 0:\n        continue\n    print(i)\n\nWhat is the output?", "1\n3"),
        ("Code:\nx = 10\nif x > 5:\n    print('a')\nelif x > 8:\n    print('b')\nelse:\n    print('c')\n\nWhat is the output and why?", "a — once the first True branch runs, later elif branches are skipped even if also True."),
        ("Code:\nfor i in range(3):\n    print(i)\nelse:\n    print('done')\n\nWhat is the output?", "0\n1\n2\ndone — the else clause runs since the loop completed without a break."),
        ("Code:\nfor i in range(5):\n    if i == 2:\n        break\nelse:\n    print('done')\nprint('after')\n\nWhat is the output?", "after — 'done' is skipped because break prevented the for-else clause from running."),
        ("Code:\nx = 7\nresult = 'even' if x % 2 == 0 else 'odd'\nprint(result)\n\nWhat is the output?", "odd — this is a ternary conditional expression."),
        ("Code:\nfor i, val in enumerate(['a', 'b', 'c']):\n    print(i, val)\n\nWhat is the output?", "0 a\n1 b\n2 c"),
        ("Code:\nfor i in range(3):\n    for j in range(2):\n        print(i, j)\n\nWhat is the output?", "0 0\n0 1\n1 0\n1 1\n2 0\n2 1"),
        ("Code:\nx = None\nif x:\n    print('yes')\nelse:\n    print('no')\n\nWhat is the output?", "no — None is falsy."),
        ("Code:\ncount = 0\nwhile True:\n    count += 1\n    if count == 3:\n        break\nprint(count)\n\nWhat is the output?", "3"),
        ("Code:\nfor letter in 'abc':\n    print(letter)\n\nWhat is the output?", "a\nb\nc"),
        ("Code:\nfor i in range(5):\n    pass\nprint('done')\n\nWhat is the output and what does pass do?", "done — pass is a no-op placeholder that lets the loop body be syntactically valid while doing nothing."),
        ("Code:\nx = 5\nif x > 10:\n    print('big')\nprint('after')\n\nWhat is the output?", "after — 'big' is skipped since the if condition is False, but the unindented line always runs."),
        ("Code:\nnums = [1, 2, 3]\nfor n in nums:\n    if n == 2:\n        continue\n    print(n)\n\nWhat is the output?", "1\n3"),
        ("Code:\nfor i in range(10, 0, -2):\n    print(i)\n\nWhat is the output?", "10\n8\n6\n4\n2"),
        ("Code:\ni = 5\nwhile i > 0:\n    print(i)\n    i -= 2\n\nWhat is the output?", "5\n3\n1"),
        ("Code:\nx = 3\nwhile x:\n    print(x)\n    x -= 1\n\nWhat is the output and why does it stop?", "3\n2\n1 — the loop stops when x becomes 0, which is falsy."),
        ("Code:\nfor i in range(3):\n    if i == 1:\n        break\n    else:\n        print(i)\nelse:\n    print('finished')\n\nWhat is the output?", "0 — the for-else 'finished' doesn't print because break exited the loop early."),
        ("Code:\nfruits = ['apple', 'banana']\nfor i in range(len(fruits)):\n    print(i, fruits[i])\n\nWhat is the output?", "0 apple\n1 banana"),
        ("What does the break statement do?", "Immediately exits the nearest enclosing loop."),
        ("What does the continue statement do?", "Skips the rest of the current loop iteration and moves to the next one."),
        ("Code:\nx = 4\nif x == 1:\n    print('one')\nif x == 2:\n    print('two')\nif x == 4:\n    print('four')\n\nWhat is the output and why not use elif here?", "four — since these are separate if statements (not elif), all are checked independently."),
        ("Code:\nresult = [i for i in range(5) if i % 2 == 0]\nprint(result)\n\nWhat is the output?", "[0, 2, 4] — a list comprehension combining a for loop and a condition."),
        ("Code:\nfor i in []:\n    print(i)\nprint('done')\n\nWhat is the output?", "done — the loop body never executes over an empty sequence."),
        ("Code:\nx = 1\nwhile x <= 100:\n    x *= 10\nprint(x)\n\nWhat is the output?", "1000"),
        ("Code:\nfor n in range(3, 0, -1):\n    print(f'Countdown: {n}')\nprint('Liftoff!')\n\nWhat is the output?", "Countdown: 3\nCountdown: 2\nCountdown: 1\nLiftoff!"),
        ("What does the range() function do?", "Generates a sequence of numbers, commonly used with for loops."),
        ("Code:\nx = 5\ny = 'big' if x > 10 else 'medium' if x > 3 else 'small'\nprint(y)\n\nWhat is the output?", "medium — chained ternary expressions evaluate left to right."),
        ("Code:\nfor i in range(3):\n    for j in range(3):\n        if j == 1:\n            break\n        print(i, j)\n\nWhat is the output?", "0 0\n1 0\n2 0 — break only exits the inner loop, not the outer one."),
        ("Code:\ntotal = 0\nfor i in range(1, 6):\n    total += i\nprint(total)\n\nWhat is the output?", "15"),
        ("Code:\nx = 0\nif x:\n    print('truthy')\nelif not x:\n    print('falsy')\n\nWhat is the output?", "falsy"),
        ("Code:\nwords = ['cat', 'dog', 'bird']\nfor w in words:\n    if len(w) > 3:\n        print(w)\n        break\n\nWhat is the output?", "bird — 'cat' and 'dog' have length 3, so only 'bird' triggers the print and break."),
        ("Code:\ncounter = 0\nfor i in range(5):\n    if i == 2:\n        counter += 10\n        continue\n    counter += 1\nprint(counter)\n\nWhat is the output?", "14 — four iterations add 1 each (4) and one iteration adds 10, totaling 14."),
        ("Code:\nx = 'yes'\nmatch x:\n    case 'yes':\n        print('confirmed')\n    case 'no':\n        print('denied')\n    case _:\n        print('unknown')\n\nWhat is the output? (Python 3.10+ match statement)", "confirmed"),
        ("Code:\nn = 7\nmatch n:\n    case n if n % 2 == 0:\n        print('even')\n    case _:\n        print('odd')\n\nWhat is the output?", "odd — the match statement's guard condition (n % 2 == 0) is False for 7."),
        ("What is a nested loop?", "A loop placed inside the body of another loop."),
        ("Code:\nfor i in range(3):\n    print('start')\n    if i == 1:\n        continue\n    print('end')\n\nWhat is the output?", "start\nend\nstart\nstart\nend — when i==1, 'end' is skipped by continue."),
        ("Code:\nvalues = [10, 20, 30]\nindex = 0\nwhile index < len(values):\n    print(values[index])\n    index += 1\n\nWhat is the output?", "10\n20\n30"),
        ("Code:\nx = 5\nif x != 5:\n    print('not five')\nelse:\n    print('is five')\n\nWhat is the output?", "is five"),
        ("Code:\nfor i in range(1, 4):\n    print(i * i)\n\nWhat is the output?", "1\n4\n9"),
        ("Code:\nn = 0\nwhile n < 5:\n    n += 1\n    if n == 3:\n        break\nelse:\n    print('completed')\nprint(n)\n\nWhat is the output?", "3 — 'completed' is skipped because break fired, and n stopped at 3."),
        ("Code:\nfor c in 'hi':\n    for d in 'yo':\n        print(c + d)\n\nWhat is the output?", "hy\nho\niy\nio"),
        ("What is the syntax for if-elif-else?", "if condition: ... elif condition: ... else: ..."),
        ("Code:\nx = -3\nif x > 0:\n    sign = 'positive'\nelif x < 0:\n    sign = 'negative'\nelse:\n    sign = 'zero'\nprint(sign)\n\nWhat is the output?", "negative"),
        ("Code:\nnums = [1, 2, 3, 4]\nsquares = []\nfor n in nums:\n    squares.append(n ** 2)\nprint(squares)\n\nWhat is the output?", "[1, 4, 9, 16]"),
        ("Code:\nx = 5\ny = 10\nif x > y:\n    bigger = x\nelse:\n    bigger = y\nprint(bigger)\n\nWhat is the output?", "10"),
    ],
    "Data Structures and Collections": [
        ("Code:\nmy_list = [1, 2, 3]\nmy_list.append(4)\nprint(my_list)\n\nWhat is the output?", "[1, 2, 3, 4]"),
        ("Code:\nmy_list = [1, 2, 3]\nprint(my_list[1])\n\nWhat is the output?", "2"),
        ("Code:\nmy_list = [1, 2, 3, 4, 5]\nprint(my_list[1:4])\n\nWhat is the output?", "[2, 3, 4] — slicing excludes the stop index."),
        ("Code:\nmy_list = [1, 2, 3, 4, 5]\nprint(my_list[::-1])\n\nWhat is the output?", "[5, 4, 3, 2, 1] — reverses the list."),
        ("Code:\nmy_list = [1, 2, 3]\nmy_list.remove(2)\nprint(my_list)\n\nWhat is the output?", "[1, 3]"),
        ("Code:\nmy_list = [1, 2, 3]\npopped = my_list.pop()\nprint(my_list, popped)\n\nWhat is the output?", "[1, 2] 3 — pop() removes and returns the last element by default."),
        ("Code:\nmy_list = [1, 2, 3]\ndel my_list[0]\nprint(my_list)\n\nWhat is the output?", "[2, 3]"),
        ("Code:\nresult = [x * 2 for x in range(5)]\nprint(result)\n\nWhat is the output?", "[0, 2, 4, 6, 8] — a list comprehension."),
        ("Code:\nd = {'a': 1, 'b': 2}\nprint(d.get('c', 'not found'))\n\nWhat is the output?", "not found — get() returns the default when the key is missing."),
        ("Code:\nt = (1, 2, 3)\nt[0] = 5\n\nWhat happens?", "TypeError: 'tuple' object does not support item assignment, since tuples are immutable."),
        ("Code:\nd1 = {'a': 1}\nd2 = {'b': 2}\nd1.update(d2)\nprint(d1)\n\nWhat is the output?", "{'a': 1, 'b': 2}"),
        ("Code:\ns1 = {'a': 1}\ns2 = {'b': 2}\nmerged = s1 | s2\nprint(merged)\n\nWhat is the output? (Python 3.9+)", "{'a': 1, 'b': 2} — the | operator merges dicts."),
        ("Code:\nmy_set = {1, 2, 2, 3, 3, 3}\nprint(my_set)\n\nWhat is the output?", "{1, 2, 3} — sets automatically drop duplicates."),
        ("Code:\na = {1, 2, 3}\nb = {2, 3, 4}\nprint(a & b)\n\nWhat is the output?", "{2, 3} — set intersection."),
        ("Code:\na = {1, 2, 3}\nb = {2, 3, 4}\nprint(a | b)\n\nWhat is the output?", "{1, 2, 3, 4} — set union."),
        ("Code:\na = {1, 2, 3}\nb = {2, 3}\nprint(a - b)\n\nWhat is the output?", "{1} — set difference."),
        ("Code:\nmy_list = [3, 1, 4, 1, 5]\nmy_list.sort()\nprint(my_list)\n\nWhat is the output?", "[1, 1, 3, 4, 5]"),
        ("Code:\nmy_list = [3, 1, 4]\nprint(sorted(my_list, reverse=True))\n\nWhat is the output?", "[4, 3, 1]"),
        ("Code:\nd = {'a': 1, 'b': 2}\nfor key in d:\n    print(key)\n\nWhat is the output?", "a\nb — iterating a dict directly yields its keys."),
        ("Code:\nd = {'a': 1, 'b': 2}\nfor k, v in d.items():\n    print(k, v)\n\nWhat is the output?", "a 1\nb 2"),
        ("Code:\nmy_tuple = (1, 2, 3)\na, b, c = my_tuple\nprint(a, b, c)\n\nWhat is the output?", "1 2 3 — tuple unpacking."),
        ("Code:\nnested = [[1, 2], [3, 4]]\nprint(nested[1][0])\n\nWhat is the output?", "3"),
        ("Code:\nmy_list = [1, 2, 3]\nmy_list2 = my_list\nmy_list2.append(4)\nprint(my_list)\n\nWhat is the output and why?", "[1, 2, 3, 4] — both names reference the same list object, so mutating one affects the other."),
        ("Code:\nmy_list = [1, 2, 3]\nmy_list2 = my_list.copy()\nmy_list2.append(4)\nprint(my_list)\n\nWhat is the output?", "[1, 2, 3] — copy() makes a separate list, so the original is unaffected."),
        ("Code:\nprint(list(range(3)))\n\nWhat is the output?", "[0, 1, 2]"),
        ("Code:\nmy_list = ['a', 'b', 'c']\nprint('b' in my_list)\n\nWhat is the output?", "True"),
        ("Code:\nd = {}\nd['x'] = 1\nd['y'] = 2\nprint(d)\n\nWhat is the output?", "{'x': 1, 'y': 2}"),
        ("Code:\nd = {'a': 1}\nprint(d['b'])\n\nWhat happens?", "KeyError: 'b', since the key doesn't exist and [] doesn't provide a default."),
        ("Code:\nmy_list = [1, 2, 3]\nmy_list.insert(1, 99)\nprint(my_list)\n\nWhat is the output?", "[1, 99, 2, 3]"),
        ("Code:\nmy_list = [1, [2, 3], 4]\nprint(len(my_list))\n\nWhat is the output?", "3 — the nested list counts as one element."),
        ("Code:\nprint(tuple([1, 2, 3]))\n\nWhat is the output?", "(1, 2, 3) — converts a list into a tuple."),
        ("Code:\nprint(set([1, 2, 2, 3]))\n\nWhat is the output?", "{1, 2, 3}"),
        ("Code:\nmy_dict = dict(a=1, b=2)\nprint(my_dict)\n\nWhat is the output?", "{'a': 1, 'b': 2}"),
        ("Code:\nlst = [1, 2, 3, 4, 5]\nprint(lst[::2])\n\nWhat is the output?", "[1, 3, 5] — every second element."),
        ("Code:\nresult = {x: x**2 for x in range(4)}\nprint(result)\n\nWhat is the output?", "{0: 0, 1: 1, 2: 4, 3: 9} — a dictionary comprehension."),
        ("Code:\nlst = [1, 2, 3]\nlst.extend([4, 5])\nprint(lst)\n\nWhat is the output?", "[1, 2, 3, 4, 5] — extend adds each element individually (unlike append)."),
        ("Code:\nlst = [1, 2, 3]\nlst.append([4, 5])\nprint(lst)\n\nWhat is the output and how does it differ from extend?", "[1, 2, 3, [4, 5]] — append adds the whole list as a single nested element."),
        ("Code:\nprint(max([3, 7, 2, 9]))\n\nWhat is the output?", "9"),
        ("Code:\nlst = [5, 3, 8, 1]\nprint(sorted(lst))\nprint(lst)\n\nWhat is the output and why does the second line differ?", "[1, 3, 5, 8]\n[5, 3, 8, 1] — sorted() returns a new list without modifying the original, unlike .sort()."),
        ("Code:\nprint(', '.join(['a', 'b', 'c']))\n\nWhat is the output?", "a, b, c — joins list elements into a string with the given separator."),
        ("Code:\nprint('a,b,c'.split(','))\n\nWhat is the output?", "['a', 'b', 'c']"),
        ("Code:\nstack = []\nstack.append(1)\nstack.append(2)\nprint(stack.pop())\n\nWhat is the output and what pattern does this show?", "2 — this demonstrates a stack (LIFO) using a list."),
        ("Code:\nfrom collections import deque\nq = deque([1, 2, 3])\nq.popleft()\nprint(q)\n\nWhat is the output?", "deque([2, 3]) — popleft() removes from the front, useful for queue (FIFO) behavior."),
        ("What is a list?", "An ordered, mutable collection of items."),
        ("What is a tuple?", "An ordered, immutable collection of items."),
        ("What is a dictionary?", "A collection of key-value pairs."),
        ("What is a set?", "An unordered collection of unique elements."),
        ("Code:\nd = {'a': 1, 'b': 2}\nprint(list(d.keys()))\n\nWhat is the output?", "['a', 'b']"),
        ("Code:\nd = {'a': 1, 'b': 2}\nprint(list(d.values()))\n\nWhat is the output?", "[1, 2]"),
        ("Code:\nnames = ['Al', 'Bo']\nages = [30, 25]\nprint(list(zip(names, ages)))\n\nWhat is the output?", "[('Al', 30), ('Bo', 25)] — zip() pairs elements from multiple iterables."),
    ],
    "Functions and Modular Code": [
        ("Code:\ndef greet(name):\n    return f'Hello, {name}!'\nprint(greet('Sam'))\n\nWhat is the output?", "Hello, Sam!"),
        ("Code:\ndef add(a, b=10):\n    return a + b\nprint(add(5))\n\nWhat is the output?", "15 — b uses its default value since no second argument was given."),
        ("Code:\ndef add(a, b=10):\n    return a + b\nprint(add(5, 20))\n\nWhat is the output?", "25 — the passed argument overrides the default."),
        ("Code:\ndef total(*args):\n    return sum(args)\nprint(total(1, 2, 3, 4))\n\nWhat is the output?", "10 — *args collects extra positional arguments into a tuple."),
        ("Code:\ndef show(**kwargs):\n    print(kwargs)\nshow(a=1, b=2)\n\nWhat is the output?", "{'a': 1, 'b': 2} — **kwargs collects keyword arguments into a dict."),
        ("Code:\nsquare = lambda x: x ** 2\nprint(square(5))\n\nWhat is the output?", "25"),
        ("Code:\ndef outer():\n    x = 1\n    def inner():\n        return x + 1\n    return inner()\nprint(outer())\n\nWhat is the output and why?", "2 — the inner function has access to the enclosing scope's variable x (a closure)."),
        ("Code:\nx = 10\ndef change():\n    global x\n    x = 20\nchange()\nprint(x)\n\nWhat is the output?", "20 — global lets the function modify the module-level variable."),
        ("Code:\nx = 10\ndef change():\n    x = 20\nchange()\nprint(x)\n\nWhat is the output and why?", "10 — without 'global', x inside the function is a separate local variable."),
        ("Code:\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\nprint(factorial(5))\n\nWhat is the output?", "120 — a recursive function computing 5!."),
        ("Code:\ndef greet(name='World'):\n    return f'Hello, {name}'\nprint(greet())\n\nWhat is the output?", "Hello, World"),
        ("Code:\ndef f(a, b, c):\n    return a + b + c\nprint(f(c=3, a=1, b=2))\n\nWhat is the output and what is this calling style called?", "6 — this uses keyword arguments, allowing any order."),
        ("Code:\ndef f():\n    pass\nresult = f()\nprint(result)\n\nWhat is the output and why?", "None — a function with no return statement implicitly returns None."),
        ("Code:\nnums = [1, 2, 3, 4]\nsquares = list(map(lambda x: x ** 2, nums))\nprint(squares)\n\nWhat is the output?", "[1, 4, 9, 16] — map() applies the lambda to every element."),
        ("Code:\nnums = [1, 2, 3, 4, 5]\nevens = list(filter(lambda x: x % 2 == 0, nums))\nprint(evens)\n\nWhat is the output?", "[2, 4] — filter() keeps only elements where the lambda returns True."),
        ("Code:\ndef make_multiplier(n):\n    def multiplier(x):\n        return x * n\n    return multiplier\ntimes3 = make_multiplier(3)\nprint(times3(5))\n\nWhat is the output and what pattern is this?", "15 — this is a closure, where multiplier 'remembers' n from its enclosing scope."),
        ("Code:\ndef risky(a, b):\n    return a / b\nprint(risky(10, 2))\n\nWhat is the output?", "5.0"),
        ("Code:\ndef add_item(item, items=[]):\n    items.append(item)\n    return items\nprint(add_item(1))\nprint(add_item(2))\n\nWhat is the output and why is this a common bug?", "[1]\n[1, 2] — mutable default arguments persist across calls since they're created only once."),
        ("Code:\ndef f(x: int, y: int) -> int:\n    return x + y\nprint(f(2, 3))\n\nWhat is the output, and what do the ': int' and '-> int' annotations do?", "5 — they're type hints documenting expected types; Python does not enforce them at runtime."),
        ("Code:\ndef stars(n):\n    return '*' * n\nfor i in range(1, 4):\n    print(stars(i))\n\nWhat is the output?", "*\n**\n***"),
        ("Code:\ndef process(*args, **kwargs):\n    print(args, kwargs)\nprocess(1, 2, a=3, b=4)\n\nWhat is the output?", "(1, 2) {'a': 3, 'b': 4}"),
        ("Code:\ndef safe_divide(a, b):\n    if b == 0:\n        return None\n    return a / b\nprint(safe_divide(10, 0))\n\nWhat is the output?", "None"),
        ("What is a lambda function?", "A small, anonymous, single-expression function defined with the lambda keyword."),
        ("What is variable scope?", "The region of code where a variable can be accessed — local, global, or nonlocal."),
        ("Code:\ndef outer():\n    x = 'outer'\n    def inner():\n        nonlocal x\n        x = 'inner'\n    inner()\n    return x\nprint(outer())\n\nWhat is the output and what does nonlocal do?", "inner — nonlocal lets the inner function modify the enclosing (but not global) variable."),
        ("Code:\nimport math\ndef circle_area(r):\n    return math.pi * r ** 2\nprint(round(circle_area(2), 2))\n\nWhat is the output?", "12.57"),
        ("Code:\ndef greet(name):\n    'Returns a greeting for name.'\n    return f'Hi {name}'\nprint(greet.__doc__)\n\nWhat is the output?", "Returns a greeting for name. — accessing a function's docstring."),
        ("Code:\ndef f(a, b, *, c):\n    return a + b + c\nprint(f(1, 2, c=3))\n\nWhat is the output, and what does the * do?", "6 — the bare * forces c to be passed as a keyword-only argument."),
        ("Code:\ndef f(a, /, b):\n    return a + b\nprint(f(1, 2))\n\nWhat does the / do here? (Python 3.8+)", "It marks 'a' as positional-only, meaning it cannot be passed as a keyword argument."),
        ("Code:\ncount = 0\ndef increment():\n    global count\n    count += 1\nfor _ in range(5):\n    increment()\nprint(count)\n\nWhat is the output?", "5"),
        ("Code:\ndef fib(n):\n    if n <= 1:\n        return n\n    return fib(n - 1) + fib(n - 2)\nprint(fib(6))\n\nWhat is the output?", "8 — the recursive Fibonacci sequence at index 6."),
        ("Code:\ndef apply_twice(f, x):\n    return f(f(x))\nprint(apply_twice(lambda x: x + 3, 10))\n\nWhat is the output?", "16 — the function is applied twice: 10+3=13, then 13+3=16."),
        ("How do you define a function in Python?", "Using the def keyword, followed by the function name and parentheses."),
        ("What is a module?", "A Python file containing reusable code such as functions, classes, and variables."),
        ("How do you import a module?", "Using the import statement, e.g. import math."),
        ("Code:\nfrom math import sqrt\nprint(sqrt(16))\n\nWhat is the output and how does this import differ from 'import math'?", "4.0 — this imports sqrt directly, so it's called without the math. prefix."),
        ("Code:\nimport math as m\nprint(m.floor(4.7))\n\nWhat is the output and what does 'as' do?", "4 — 'as' creates an alias, letting you refer to the module by a shorter name."),
        ("What is the difference between a function and a method?", "A method is a function that is defined inside a class and bound to its instances."),
        ("Code:\ndef f(x):\n    return x\nprint(f.__name__)\n\nWhat is the output?", "f — every function object stores its own name."),
        ("Code:\ndef counter():\n    n = 0\n    def increment():\n        nonlocal n\n        n += 1\n        return n\n    return increment\nc = counter()\nprint(c(), c(), c())\n\nWhat is the output?", "1 2 3 — each call to the returned closure remembers and updates its own n."),
        ("Code:\ndef f(a, b, c=3, *args, **kwargs):\n    return (a, b, c, args, kwargs)\nprint(f(1, 2, 4, 5, 6, x=7))\n\nWhat is the output?", "(1, 2, 4, (5, 6), {'x': 7})"),
        ("Code:\nresult = (lambda x, y: x * y)(4, 5)\nprint(result)\n\nWhat is the output?", "20 — an immediately-invoked lambda expression."),
        ("Code:\ndef greet():\n    return 'Hi'\ng = greet\nprint(g())\n\nWhat is the output and what does this show about functions?", "Hi — functions are first-class objects and can be assigned to other names."),
        ("Code:\nfrom functools import reduce\nprint(reduce(lambda a, b: a + b, [1, 2, 3, 4]))\n\nWhat is the output?", "10 — reduce() cumulatively applies the function across the sequence."),
        ("Code:\ndef power(base, exp=2):\n    return base ** exp\nprint(power(3), power(3, 3))\n\nWhat is the output?", "9 27"),
        ("Code:\ndef f():\n    return 1, 2, 3\na, b, c = f()\nprint(a, b, c)\n\nWhat is the output and what is happening?", "1 2 3 — the function returns a tuple, which is then unpacked."),
        ("Code:\ndef validate(age):\n    if age < 0:\n        raise ValueError('Age cannot be negative')\n    return age\nprint(validate(25))\n\nWhat is the output?", "25"),
        ("What is a docstring?", "A string literal placed right after a def/class/module used to document its purpose."),
        ("What is recursion?", "A function that calls itself to break a problem into smaller sub-problems."),
        ("Code:\ndef f(x, y=[]):\n    y.append(x)\n    return y\nprint(f(1))\nprint(f(2, []))\nprint(f(3))\n\nWhat is the output?", "[1]\n[2]\n[1, 3] — the third call reuses the same default list from the first call, not the fresh one passed in the second."),
    ],
    "Error Handling and Exceptions": [
        ("Code:\ntry:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print('cannot divide by zero')\n\nWhat is the output?", "cannot divide by zero"),
        ("Code:\ntry:\n    print(int('abc'))\nexcept ValueError:\n    print('invalid literal')\n\nWhat is the output?", "invalid literal"),
        ("Code:\ntry:\n    print(1 + 1)\nfinally:\n    print('always runs')\n\nWhat is the output?", "2\nalways runs"),
        ("Code:\ntry:\n    x = [1, 2][5]\nexcept IndexError as e:\n    print(f'Error: {e}')\n\nWhat is the output?", "Error: list index out of range"),
        ("Code:\ntry:\n    d = {'a': 1}\n    print(d['b'])\nexcept KeyError:\n    print('key not found')\n\nWhat is the output?", "key not found"),
        ("Code:\ntry:\n    print(1)\nexcept Exception:\n    print('error')\nelse:\n    print('no error')\n\nWhat is the output?", "1\nno error — the else clause runs only when no exception occurred."),
        ("Code:\ndef check(age):\n    if age < 0:\n        raise ValueError('negative age')\n    return age\ntry:\n    check(-5)\nexcept ValueError as e:\n    print(e)\n\nWhat is the output?", "negative age"),
        ("Code:\ntry:\n    print('x' + 5)\nexcept TypeError:\n    print('type mismatch')\n\nWhat is the output?", "type mismatch"),
        ("Code:\ntry:\n    raise ValueError('custom message')\nexcept (TypeError, ValueError) as e:\n    print(f'caught: {e}')\n\nWhat is the output?", "caught: custom message"),
        ("Code:\nclass MyError(Exception):\n    pass\ntry:\n    raise MyError('something broke')\nexcept MyError as e:\n    print(e)\n\nWhat is the output?", "something broke — a custom exception derived from Exception."),
        ("Code:\ntry:\n    print(undefined_var)\nexcept NameError:\n    print('name not found')\n\nWhat is the output?", "name not found"),
        ("Code:\ntry:\n    print(1)\nexcept Exception:\n    print('error')\nfinally:\n    print('cleanup')\n\nWhat is the output?", "1\ncleanup — finally always runs, but the except is skipped since there's no error."),
        ("Code:\ntry:\n    x = 10 / 0\nexcept ZeroDivisionError:\n    print('caught')\nfinally:\n    print('done')\n\nWhat is the output?", "caught\ndone — both the except and finally blocks run."),
        ("Code:\ntry:\n    try:\n        1 / 0\n    except ValueError:\n        print('inner')\nexcept ZeroDivisionError:\n    print('outer')\n\nWhat is the output and why?", "outer — the inner except doesn't match ZeroDivisionError, so it propagates to the outer handler."),
        ("Code:\ndef f():\n    try:\n        return 1\n    finally:\n        print('cleanup')\nprint(f())\n\nWhat is the output?", "cleanup\n1 — finally runs even when a return statement is executing."),
        ("What does the finally block do?", "Runs cleanup code that always executes, whether or not an exception occurred."),
        ("What does the else clause of a try block do?", "Runs only if the try block completed without raising an exception."),
        ("How do you raise an exception manually?", "Using the raise keyword, e.g. raise ValueError('message')."),
        ("What is a custom exception?", "A user-defined exception class that inherits from Exception."),
        ("What is the base class for almost all exceptions?", "The Exception class (which itself inherits from BaseException)."),
        ("Code:\ntry:\n    print(1 / 0)\nexcept Exception as e:\n    print(type(e).__name__)\n\nWhat is the output?", "ZeroDivisionError — Exception catches it, and type(e).__name__ reveals the specific class."),
        ("Code:\ntry:\n    raise Exception('boom')\nexcept Exception:\n    raise\n\nWhat happens?", "The exception is re-raised after the except block, propagating with its original traceback."),
        ("Code:\ntry:\n    x = int('5')\nexcept ValueError:\n    x = 0\nprint(x)\n\nWhat is the output?", "5 — no exception occurs since '5' converts cleanly."),
        ("Code:\ntry:\n    assert 2 > 3\nexcept AssertionError:\n    print('assertion failed')\n\nWhat is the output?", "assertion failed"),
        ("What exception is raised by dividing by zero?", "ZeroDivisionError."),
        ("What exception is raised when using an undefined variable?", "NameError."),
        ("What exception occurs from an invalid type operation?", "TypeError."),
        ("What exception occurs when a dictionary key isn't found?", "KeyError."),
        ("What exception occurs with an out-of-range list index?", "IndexError."),
        ("How do you catch multiple exception types in one except block?", "By listing them in a tuple, e.g. except (TypeError, ValueError):"),
        ("Code:\ntry:\n    open('nonexistent_file.txt')\nexcept FileNotFoundError:\n    print('file missing')\n\nWhat is the output?", "file missing"),
        ("Code:\nclass InsufficientFundsError(Exception):\n    def __init__(self, balance):\n        super().__init__(f'Balance too low: {balance}')\n        self.balance = balance\ntry:\n    raise InsufficientFundsError(10)\nexcept InsufficientFundsError as e:\n    print(e)\n\nWhat is the output?", "Balance too low: 10"),
        ("Code:\ndef divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return float('inf')\nprint(divide(5, 0))\n\nWhat is the output?", "inf"),
        ("Code:\ntry:\n    x = [1, 2, 3]\n    x.remove(10)\nexcept ValueError:\n    print('value not in list')\n\nWhat is the output?", "value not in list"),
        ("Code:\ntry:\n    print('start')\n    raise RuntimeError('oops')\n    print('never reached')\nexcept RuntimeError as e:\n    print(f'caught: {e}')\n\nWhat is the output?", "start\ncaught: oops"),
        ("Code:\nimport sys\ntry:\n    1 / 0\nexcept ZeroDivisionError:\n    print('handled', file=sys.stderr)\n\nWhere does the output go?", "It's printed to standard error (stderr) instead of standard output, due to the file= argument."),
        ("Code:\ntry:\n    x = 1\nexcept Exception:\n    pass\nelse:\n    raise ValueError('failure in else')\n\nWhat happens?", "ValueError: failure in else is raised, since the else block runs (no exception occurred) and it itself raises."),
        ("Code:\ndef f(x):\n    if not isinstance(x, int):\n        raise TypeError('x must be an int')\n    return x * 2\ntry:\n    f('a')\nexcept TypeError as e:\n    print(e)\n\nWhat is the output?", "x must be an int"),
        ("Code:\ntry:\n    x = 5\n    y = 0\n    print(x / y)\nexcept ZeroDivisionError:\n    print('cannot divide')\nexcept Exception:\n    print('other error')\n\nWhat is the output and why is order important?", "cannot divide — except clauses are checked top to bottom, so more specific exceptions should come first."),
        ("Code:\nclass CustomError(Exception):\n    pass\ndef risky():\n    raise CustomError('custom failure')\ntry:\n    risky()\nexcept CustomError:\n    print('handled custom error')\nexcept Exception:\n    print('handled generic error')\n\nWhat is the output?", "handled custom error"),
        ("Code:\ntry:\n    print(1)\nexcept:\n    print('error')\n\nWhat is a downside of a bare 'except:' like this?", "It catches all exceptions, including system-exiting ones like KeyboardInterrupt, which can hide bugs and make debugging harder."),
        ("Code:\ntry:\n    raise ValueError\nexcept ValueError:\n    print('caught, no message')\n\nWhat is the output?", "caught, no message — raising without an argument is valid, str(e) would just be empty."),
        ("Code:\ndef parse_int(s):\n    try:\n        return int(s)\n    except ValueError:\n        print(f'Could not parse: {s}')\n        return None\nprint(parse_int('42'))\nprint(parse_int('abc'))\n\nWhat is the output?", "42\nCould not parse: abc\nNone"),
        ("Code:\ntry:\n    x = 1\n    raise KeyError('missing')\nexcept LookupError as e:\n    print('caught via LookupError:', e)\n\nWhat is the output and why does this work?", "caught via LookupError: 'missing' — KeyError is a subclass of LookupError, so the broader except still catches it."),
        ("Code:\ntry:\n    with open('missing.txt') as f:\n        data = f.read()\nexcept OSError:\n    print('file operation failed')\n\nWhat is the output and why does OSError catch it?", "file operation failed — FileNotFoundError is a subclass of OSError."),
        ("Code:\ndef f():\n    try:\n        raise ValueError('inner')\n    except ValueError as e:\n        raise RuntimeError('outer') from e\ntry:\n    f()\nexcept RuntimeError as e:\n    print(e)\n\nWhat is the output and what does 'from e' do?", "outer — 'from e' chains the original exception as the cause, preserved in the traceback for debugging."),
        ("Code:\ntry:\n    x = 10\nexcept Exception:\n    print('error')\nelse:\n    print('success')\nfinally:\n    print('cleanup')\n\nWhat is the output?", "success\ncleanup"),
        ("Code:\ndef safe_get(lst, index):\n    try:\n        return lst[index]\n    except IndexError:\n        return None\nprint(safe_get([1, 2, 3], 10))\n\nWhat is the output?", "None"),
        ("Code:\nimport json\ntry:\n    json.loads('{invalid json}')\nexcept json.JSONDecodeError:\n    print('invalid JSON')\n\nWhat is the output?", "invalid JSON"),
        ("Code:\ntry:\n    x = 1 // 0\nexcept ArithmeticError:\n    print('arithmetic error caught')\n\nWhat is the output and why does this work?", "arithmetic error caught — ZeroDivisionError is a subclass of ArithmeticError."),
    ],
    "File I/O and Working with Files": [
        ("Code:\nwith open('notes.txt', 'w') as f:\n    f.write('Hello, file!')\n\nWhat does this do?", "Creates (or overwrites) notes.txt and writes the text 'Hello, file!' into it."),
        ("Code:\nwith open('notes.txt', 'r') as f:\n    content = f.read()\nprint(content)\n\nAssuming notes.txt contains 'Hello, file!', what is the output?", "Hello, file!"),
        ("Why should you use the 'with' statement for files?", "It automatically closes the file for you, even if an exception occurs."),
        ("Code:\nwith open('data.txt', 'w') as f:\n    f.write('line1\\n')\n    f.write('line2\\n')\nwith open('data.txt', 'r') as f:\n    for line in f:\n        print(line.strip())\n\nWhat is the output?", "line1\nline2"),
        ("Code:\nwith open('data.txt', 'a') as f:\n    f.write('line3\\n')\n\nWhat does the 'a' mode do, assuming data.txt already has content?", "It appends the new text to the end of the file, without erasing existing content."),
        ("What's the difference between 'w' and 'a' modes?", "'w' overwrites the file's contents; 'a' appends to the end of the file."),
        ("Code:\nwith open('data.txt', 'r') as f:\n    lines = f.readlines()\nprint(lines)\n\nAssuming the file has 'a\\nb\\n', what is the output?", "['a\\n', 'b\\n'] — readlines() returns a list of lines, including newline characters."),
        ("Code:\nimport os\nprint(os.path.exists('nonexistent.txt'))\n\nWhat is the output?", "False"),
        ("Code:\nfrom pathlib import Path\np = Path('example.txt')\nprint(p.exists())\n\nWhat does this check?", "Whether the file example.txt exists, using pathlib's object-oriented path handling."),
        ("Code:\ntry:\n    with open('missing.txt') as f:\n        pass\nexcept FileNotFoundError:\n    print('file not found')\n\nWhat is the output?", "file not found"),
        ("Code:\nimport json\ndata = {'name': 'Ann', 'age': 25}\nwith open('data.json', 'w') as f:\n    json.dump(data, f)\n\nWhat does this do?", "Serializes the dict to JSON text and writes it to data.json."),
        ("Code:\nimport json\nwith open('data.json', 'r') as f:\n    data = json.load(f)\nprint(data['name'])\n\nAssuming data.json contains {'name': 'Ann', 'age': 25}, what is the output?", "Ann"),
        ("What is the difference between text mode and binary mode?", "Text mode handles strings with an encoding; binary mode ('b') handles raw bytes."),
        ("Code:\nwith open('image.png', 'rb') as f:\n    data = f.read()\nprint(type(data))\n\nWhat is the output?", "<class 'bytes'> — binary mode returns raw bytes instead of a decoded string."),
        ("Code:\nwith open('numbers.txt', 'w') as f:\n    for i in range(3):\n        f.write(f'{i}\\n')\n\nWhat does numbers.txt contain afterward?", "'0\\n1\\n2\\n' — three lines with the numbers 0 through 2."),
        ("What module offers a modern, object-oriented way to work with paths?", "The pathlib module."),
        ("Code:\nfrom pathlib import Path\np = Path('folder') / 'file.txt'\nprint(p)\n\nWhat is the output?", "folder/file.txt — the / operator joins path components in pathlib."),
        ("What exception is raised if a file can't be found?", "FileNotFoundError."),
        ("Code:\nwith open('a.txt', 'w') as f1, open('b.txt', 'w') as f2:\n    f1.write('one')\n    f2.write('two')\n\nWhat does this do?", "Opens two files simultaneously using a single with statement and writes to each."),
        ("Code:\nimport csv\nwith open('data.csv', 'w', newline='') as f:\n    writer = csv.writer(f)\n    writer.writerow(['name', 'age'])\n    writer.writerow(['Sam', 30])\n\nWhat does data.csv contain afterward?", "'name,age\\r\\nSam,30\\r\\n' — a CSV file with a header row and one data row."),
        ("Code:\nimport csv\nwith open('data.csv', 'r') as f:\n    reader = csv.reader(f)\n    for row in reader:\n        print(row)\n\nAssuming data.csv has 'name,age\\nSam,30\\n', what is the output?", "['name', 'age']\n['Sam', '30'] — each row is read as a list of strings."),
        ("Code:\nwith open('log.txt', 'w') as f:\n    print('hello', file=f)\n\nWhat does this do?", "Writes 'hello\\n' into log.txt, since print() can redirect its output to any file-like object."),
        ("Code:\nimport os\nfor filename in os.listdir('.'):\n    print(filename)\n\nWhat does this do?", "Prints the names of all files and folders in the current directory."),
        ("Code:\nfrom pathlib import Path\nfor file in Path('.').glob('*.txt'):\n    print(file)\n\nWhat does this do?", "Prints all files in the current directory matching the pattern *.txt."),
        ("Code:\nwith open('empty_check.txt', 'w') as f:\n    pass\nimport os\nprint(os.path.getsize('empty_check.txt'))\n\nWhat is the output?", "0 — the file was created but nothing was written to it."),
        ("Code:\nwith open('data.txt', 'r') as f:\n    first_line = f.readline()\nprint(first_line)\n\nAssuming data.txt has 'first\\nsecond\\n', what is the output?", "first (with a trailing newline) — readline() reads only one line at a time."),
        ("What is the difference between file.read() and file.readlines()?", "read() returns the entire file as one string; readlines() returns a list where each element is one line."),
        ("Code:\nwith open('data.txt', 'r', encoding='utf-8') as f:\n    content = f.read()\n\nWhat does the encoding='utf-8' argument do?", "Explicitly specifies the text encoding used to decode the file's bytes into a string."),
        ("Code:\nimport os\nos.remove('temp.txt')\n\nWhat does this do, and what happens if temp.txt doesn't exist?", "Deletes the file temp.txt; if it doesn't exist, a FileNotFoundError is raised."),
        ("Code:\nimport os\nos.rename('old.txt', 'new.txt')\n\nWhat does this do?", "Renames (or moves) old.txt to new.txt."),
        ("Code:\nimport os\nos.makedirs('a/b/c', exist_ok=True)\n\nWhat does this do?", "Creates the nested directories a/b/c, and exist_ok=True prevents an error if they already exist."),
        ("Code:\nwith open('data.txt') as f:\n    print(f.tell())\n\nWhat does f.tell() return right after opening the file?", "0 — the current position of the file cursor, which starts at the beginning."),
        ("Code:\nwith open('data.txt') as f:\n    f.seek(5)\n    print(f.read())\n\nWhat does f.seek(5) do?", "Moves the file cursor to byte offset 5, so reading starts from that position."),
        ("Code:\nlines = ['a', 'b', 'c']\nwith open('out.txt', 'w') as f:\n    f.writelines(line + '\\n' for line in lines)\n\nWhat does writelines() do here?", "Writes each string from the iterable directly to the file, without adding separators automatically (so newlines must be included manually)."),
        ("Code:\nimport shutil\nshutil.copy('source.txt', 'destination.txt')\n\nWhat does this do?", "Copies the contents of source.txt into a new (or existing) file named destination.txt."),
        ("Code:\nimport os\nprint(os.path.isfile('data.txt'), os.path.isdir('data.txt'))\n\nWhat do these check?", "Whether the given path is a regular file, and whether it's a directory, respectively."),
        ("Code:\nfrom pathlib import Path\np = Path('report.pdf')\nprint(p.suffix, p.stem)\n\nWhat is the output?", ".pdf report — suffix gives the extension, stem gives the filename without it."),
        ("How do you check whether a file exists?", "Using os.path.exists(), or Path.exists() from the pathlib module."),
        ("Code:\nwith open('nums.txt', 'w') as f:\n    f.write('1,2,3')\nwith open('nums.txt') as f:\n    nums = [int(n) for n in f.read().split(',')]\nprint(nums)\n\nWhat is the output?", "[1, 2, 3]"),
        ("Code:\nimport tempfile\nwith tempfile.NamedTemporaryFile(mode='w', delete=False) as f:\n    f.write('temp data')\n    print(f.name)\n\nWhat does this do?", "Creates a temporary file on disk, writes to it, and prints its generated filename."),
        ("How do you open a file in Python?", "Using the built-in open() function."),
        ("What are the common file modes?", "'r' (read), 'w' (write), 'a' (append), 'r+' (read/write); add 'b' for binary."),
        ("Code:\nwith open('a.txt', 'w') as f:\n    f.write('hello')\nf.write('world')\n\nWhat happens on the second write, and why?", "ValueError: I/O operation on closed file — the file was already closed when the with block ended."),
        ("Code:\nimport os\nprint(os.path.abspath('data.txt'))\n\nWhat does this print?", "The full absolute filesystem path to data.txt, based on the current working directory."),
        ("Code:\nwith open('log.txt', 'a') as f:\n    for i in range(3):\n        f.write(f'entry {i}\\n')\n\nWhat does this do if log.txt already has 2 lines?", "Adds three new lines ('entry 0', 'entry 1', 'entry 2') after the existing content, without deleting it."),
        ("Code:\nimport csv\nwith open('data.csv') as f:\n    reader = csv.DictReader(f)\n    for row in reader:\n        print(row['name'])\n\nAssuming a header row 'name,age' and data 'Sam,30', what is the output?", "Sam — DictReader maps each row to a dict keyed by the header."),
        ("How do you read/write JSON data to a file?", "Using the json module's json.load() and json.dump() functions."),
        ("How do you read a file line by line?", "Using file.readlines(), or by iterating over the file object directly."),
        ("How do you write text to a file?", "Using file.write() after opening the file in write ('w') or append ('a') mode."),
        ("Code:\nimport json\nwith open('config.json', 'w') as f:\n    json.dump({'debug': True}, f, indent=2)\n\nWhat does the indent=2 argument do?", "Pretty-prints the JSON output with 2-space indentation, making it more human-readable."),
    ],
    "Object Oriented Programming (OOP)": [
        ("Code:\nclass Dog:\n    def __init__(self, name):\n        self.name = name\nd = Dog('Rex')\nprint(d.name)\n\nWhat is the output?", "Rex"),
        ("Code:\nclass Dog:\n    def bark(self):\n        return 'Woof!'\nd = Dog()\nprint(d.bark())\n\nWhat is the output?", "Woof!"),
        ("What does 'self' refer to?", "The current instance of the class, used to access its own attributes and methods."),
        ("Code:\nclass Animal:\n    def speak(self):\n        return '...'\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof!'\nd = Dog()\nprint(d.speak())\n\nWhat is the output and what concept is this?", "Woof! — this is method overriding, where the subclass replaces the parent's implementation."),
        ("Code:\nclass Animal:\n    def __init__(self, name):\n        self.name = name\nclass Dog(Animal):\n    def __init__(self, name, breed):\n        super().__init__(name)\n        self.breed = breed\nd = Dog('Rex', 'Labrador')\nprint(d.name, d.breed)\n\nWhat is the output?", "Rex Labrador — super() calls the parent class's __init__."),
        ("Code:\nclass Counter:\n    count = 0\n    def __init__(self):\n        Counter.count += 1\nc1 = Counter()\nc2 = Counter()\nprint(Counter.count)\n\nWhat is the output and why?", "2 — count is a class attribute shared across all instances."),
        ("Code:\nclass Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __str__(self):\n        return f'({self.x}, {self.y})'\np = Point(1, 2)\nprint(p)\n\nWhat is the output and what triggers it?", "(1, 2) — print() calls __str__ automatically to get a readable string representation."),
        ("Code:\nclass Animal:\n    def speak(self):\n        raise NotImplementedError\nclass Cat(Animal):\n    def speak(self):\n        return 'Meow'\nfor a in [Cat()]:\n    print(a.speak())\n\nWhat is the output and what OOP concept does the loop illustrate?", "Meow — this shows polymorphism: different subclasses can be used interchangeably through a common interface."),
        ("Code:\nclass BankAccount:\n    def __init__(self, balance):\n        self._balance = balance\n    def deposit(self, amount):\n        self._balance += amount\n    def get_balance(self):\n        return self._balance\nacc = BankAccount(100)\nacc.deposit(50)\nprint(acc.get_balance())\n\nWhat is the output?", "150"),
        ("Code:\nclass Shape:\n    def area(self):\n        return 0\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n    def area(self):\n        return self.side ** 2\ns = Square(4)\nprint(s.area())\n\nWhat is the output?", "16"),
        ("What is a class?", "A blueprint for creating objects, defining their attributes and behaviors."),
        ("What is an object?", "An instance of a class."),
        ("What is the __init__ method?", "A constructor method that runs automatically when a new object is created."),
        ("What is inheritance?", "A mechanism where a class derives attributes and behaviors from a parent class."),
        ("What is polymorphism?", "The ability for objects of different classes to be used through a common interface, often via overridden methods."),
        ("What is encapsulation?", "Bundling data and methods together while restricting direct access to some internal details."),
        ("What does super() do?", "Gives access to methods and properties of a parent class from within a child class."),
        ("What's the difference between a class attribute and an instance attribute?", "Class attributes are shared by all instances; instance attributes are unique to each object."),
        ("What is abstraction?", "Hiding complex implementation details and exposing only what's necessary through a simple interface."),
        ("What are dunder (magic) methods?", "Special methods like __str__ or __len__ that let objects work with Python's built-in syntax and functions."),
        ("Code:\nclass Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n    def __repr__(self):\n        return f'Vector({self.x}, {self.y})'\nv = Vector(1, 2) + Vector(3, 4)\nprint(v)\n\nWhat is the output and what does __add__ enable?", "Vector(4, 6) — __add__ lets custom objects support the + operator."),
        ("Code:\nclass Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    def __eq__(self, other):\n        return self.age == other.age\np1 = Person('A', 30)\np2 = Person('B', 30)\nprint(p1 == p2)\n\nWhat is the output and what does __eq__ control?", "True — __eq__ defines what the == operator does for instances of this class."),
        ("Code:\nclass Box:\n    def __init__(self, items):\n        self.items = items\n    def __len__(self):\n        return len(self.items)\nb = Box([1, 2, 3])\nprint(len(b))\n\nWhat is the output and how does len() work here?", "3 — len() calls the object's __len__ method internally."),
        ("Code:\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    def __repr__(self):\n        return f'Animal({self.name!r})'\na = Animal('Rex')\nprint(a)\n\nWhat is the output and how does __repr__ differ from __str__?", "Animal('Rex') — __repr__ provides an unambiguous, developer-facing representation, used when __str__ isn't defined."),
        ("Code:\nclass Base:\n    def greet(self):\n        return 'Hi from Base'\nclass Mid(Base):\n    pass\nclass Child(Mid):\n    pass\nc = Child()\nprint(c.greet())\n\nWhat is the output and what does this show about multi-level inheritance?", "Hi from Base — methods are inherited through multiple levels of the class hierarchy."),
        ("Code:\nclass Employee:\n    def __init__(self, name, salary):\n        self.name = name\n        self.__salary = salary\n    def get_salary(self):\n        return self.__salary\ne = Employee('Tom', 50000)\nprint(e.get_salary())\nprint(e.__salary)\n\nWhat happens on the last line and why?", "AttributeError — the double-underscore prefix triggers name mangling, making __salary effectively private and inaccessible directly."),
        ("Code:\nclass Shape:\n    def area(self):\n        raise NotImplementedError('Subclasses must implement area()')\ns = Shape()\ns.area()\n\nWhat happens?", "NotImplementedError is raised, since Shape is meant to act as an abstract base and defines no real implementation."),
        ("Code:\nfrom abc import ABC, abstractmethod\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass\ns = Shape()\n\nWhat happens and why?", "TypeError: Can't instantiate abstract class Shape — ABC with an abstractmethod prevents direct instantiation."),
        ("Code:\nclass Counter:\n    def __init__(self):\n        self.count = 0\n    def increment(self):\n        self.count += 1\n        return self\nc = Counter()\nc.increment().increment().increment()\nprint(c.count)\n\nWhat is the output and what pattern enables the chained calls?", "3 — method chaining, enabled by returning self from each method."),
        ("Code:\nclass Temperature:\n    def __init__(self, celsius):\n        self._celsius = celsius\n    @property\n    def fahrenheit(self):\n        return self._celsius * 9/5 + 32\nt = Temperature(20)\nprint(t.fahrenheit)\n\nWhat is the output and what does @property do?", "68.0 — @property lets a method be accessed like an attribute, without parentheses."),
        ("Code:\nclass Circle:\n    def __init__(self, radius):\n        self._radius = radius\n    @property\n    def radius(self):\n        return self._radius\n    @radius.setter\n    def radius(self, value):\n        if value < 0:\n            raise ValueError('radius cannot be negative')\n        self._radius = value\nc = Circle(5)\nc.radius = 10\nprint(c.radius)\n\nWhat is the output?", "10 — the setter validates and updates the underlying _radius attribute."),
        ("Code:\nclass MathUtils:\n    @staticmethod\n    def add(a, b):\n        return a + b\nprint(MathUtils.add(3, 4))\n\nWhat is the output and what does @staticmethod mean?", "7 — a static method doesn't receive self or cls, behaving like a plain function namespaced under the class."),
        ("Code:\nclass Dog:\n    species = 'Canis familiaris'\n    @classmethod\n    def get_species(cls):\n        return cls.species\nprint(Dog.get_species())\n\nWhat is the output and what does @classmethod provide?", "Canis familiaris — a class method receives the class itself (cls) rather than an instance."),
        ("Code:\nclass A:\n    def hello(self):\n        return 'A'\nclass B:\n    def hello(self):\n        return 'B'\nclass C(A, B):\n    pass\nprint(C().hello())\n\nWhat is the output and what concept determines it?", "A — Python's Method Resolution Order (MRO) checks A before B in this multiple-inheritance case."),
        ("Code:\nclass Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)\n    def pop(self):\n        return self.items.pop()\n    def __bool__(self):\n        return len(self.items) > 0\ns = Stack()\nprint(bool(s))\ns.push(1)\nprint(bool(s))\n\nWhat is the output and how does __bool__ work?", "False\nTrue — __bool__ defines how the object behaves in boolean contexts like bool() or if statements."),
        ("Code:\nclass Node:\n    def __init__(self, value, next=None):\n        self.value = value\n        self.next = next\nn2 = Node(2)\nn1 = Node(1, n2)\nprint(n1.next.value)\n\nWhat is the output and what data structure is being represented?", "2 — this models a singly linked list, where each node references the next."),
        ("Code:\nclass Book:\n    def __init__(self, title):\n        self.title = title\n    def __hash__(self):\n        return hash(self.title)\n    def __eq__(self, other):\n        return self.title == other.title\nbooks = {Book('Dune'), Book('Dune')}\nprint(len(books))\n\nWhat is the output and why?", "1 — with matching __hash__ and __eq__, the set treats two books with the same title as duplicates."),
        ("Code:\nclass Config:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\na = Config()\nb = Config()\nprint(a is b)\n\nWhat is the output and what design pattern is this?", "True — this is the Singleton pattern, ensuring only one instance is ever created."),
        ("Code:\nclass Animal:\n    def __init__(self, name):\n        self.name = name\ndog = Animal('Rex')\nprint(isinstance(dog, Animal))\nprint(isinstance(dog, str))\n\nWhat is the output?", "True\nFalse — isinstance() checks whether an object belongs to a given class (or its subclasses)."),
        ("Code:\nclass Wallet:\n    def __init__(self, balance=0):\n        self.balance = balance\n    def __iadd__(self, amount):\n        self.balance += amount\n        return self\nw = Wallet(100)\nw += 50\nprint(w.balance)\n\nWhat is the output and what does __iadd__ control?", "150 — __iadd__ defines the behavior of the += operator for the class."),
        ("Code:\nclass Grid:\n    def __init__(self, data):\n        self.data = data\n    def __getitem__(self, index):\n        return self.data[index]\ng = Grid([10, 20, 30])\nprint(g[1])\n\nWhat is the output and what does __getitem__ enable?", "20 — __getitem__ lets instances support square-bracket indexing like sequences."),
        ("Code:\nclass Countdown:\n    def __init__(self, start):\n        self.current = start\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.current <= 0:\n            raise StopIteration\n        self.current -= 1\n        return self.current + 1\nfor n in Countdown(3):\n    print(n)\n\nWhat is the output and what makes this class iterable?", "3\n2\n1 — defining __iter__ and __next__ makes the class a working iterator, and StopIteration signals the end."),
        ("Code:\nclass Person:\n    def __init__(self, name):\n        self.name = name\np = Person('Sam')\nprint(hasattr(p, 'name'), hasattr(p, 'age'))\n\nWhat is the output?", "True False — hasattr checks whether an attribute exists on the object."),
        ("Code:\nclass Person:\n    def __init__(self, name):\n        self.name = name\np = Person('Sam')\nsetattr(p, 'age', 30)\nprint(p.age)\n\nWhat is the output and what does setattr do?", "30 — setattr() dynamically adds or updates an attribute on an object."),
        ("Code:\nclass Rectangle:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n    def __lt__(self, other):\n        return (self.w * self.h) < (other.w * other.h)\nr1 = Rectangle(2, 3)\nr2 = Rectangle(4, 5)\nprint(r1 < r2)\n\nWhat is the output and what does __lt__ enable?", "True — __lt__ defines how the < operator compares instances, here based on area."),
        ("Code:\nclass Animal:\n    def __init__(self, name):\n        self.name = name\nclass Dog(Animal):\n    def __init__(self, name, breed):\n        super().__init__(name)\n        self.breed = breed\n    def __str__(self):\n        return f'{self.name} the {self.breed}'\nd = Dog('Rex', 'Lab')\nprint(d)\n\nWhat is the output?", "Rex the Lab"),
        ("Code:\nclass Meeting:\n    def __enter__(self):\n        print('Meeting started')\n        return self\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        print('Meeting ended')\nwith Meeting():\n    print('Discussing agenda')\n\nWhat is the output and what pattern is this?", "Meeting started\nDiscussing agenda\nMeeting ended — this implements the context manager protocol used by the 'with' statement."),
        ("Code:\nclass Product:\n    def __init__(self, price):\n        self.price = price\nproducts = [Product(30), Product(10), Product(20)]\nproducts.sort(key=lambda p: p.price)\nprint([p.price for p in products])\n\nWhat is the output?", "[10, 20, 30] — sort() with a key function orders objects by a derived value."),
        ("Code:\nclass Base:\n    def __init__(self):\n        print('Base init')\nclass Derived(Base):\n    def __init__(self):\n        print('Derived init')\n        super().__init__()\nDerived()\n\nWhat is the output?", "Derived init\nBase init — the derived constructor's print runs first, then it explicitly calls the parent constructor."),
        ("Code:\nclass Logger:\n    logs = []\n    def log(self, msg):\n        Logger.logs.append(msg)\nl1 = Logger()\nl2 = Logger()\nl1.log('first')\nl2.log('second')\nprint(Logger.logs)\n\nWhat is the output and why do both instances share the same list?", "['first', 'second'] — logs is a class attribute (a mutable list), so all instances reference the same underlying object."),
    ],
    "Iterators, Generators, and Advanced Functions": [
        ("What is an iterable?", "Any object capable of returning its members one at a time, such as a list, string, or dict — anything that supports iter()."),
        ("What is an iterator?", "An object with both __iter__ and __next__ methods, which produces values one at a time and remembers its position."),
        ("Code:\nnums = [1, 2, 3]\nit = iter(nums)\nprint(next(it))\nprint(next(it))\n\nWhat is the output?", "1\n2 — each call to next() advances the iterator by one item."),
        ("Code:\nit = iter([1, 2])\nnext(it)\nnext(it)\nnext(it)\n\nWhat happens on the third call?", "StopIteration is raised, since the iterator has no more items to return."),
        ("Code:\nnums = [1, 2, 3]\nprint(hasattr(nums, '__iter__'), hasattr(nums, '__next__'))\n\nWhat is the output and why?", "True False — a list is iterable (has __iter__) but is not itself an iterator (no __next__); iter() must be called on it first."),
        ("What is the difference between an iterable and an iterator?", "An iterable can produce an iterator via iter(); an iterator is the object that actually tracks state and yields values via next()."),
        ("Code:\ndef count_up(n):\n    i = 1\n    while i <= n:\n        yield i\n        i += 1\nfor x in count_up(3):\n    print(x)\n\nWhat is the output?", "1\n2\n3"),
        ("What is a generator function?", "A function containing at least one yield statement, which returns a generator (lazy iterator) instead of executing immediately."),
        ("Code:\ndef gen():\n    yield 1\n    yield 2\ng = gen()\nprint(type(g))\n\nWhat is the output?", "<class 'generator'> — calling a generator function returns a generator object without running the body yet."),
        ("Code:\ndef gen():\n    print('start')\n    yield 1\n    print('middle')\n    yield 2\ng = gen()\nprint('created')\nprint(next(g))\n\nWhat is the output and why doesn't 'start' print immediately?", "created\nstart\n1 — generator bodies only execute up to the next yield when next() is called, not when the generator is created."),
        ("Code:\ndef gen():\n    yield 1\n    yield 2\ng = gen()\nnext(g)\nnext(g)\nnext(g)\n\nWhat happens on the third next() call?", "StopIteration is raised, since the generator function has finished running past its last yield."),
        ("Code:\nsquares = (x ** 2 for x in range(4))\nprint(type(squares))\nprint(list(squares))\n\nWhat is the output?", "<class 'generator'>\n[0, 1, 4, 9] — parentheses create a generator expression, evaluated lazily until consumed."),
        ("Code:\ngen = (x for x in range(3))\nprint(list(gen))\nprint(list(gen))\n\nWhat is the output and why does the second list come back empty?", "[0, 1, 2]\n[] — a generator is exhausted after being fully consumed once; it cannot be restarted or reused."),
        ("What is the main advantage of a generator over building a full list?", "Generators produce values lazily and hold only the current state in memory, avoiding the memory cost of materializing an entire large sequence at once."),
        ("Code:\ndef first_n_squares(n):\n    for i in range(n):\n        yield i ** 2\nprint(sum(first_n_squares(5)))\n\nWhat is the output?", "30 — sum() can consume a generator directly, since it's iterable."),
        ("Code:\ndef gen():\n    for i in range(3):\n        yield i\ng = gen()\nprint(list(g))\n\nWhat is the output?", "[0, 1, 2] — list() drains the generator fully, collecting every yielded value."),
        ("Code:\ndef countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\nfor val in countdown(3):\n    print(val)\n\nWhat is the output?", "3\n2\n1"),
        ("Code:\ndef gen():\n    x = yield 1\n    print('received', x)\n    yield 2\ng = gen()\nprint(next(g))\nprint(g.send('hello'))\n\nWhat is the output and what does send() do?", "1\nreceived hello\n2 — send() resumes the generator, passing a value in as the result of the paused yield expression."),
        ("Code:\ndef inner():\n    yield 1\n    yield 2\ndef outer():\n    yield 0\n    yield from inner()\n    yield 3\nprint(list(outer()))\n\nWhat is the output and what does yield from do?", "[0, 1, 2, 3] — yield from delegates iteration to a sub-generator/iterable, yielding each of its values in turn."),
        ("Code:\ndef gen():\n    try:\n        yield 1\n        yield 2\n    finally:\n        print('cleanup')\ng = gen()\nnext(g)\ng.close()\n\nWhat is the output and what does close() do?", "cleanup — close() raises GeneratorExit inside the generator at its current yield, triggering any finally block before stopping it."),
        ("Code:\nimport itertools\nfor x in itertools.count(5, 2):\n    if x > 10:\n        break\n    print(x)\n\nWhat is the output?", "5\n7\n9 — itertools.count(start, step) produces an infinite arithmetic sequence, so a break is needed to stop it."),
        ("Code:\nimport itertools\nprint(list(itertools.islice(range(100), 3)))\n\nWhat is the output?", "[0, 1, 2] — islice() lazily takes a slice of an iterable without needing it to support indexing."),
        ("Code:\nimport itertools\nprint(list(itertools.chain([1, 2], [3, 4])))\n\nWhat is the output?", "[1, 2, 3, 4] — chain() lazily concatenates multiple iterables into one sequence."),
        ("Code:\nimport itertools\nfor a, b in itertools.zip_longest([1, 2, 3], ['a', 'b'], fillvalue='-'):\n    print(a, b)\n\nWhat is the output?", "1 a\n2 b\n3 - — unlike zip(), zip_longest() continues until the longest iterable is exhausted, filling gaps."),
        ("Code:\nimport itertools\nprint(list(itertools.cycle('AB'))[:5])\n\nWhat would this attempt to do, and why is it dangerous?", "It tries to build an infinite list, since cycle() repeats its input forever — this would hang or exhaust memory; it should instead be paired with islice() or a break in a loop."),
        ("Code:\nimport itertools\nprint(list(itertools.permutations([1, 2, 3], 2)))\n\nWhat is the output?", "[(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)] — all ordered pairs without repeating an element within a pair."),
        ("Code:\nimport itertools\nprint(list(itertools.combinations([1, 2, 3], 2)))\n\nWhat is the output?", "[(1, 2), (1, 3), (2, 3)] — unordered selections, so (2, 1) is not included separately from (1, 2)."),
        ("Code:\nimport itertools\nfor key, group in itertools.groupby([1, 1, 2, 2, 3]):\n    print(key, list(group))\n\nWhat is the output?", "1 [1, 1]\n2 [2, 2]\n3 [3] — groupby() clusters only consecutive equal elements, so the input should usually be sorted first."),
        ("What does the yield keyword do inside a function?", "It pauses the function, returns a value to the caller, and preserves all local state so execution can resume from that point on the next call."),
        ("What does the yield from expression do?", "It delegates to another iterable or generator, yielding each of its values in turn and forwarding sent values/exceptions back and forth."),
        ("Code:\ndef gen():\n    yield 1\n    return 'done'\ng = gen()\nnext(g)\ntry:\n    next(g)\nexcept StopIteration as e:\n    print(e.value)\n\nWhat is the output and how does a generator's return value surface?", "done — a generator's return value is attached to the StopIteration exception raised when it finishes, accessible via .value."),
        ("Code:\nsquares = [x**2 for x in range(5)]\nsquares_gen = (x**2 for x in range(5))\nprint(type(squares), type(squares_gen))\n\nWhat is the output and what's the key difference?", "<class 'list'> <class 'generator'> — the list comprehension builds the whole list immediately, while the generator expression computes values lazily on demand."),
        ("What is a decorator?", "A function that takes another function (or class) and returns a modified or wrapped version of it, typically applied with @ syntax."),
        ("Code:\ndef shout(func):\n    def wrapper(*args, **kwargs):\n        result = func(*args, **kwargs)\n        return result.upper()\n    return wrapper\n\n@shout\ndef greet(name):\n    return f'hello {name}'\n\nprint(greet('sam'))\n\nWhat is the output?", "HELLO SAM — @shout wraps greet so its return value is uppercased before being returned."),
        ("Code:\ndef repeat(times):\n    def decorator(func):\n        def wrapper(*args, **kwargs):\n            for _ in range(times):\n                func(*args, **kwargs)\n        return wrapper\n    return decorator\n\n@repeat(3)\ndef say_hi():\n    print('hi')\n\nsay_hi()\n\nWhat is the output and what pattern is repeat()?", "hi\nhi\nhi — repeat(times) is a decorator factory: a function that returns a decorator configured with an argument."),
        ("Code:\nimport functools\n\ndef logger(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs)\n    return wrapper\n\n@logger\ndef add(a, b):\n    'Adds two numbers.'\n    return a + b\n\nprint(add.__name__, add.__doc__)\n\nWhat is the output and what does functools.wraps do?", "add Adds two numbers. — functools.wraps copies the original function's metadata (name, docstring) onto the wrapper, which would otherwise be lost."),
        ("Code:\ndef trace(func):\n    def wrapper(*args, **kwargs):\n        print(f'Calling {func.__name__}')\n        return func(*args, **kwargs)\n    return wrapper\n\n@trace\ndef add(a, b):\n    return a + b\n\nprint(add(2, 3))\n\nWhat is the output?", "Calling add\n5"),
        ("Code:\ndef double(func):\n    def wrapper(*args, **kwargs):\n        return 2 * func(*args, **kwargs)\n    return wrapper\n\n@double\n@double\ndef value():\n    return 5\n\nprint(value())\n\nWhat is the output and in what order do stacked decorators apply?", "20 — decorators apply bottom-up (closest to the function first), so value() -> 5 -> doubled to 10 -> doubled again to 20."),
        ("Code:\nimport functools\n\n@functools.lru_cache(maxsize=None)\ndef fib(n):\n    if n <= 1:\n        return n\n    return fib(n - 1) + fib(n - 2)\n\nprint(fib(10))\n\nWhat is the output and what does lru_cache do?", "55 — lru_cache memoizes results by argument, so repeated/overlapping recursive calls are looked up instead of recomputed."),
        ("What is a higher-order function?", "A function that takes one or more functions as arguments, returns a function, or both."),
        ("Code:\ndef apply_op(a, b, op):\n    return op(a, b)\nimport operator\nprint(apply_op(4, 2, operator.sub))\n\nWhat is the output and what is the operator module used for here?", "2 — operator.sub is a function version of the - operator, so it's passed in and called just like any other function."),
        ("Code:\nfrom functools import partial\ndef power(base, exp):\n    return base ** exp\nsquare = partial(power, exp=2)\nprint(square(5))\n\nWhat is the output and what does partial do?", "25 — partial pre-fills some arguments of a function, returning a new callable that only needs the rest."),
        ("Code:\nnums = [3, 1, 4, 1, 5]\nprint(sorted(nums, key=lambda x: -x))\n\nWhat is the output and why use a lambda as key here?", "[5, 4, 3, 1, 1] — the key function transforms each element before comparison, so negating produces a descending sort."),
        ("Code:\nwords = ['banana', 'kiwi', 'apple']\nprint(sorted(words, key=len))\n\nWhat is the output?", "['kiwi', 'apple', 'banana'] — sorted by string length rather than alphabetically."),
        ("What is memoization?", "A caching technique that stores the results of expensive function calls and returns the cached result when the same inputs occur again."),
        ("Code:\ndef make_counter():\n    count = 0\n    def counter():\n        nonlocal count\n        count += 1\n        return count\n    return counter\nc1 = make_counter()\nc2 = make_counter()\nprint(c1(), c1(), c2())\n\nWhat is the output and why is c2's count independent of c1's?", "1 2 1 — each call to make_counter() creates a fresh closure with its own separate count variable."),
        ("Code:\ndef gen_pairs():\n    for i in range(3):\n        for j in range(3):\n            yield (i, j)\nprint(len(list(gen_pairs())))\n\nWhat is the output?", "9 — the nested loops yield one tuple per combination of i and j, 3 x 3 total."),
        ("Code:\nclass Repeater:\n    def __init__(self, value, times):\n        self.value = value\n        self.times = times\n    def __iter__(self):\n        for _ in range(self.times):\n            yield self.value\nfor v in Repeater('x', 3):\n    print(v)\n\nWhat is the output and what does using a generator inside __iter__ achieve?", "x\nx\nx — defining __iter__ as a generator function is a concise way to make a custom class iterable, without writing a separate __next__ method."),
        ("Code:\ndef safe_divide_gen(pairs):\n    for a, b in pairs:\n        try:\n            yield a / b\n        except ZeroDivisionError:\n            yield None\nprint(list(safe_divide_gen([(10, 2), (5, 0), (9, 3)])))\n\nWhat is the output?", "[5.0, None, 3.0] — the generator handles the error per-item and keeps yielding instead of stopping the whole iteration."),
        ("Code:\nimport functools\ndef add_logging(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f'args={args}, kwargs={kwargs}')\n        return func(*args, **kwargs)\n    return wrapper\n\n@add_logging\ndef greet(name, greeting='Hi'):\n    return f'{greeting}, {name}'\n\nprint(greet('Sam', greeting='Hello'))\n\nWhat is the output?", "args=('Sam',), kwargs={'greeting': 'Hello'}\nHello, Sam"),
        ("Code:\ndef gen():\n    print('A')\n    yield\n    print('B')\n    yield\n    print('C')\ng = gen()\nfor _ in g:\n    pass\n\nWhat is the output?", "A\nB\nC — a for loop repeatedly calls next() until StopIteration, driving the generator through all its yields."),
    ],
    "Regular Expressions and String Processing": [
        ("What is a regular expression?", "A pattern-matching language used to search, validate, and manipulate text based on defined rules."),
        ("What module provides regular expression support in Python?", "The re module."),
        ("Code:\nimport re\nprint(re.search('cat', 'the cat sat'))\n\nWhat does re.search return here?", "A Match object, since 'cat' is found within the string (its repr shows the match span and text)."),
        ("Code:\nimport re\nprint(re.search('dog', 'the cat sat'))\n\nWhat is the output?", "None — search() returns None when the pattern isn't found anywhere in the string."),
        ("Code:\nimport re\nm = re.search(r'\\d+', 'order 42 shipped')\nprint(m.group())\n\nWhat is the output?", "42 — \\d+ matches one or more digits, and .group() returns the matched text."),
        ("Code:\nimport re\nprint(re.match('cat', 'the cat sat'))\n\nWhat is the output and how does match() differ from search()?", "None — match() only checks for a match at the very start of the string, while search() scans the whole string."),
        ("Code:\nimport re\nprint(re.match('the', 'the cat sat'))\n\nWhat is the output?", "A Match object, since 'the' does appear right at the start of the string."),
        ("Code:\nimport re\nprint(re.findall(r'\\d+', 'a1 b22 c333'))\n\nWhat is the output?", "['1', '22', '333'] — findall() returns every non-overlapping match as a list of strings."),
        ("Code:\nimport re\nfor m in re.finditer(r'\\d+', 'a1 b22'):\n    print(m.group(), m.start())\n\nWhat is the output?", "1 1\n22 4 — finditer() yields Match objects one at a time, each with position info."),
        ("Code:\nimport re\nprint(re.sub(r'\\d+', '#', 'a1 b22 c333'))\n\nWhat is the output?", "a# b# c# — sub() replaces every match of the pattern with the replacement string."),
        ("Code:\nimport re\nprint(re.sub(r'\\d+', '#', 'a1 b22 c333', count=1))\n\nWhat is the output?", "a# b22 c333 — the count argument limits how many matches get replaced."),
        ("Code:\nimport re\nprint(re.split(r'\\s*,\\s*', 'a, b,c ,  d'))\n\nWhat is the output?", "['a', 'b', 'c', 'd'] — split() breaks the string wherever the pattern matches, here a comma with optional surrounding spaces."),
        ("Code:\nimport re\npattern = re.compile(r'\\d+')\nprint(pattern.findall('a1 b22'))\n\nWhat does re.compile() do and what is the output?", "['1', '22'] — compile() pre-builds a reusable pattern object, useful when the same pattern is applied many times."),
        ("Code:\nimport re\nm = re.search(r'(\\w+)@(\\w+)\\.com', 'contact: sam@example.com')\nprint(m.group(1), m.group(2))\n\nWhat is the output?", "sam example — parentheses create capture groups, retrievable individually via .group(n)."),
        ("Code:\nimport re\nm = re.search(r'(?P<user>\\w+)@(?P<domain>\\w+)\\.com', 'sam@example.com')\nprint(m.group('user'), m.group('domain'))\n\nWhat is the output and what does (?P<name>...) do?", "sam example — it creates a named capture group, accessible by name instead of only by position."),
        ("Code:\nimport re\nprint(re.findall(r'a.c', 'abc a1c a\\nc'))\n\nWhat is the output and what does . match?", "['abc', 'a1c'] — . matches any character except a newline by default, so 'a\\nc' is not matched."),
        ("Code:\nimport re\nprint(re.findall(r'colou?r', 'color colour colouur'))\n\nWhat is the output and what does ? mean here?", "['color', 'colour'] — ? makes the preceding character (u) optional, matching zero or one occurrence."),
        ("Code:\nimport re\nprint(re.findall(r'ab*c', 'ac abc abbbc'))\n\nWhat is the output and what does * mean?", "['ac', 'abc', 'abbbc'] — * matches zero or more of the preceding character."),
        ("Code:\nimport re\nprint(re.findall(r'ab+c', 'ac abc abbbc'))\n\nWhat is the output and how does + differ from *?", "['abc', 'abbbc'] — + requires at least one occurrence, so 'ac' (zero b's) doesn't match."),
        ("Code:\nimport re\nprint(re.findall(r'\\bcat\\b', 'cat catalog cat'))\n\nWhat is the output and what does \\b mean?", "['cat', 'cat'] — \\b is a word boundary, so it matches 'cat' as a whole word but not as part of 'catalog'."),
        ("Code:\nimport re\nprint(re.findall(r'^\\d+', '123abc 456'))\n\nWhat is the output and what does ^ mean here?", "['123'] — ^ anchors the match to the start of the string, so only the leading digits are found."),
        ("Code:\nimport re\nprint(re.findall(r'\\d+$', 'abc123'))\n\nWhat is the output and what does $ mean?", "['123'] — $ anchors the match to the end of the string."),
        ("Code:\nimport re\nprint(re.findall(r'[aeiou]', 'hello world'))\n\nWhat is the output and what does [aeiou] represent?", "['e', 'o', 'o'] — square brackets define a character class, matching any single character listed inside."),
        ("Code:\nimport re\nprint(re.findall(r'[^aeiou ]', 'hi there'))\n\nWhat is the output and what does ^ inside brackets mean?", "['h', 't', 'h', 'r'] — inside a character class, ^ negates it, matching any character NOT in the set."),
        ("Code:\nimport re\nprint(re.findall(r'[a-z]+', 'Hello World 123'))\n\nWhat is the output?", "['ello', 'orld'] — [a-z] matches lowercase letters only, so capital letters and digits break the match."),
        ("Code:\nimport re\nprint(re.findall(r'\\w+', \"it's a test-run\"))\n\nWhat is the output and what does \\w match?", "['it', 's', 'a', 'test', 'run'] — \\w matches word characters (letters, digits, underscore), so apostrophes and hyphens split the matches."),
        ("Code:\nimport re\nprint(re.findall(r'\\s+', 'a  b\\tc\\nd'))\n\nWhat is the output and what does \\s match?", "['  ', '\\t', '\\n'] — \\s matches any whitespace character, including spaces, tabs, and newlines."),
        ("Code:\nimport re\nprint(re.findall(r'a{2,4}', 'a aa aaa aaaaa'))\n\nWhat is the output and what does {2,4} mean?", "['aa', 'aaa', 'aaaa'] — {2,4} requires between 2 and 4 repetitions; the run of 5 a's is matched as 4 then leaves 1 unmatched."),
        ("Code:\nimport re\nprint(re.findall(r'<.+>', '<a><b>'))\n\nWhat is the output and why doesn't it just match '<a>' and '<b>' separately?", "['<a><b>'] — by default quantifiers are greedy, so .+ consumes as much as possible while still allowing the overall pattern to match."),
        ("Code:\nimport re\nprint(re.findall(r'<.+?>', '<a><b>'))\n\nWhat is the output and what does the ? after + do?", "['<a>', '<b>'] — appending ? makes the quantifier non-greedy (lazy), matching as little as possible."),
        ("Code:\nimport re\nprint(bool(re.match(r'cat', 'CAT', re.IGNORECASE)))\n\nWhat is the output and what does re.IGNORECASE do?", "True — it makes the match case-insensitive."),
        ("Code:\nimport re\npattern = re.compile(r'''\n    \\d+  # the number\n    [a-z]+  # the unit\n''', re.VERBOSE)\nprint(pattern.findall('10kg 5lb'))\n\nWhat is the output and what does re.VERBOSE enable?", "['10kg', '5lb'] — VERBOSE mode lets you write the pattern across multiple lines with whitespace and comments for readability, both ignored during matching."),
        ("Code:\nimport re\nprint(re.findall(r'foo(?=bar)', 'foobar foobaz'))\n\nWhat is the output and what does (?=...) do?", "['foo'] — this is a positive lookahead: it matches 'foo' only where it's followed by 'bar', without including 'bar' in the match."),
        ("Code:\nimport re\nprint(re.findall(r'foo(?!bar)', 'foobar foobaz'))\n\nWhat is the output and what does (?!...) do?", "['foo'] — this is a negative lookahead: it matches 'foo' only where it's NOT followed by 'bar', so only the 'foobaz' occurrence matches."),
        ("Code:\nimport re\nprint(re.findall(r'(?<=\\$)\\d+', 'price: $50, count: 3'))\n\nWhat is the output and what does (?<=...) do?", "['50'] — this is a positive lookbehind: it matches digits only where preceded by a dollar sign, without including the $ in the result."),
        ("Code:\nimport re\nprint(re.findall(r'cat|dog', 'I have a cat and a dog'))\n\nWhat is the output and what does | mean?", "['cat', 'dog'] — | acts as alternation (OR), matching either pattern on either side."),
        ("Why should regex patterns with backslashes usually be written as raw strings?", "Because raw strings (r'...') prevent Python from interpreting backslash sequences like \\d or \\b as escape codes before re even sees the pattern."),
        ("Code:\nimport re\nprint(re.escape('3.14 (pi)'))\n\nWhat is the output and what does re.escape do?", "3\\.14\\ \\(pi\\) — it escapes all regex-special characters in a string so it can be safely used as a literal pattern."),
        ("Code:\nimport re\nresult = re.sub(r'(\\w+)@(\\w+)', r'\\2 at \\1', 'sam@example')\nprint(result)\n\nWhat is the output and what do \\1 and \\2 refer to in the replacement?", "example at sam — they refer back to the text captured by the first and second groups in the pattern."),
        ("Code:\nimport re\nprint(re.fullmatch(r'\\d{3}-\\d{4}', '123-4567'))\nprint(re.fullmatch(r'\\d{3}-\\d{4}', '123-4567x'))\n\nWhat is the output and how does fullmatch differ from match?", "A Match object, then None — fullmatch() requires the entire string to match the pattern, not just a portion at the start."),
        ("Code:\ns = 'Hello World'\nprint(s.lower())\nprint(s.upper())\n\nWhat is the output?", "hello world\nHELLO WORLD"),
        ("Code:\ns = 'Hello World'\nprint(s.replace('World', 'Python'))\n\nWhat is the output?", "Hello Python — replace() swaps every occurrence of the first substring with the second."),
        ("Code:\nprint('  spaced out  '.strip())\nprint('  spaced out  '.lstrip())\nprint('  spaced out  '.rstrip())\n\nWhat is the output?", "'spaced out'\n'spaced out  '\n'  spaced out' — strip removes both sides, lstrip only the left, rstrip only the right."),
        ("Code:\nprint('a-b-c'.split('-'))\nprint('-'.join(['a', 'b', 'c']))\n\nWhat is the output?", "['a', 'b', 'c']\na-b-c — split() breaks a string apart by a separator, join() does the reverse."),
        ("Code:\nprint('hello'.startswith('he'), 'hello'.endswith('lo'))\n\nWhat is the output?", "True True"),
        ("Code:\nprint('42'.isdigit(), 'abc'.isalpha(), 'abc123'.isalnum())\n\nWhat is the output?", "True True True"),
        ("Code:\nprint('7'.zfill(3))\n\nWhat is the output and what does zfill do?", "007 — zfill pads a numeric string with leading zeros to reach the given width."),
        ("Code:\nprint('7'.rjust(4, '*'))\nprint('7'.ljust(4, '*'))\nprint('7'.center(5, '*'))\n\nWhat is the output?", "***7\n7***\n**7**"),
        ("Code:\ntable = str.maketrans('abc', 'xyz')\nprint('aabbcc'.translate(table))\n\nWhat is the output and what does maketrans/translate do?", "xxyyzz — maketrans builds a character mapping table, and translate() applies it, replacing each mapped character."),
        ("Code:\nprint(' '.join('hello world'.split()))\n\nWhat does this do, and why is it a common idiom for cleaning whitespace?", "It collapses any run of whitespace (including multiple spaces, tabs, newlines) down to single spaces, since split() with no argument splits on any whitespace and discards empty strings."),
    ],
    "Working with External Libraries and APIs": [
        ("What is an API?", "An Application Programming Interface — a defined set of rules that lets one piece of software communicate with another."),
        ("What is a REST API?", "A web API that follows REST principles, using standard HTTP methods (GET, POST, PUT, DELETE) and URLs to operate on resources."),
        ("What third-party library is most commonly used to make HTTP requests in Python?", "The requests library."),
        ("Command: pip install requests\n\nWhat does this do?", "Downloads and installs the requests package from PyPI into the current (virtual) environment."),
        ("Code:\nimport requests\nresponse = requests.get('https://api.example.com/data')\nprint(response.status_code)\n\nWhat does response.status_code represent?", "The HTTP status code returned by the server, e.g. 200 for success or 404 for not found."),
        ("Code:\nimport requests\nresponse = requests.get('https://api.example.com/data')\ndata = response.json()\nprint(type(data))\n\nWhat does response.json() do?", "Parses the response body as JSON and returns it as a Python object (typically a dict or list)."),
        ("What does an HTTP status code in the 200 range generally mean?", "Success — the request was received, understood, and processed correctly."),
        ("What does an HTTP status code in the 400 range generally mean?", "A client error — something about the request itself was invalid, such as bad syntax or missing authentication."),
        ("What does an HTTP status code in the 500 range generally mean?", "A server error — the server failed to fulfill a valid request due to a problem on its end."),
        ("What does HTTP status code 404 mean specifically?", "Not Found — the requested resource doesn't exist at that URL."),
        ("What does HTTP status code 401 mean specifically?", "Unauthorized — the request lacks valid authentication credentials."),
        ("What does HTTP status code 429 mean specifically?", "Too Many Requests — the client has been rate-limited and should slow down or retry later."),
        ("Code:\nimport requests\nresponse = requests.get('https://api.example.com/search', params={'q': 'python', 'limit': 5})\nprint(response.url)\n\nWhat does the params argument do?", "It builds and appends a URL query string from the dict automatically, e.g. ?q=python&limit=5."),
        ("Code:\nimport requests\nresponse = requests.post('https://api.example.com/items', json={'name': 'widget'})\n\nWhat does passing json=... do, as opposed to data=...?", "It serializes the dict to a JSON string, sets the Content-Type header to application/json, and sends it as the request body."),
        ("Code:\nimport requests\nheaders = {'Authorization': 'Bearer abc123'}\nresponse = requests.get('https://api.example.com/me', headers=headers)\n\nWhat is this pattern commonly used for?", "Passing an authentication token (here a Bearer token) so the API can identify and authorize the caller."),
        ("Code:\nimport requests\ntry:\n    response = requests.get('https://api.example.com/data', timeout=5)\nexcept requests.exceptions.Timeout:\n    print('request timed out')\n\nWhat does the timeout argument do?", "It caps how long requests will wait for a response before giving up and raising a Timeout exception, instead of hanging indefinitely."),
        ("Code:\nimport requests\ntry:\n    response = requests.get('https://bad-domain-xyz.invalid')\nexcept requests.exceptions.ConnectionError:\n    print('could not connect')\n\nWhat is the output?", "could not connect — ConnectionError is raised when the network request itself can't reach the server (DNS failure, refused connection, etc.)."),
        ("Code:\nimport requests\nresponse = requests.get('https://api.example.com/missing')\nresponse.raise_for_status()\n\nWhat does raise_for_status() do?", "It raises an HTTPError if the response's status code indicates a client or server error (4xx/5xx); it does nothing for successful responses."),
        ("Code:\nimport requests\nsession = requests.Session()\nsession.headers.update({'Authorization': 'Bearer abc123'})\nr1 = session.get('https://api.example.com/a')\nr2 = session.get('https://api.example.com/b')\n\nWhat is the advantage of using a Session here?", "It reuses the underlying TCP connection and default headers across multiple requests, which is faster and avoids repeating shared setup like auth headers."),
        ("Code:\nimport json\ndata = {'name': 'Ann', 'active': True}\ntext = json.dumps(data)\nprint(text)\n\nWhat is the output?", "'{\"name\": \"Ann\", \"active\": true}' — json.dumps() serializes a Python object into a JSON-formatted string."),
        ("Code:\nimport json\ntext = '{\"name\": \"Ann\", \"age\": 25}'\ndata = json.loads(text)\nprint(data['name'])\n\nWhat is the output?", "Ann — json.loads() parses a JSON string into a Python object."),
        ("Code:\nimport json\ntry:\n    json.loads('{bad json}')\nexcept json.JSONDecodeError as e:\n    print('invalid JSON:', e)\n\nWhat does this demonstrate?", "That malformed JSON text raises a JSONDecodeError when parsed, which should be handled when working with data from external sources like APIs."),
        ("Why shouldn't API keys or secrets be hardcoded directly into source code?", "Because source code is often shared, committed to version control, or exposed publicly, which would leak the credentials; secrets should instead come from environment variables or a secure secrets manager."),
        ("Code:\nimport os\napi_key = os.environ.get('API_KEY')\nif not api_key:\n    raise RuntimeError('API_KEY not set')\n\nWhat does this pattern accomplish?", "It reads a secret from an environment variable at runtime instead of hardcoding it, and fails fast with a clear error if it's missing."),
        ("What is the purpose of a .env file combined with a library like python-dotenv?", "It lets developers define environment variables (like API keys) in a local file that's loaded into the environment at startup, keeping secrets out of source code and version control."),
        ("What does an API rate limit typically restrict?", "The number of requests a client is allowed to make within a given time window, to prevent overload and abuse of the service."),
        ("What is exponential backoff, in the context of retrying failed API requests?", "A retry strategy where the wait time between successive retry attempts increases exponentially, reducing load on a struggling server and avoiding tight retry loops."),
        ("Code:\nimport time\nimport requests\n\ndef get_with_retries(url, retries=3):\n    for attempt in range(retries):\n        try:\n            return requests.get(url, timeout=5)\n        except requests.exceptions.RequestException:\n            if attempt == retries - 1:\n                raise\n            time.sleep(2 ** attempt)\n\nWhat does this function do?", "It retries a failed HTTP request up to a set number of times, waiting progressively longer (1s, 2s, 4s...) between attempts, and re-raises the error if all retries fail."),
        ("What is pagination in the context of a REST API?", "A technique where a large result set is split across multiple requests/pages (often via a page number, offset, or cursor parameter), rather than returned all at once."),
        ("Code:\nimport requests\nurl = 'https://api.example.com/items'\nall_items = []\nwhile url:\n    response = requests.get(url).json()\n    all_items.extend(response['results'])\n    url = response.get('next')\nprint(len(all_items))\n\nWhat pattern does this loop implement?", "Following pagination links: it keeps requesting the 'next' page URL supplied by the API until there are no more pages, accumulating all results."),
        ("What does an HTTP GET request typically do, semantically?", "Retrieves data from the server without modifying it (in a well-designed REST API, GET should be a safe, read-only operation)."),
        ("What does an HTTP POST request typically do, semantically?", "Sends data to the server to create a new resource or trigger an action that changes state."),
        ("What does an HTTP PUT request typically do, semantically?", "Replaces an existing resource entirely with the provided data (or creates it at that URL if it doesn't exist)."),
        ("What does an HTTP PATCH request typically do, semantically?", "Applies a partial update to an existing resource, changing only the specified fields."),
        ("What does an HTTP DELETE request typically do, semantically?", "Removes the specified resource from the server."),
        ("What is a webhook?", "A way for one service to notify another automatically by sending an HTTP request to a pre-configured URL when a specific event occurs, instead of the receiver having to poll for updates."),
        ("What is API authentication typically used for?", "To verify the identity of the caller and determine what data or actions they're allowed to access."),
        ("What is an API key?", "A unique token issued to a client that identifies and authorizes it when calling an API, usually sent as a header or query parameter."),
        ("What is OAuth, at a high level?", "An authorization framework that lets a user grant a third-party application limited access to their resources on another service, without sharing their password directly."),
        ("Code:\nimport requests\nresponse = requests.get('https://api.example.com/data')\nprint(response.headers['Content-Type'])\n\nWhat does response.headers contain?", "The HTTP response headers sent back by the server, such as Content-Type, as a dict-like object."),
        ("Code:\nimport requests\nresponse = requests.get('https://api.example.com/download')\nwith open('file.zip', 'wb') as f:\n    f.write(response.content)\n\nWhat does response.content contain, and why write in binary mode?", "The raw response body as bytes; binary mode ('wb') is used because the downloaded content (like a zip file) isn't text and shouldn't be decoded or have newlines translated."),
        ("What does it mean for an API to be 'idempotent' for a given method?", "Making the same request multiple times has the same effect as making it once — e.g., PUT and DELETE are expected to be idempotent, while POST typically isn't."),
        ("What is the purpose of a client library / SDK provided by an API vendor?", "It wraps the raw HTTP calls, authentication, and response parsing into convenient functions/classes, so developers don't have to build those requests by hand."),
        ("Code:\nfrom unittest.mock import patch\nimport requests\n\ndef fetch_status():\n    return requests.get('https://api.example.com').status_code\n\nwith patch('requests.get') as mock_get:\n    mock_get.return_value.status_code = 200\n    print(fetch_status())\n\nWhat is the output and why is mocking used here?", "200 — patch() replaces requests.get with a mock during the test, so the test doesn't depend on a real network call and can control the exact response it simulates."),
        ("What is a common reason to catch requests.exceptions.RequestException broadly rather than only specific subclasses?", "It's the base class for all of requests' network-related errors (Timeout, ConnectionError, HTTPError, etc.), so catching it provides a single fallback for 'something went wrong on the network side'."),
        ("Code:\nimport requests\nresponse = requests.get('https://api.example.com/user/1')\nuser = response.json()\nprint(user.get('email', 'no email on file'))\n\nWhy use .get() with a default here instead of user['email']?", "Because API response fields aren't always guaranteed to be present; .get() avoids a KeyError and provides a sensible fallback if 'email' is missing."),
        ("What is the difference between synchronous and asynchronous API calls, at a high level?", "A synchronous call blocks the program until the response arrives; an asynchronous call lets the program continue doing other work while waiting for the response."),
        ("What does 'CORS' stand for and what problem does it address?", "Cross-Origin Resource Sharing — a browser security mechanism that controls whether a web page from one origin is allowed to make requests to a server on a different origin."),
        ("Why is it good practice to check response.status_code (or use raise_for_status()) before trying to parse response.json()?", "Because an error response (like a 404 or 500 page) often isn't valid JSON, or contains an error payload rather than the expected data, so parsing it as if it succeeded can cause confusing failures."),
        ("What is versioning in the context of an API (e.g. /v1/, /v2/ in a URL)?", "A way of marking which version of an API's contract a client is using, so the provider can introduce breaking changes in a new version without breaking existing clients on the old one."),
    ],
    "Concurrency and Parallelism": [
        ("What is concurrency?", "The ability of a program to make progress on multiple tasks by interleaving their execution, without necessarily running them at the exact same instant."),
        ("What is parallelism?", "Running multiple tasks literally at the same time, typically by using multiple CPU cores."),
        ("What is the GIL (Global Interpreter Lock)?", "A lock in CPython that allows only one thread to execute Python bytecode at a time, even on multi-core machines."),
        ("Why doesn't Python threading speed up CPU-bound work in CPython?", "Because the GIL prevents more than one thread from executing Python bytecode simultaneously, so CPU-bound threads end up taking turns rather than running in true parallel."),
        ("Why can Python threading still speed up I/O-bound work despite the GIL?", "Because the GIL is released while a thread waits on I/O (like a network request or disk read), letting other threads run during that wait."),
        ("Code:\nimport threading\n\ndef greet():\n    print('hello from thread')\n\nt = threading.Thread(target=greet)\nt.start()\nt.join()\n\nWhat does t.start() do, and what does t.join() do?", "start() begins running the thread's target function concurrently; join() blocks the calling code until that thread finishes."),
        ("Code:\nimport threading\n\ndef worker(n):\n    print(f'worker {n}')\n\nthreads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]\nfor t in threads:\n    t.start()\nfor t in threads:\n    t.join()\nprint('all done')\n\nWhat is guaranteed about the output order?", "'all done' is guaranteed to print last, but the order of the three 'worker N' lines is not guaranteed, since the threads run concurrently and can be scheduled in any order."),
        ("Code:\nimport threading\ncounter = 0\ndef increment():\n    global counter\n    for _ in range(100000):\n        counter += 1\nthreads = [threading.Thread(target=increment) for _ in range(2)]\nfor t in threads:\n    t.start()\nfor t in threads:\n    t.join()\nprint(counter)\n\nWhy might the output be less than 200000?", "This is a race condition: counter += 1 isn't atomic, so two threads can read the same value before either writes back its increment, silently losing updates."),
        ("What is a race condition?", "A bug where the correctness of a program depends on the unpredictable timing or interleaving of concurrent operations, often leading to inconsistent results."),
        ("Code:\nimport threading\ncounter = 0\nlock = threading.Lock()\ndef increment():\n    global counter\n    for _ in range(100000):\n        with lock:\n            counter += 1\nthreads = [threading.Thread(target=increment) for _ in range(2)]\nfor t in threads:\n    t.start()\nfor t in threads:\n    t.join()\nprint(counter)\n\nWhat is the output, and how does the Lock fix the earlier race condition?", "200000 — the lock ensures only one thread can execute the increment at a time, making the read-modify-write operation effectively atomic."),
        ("What does threading.Lock() provide?", "A mutual-exclusion primitive that only one thread can hold at a time, used to protect shared data from concurrent access."),
        ("Code:\nimport threading\nlock = threading.Lock()\nlock.acquire()\nlock.acquire()\n\nWhat happens on the second acquire() call, and what's the fix?", "The thread deadlocks, blocking forever since a plain Lock can't be acquired twice by the same thread; a threading.RLock (reentrant lock) allows the same thread to acquire it multiple times."),
        ("What is a deadlock?", "A situation where two or more threads/processes are each waiting on a resource the other holds, so none of them can ever proceed."),
        ("What does threading.Event provide?", "A simple flag object that one thread can set() and others can wait() on, useful for signaling between threads."),
        ("What does threading.Semaphore control?", "It limits how many threads can access a resource concurrently, by maintaining an internal counter that's decremented on acquire and incremented on release."),
        ("What is a daemon thread?", "A background thread that doesn't prevent the program from exiting; when only daemon threads remain, the interpreter exits without waiting for them to finish."),
        ("Code:\nimport threading\nt = threading.Thread(target=lambda: None, daemon=True)\n\nWhat does setting daemon=True change about this thread?", "It marks the thread as a daemon, so the main program can exit even if this thread is still running, instead of waiting for it to finish."),
        ("What is the multiprocessing module used for?", "Running separate Python processes (each with its own interpreter and memory space) to achieve true parallelism, bypassing the GIL."),
        ("Code:\nimport multiprocessing\n\ndef square(n):\n    return n * n\n\nif __name__ == '__main__':\n    with multiprocessing.Pool(4) as pool:\n        print(pool.map(square, [1, 2, 3, 4]))\n\nWhat is the output, and what does Pool.map do?", "[1, 4, 9, 16] — it distributes the input items across worker processes, applies the function to each in parallel, and collects the results in order."),
        ("Why does multiprocessing avoid the GIL limitation that threading has?", "Because each process gets its own separate Python interpreter and memory space (and thus its own GIL), so multiple processes can run Python bytecode truly in parallel across CPU cores."),
        ("Why is if __name__ == '__main__': commonly required around multiprocessing code on some platforms?", "Because starting a new process may re-import the main module; without the guard, that re-import would recursively spawn more processes."),
        ("Code:\nimport multiprocessing\n\ndef worker(q):\n    q.put('result from process')\n\nif __name__ == '__main__':\n    q = multiprocessing.Queue()\n    p = multiprocessing.Process(target=worker, args=(q,))\n    p.start()\n    print(q.get())\n    p.join()\n\nWhat is the output, and why use a multiprocessing.Queue instead of a regular list here?", "result from process — separate processes don't share memory, so a regular list can't be used to pass data between them; multiprocessing.Queue is built specifically for safe inter-process communication."),
        ("What is the key practical difference between threading and multiprocessing for CPU-bound work in Python?", "Multiprocessing can achieve real parallel speedup on CPU-bound work by using multiple cores, while threading generally cannot, due to the GIL."),
        ("What is the key practical difference between threading and multiprocessing for I/O-bound work in Python?", "Threading is usually preferred for I/O-bound work since it's lighter-weight than spawning separate processes, and the GIL is released during I/O waits anyway."),
        ("Code:\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef square(n):\n    return n * n\n\nwith ThreadPoolExecutor(max_workers=3) as executor:\n    results = list(executor.map(square, [1, 2, 3, 4]))\nprint(results)\n\nWhat is the output?", "[1, 4, 9, 16] — ThreadPoolExecutor.map() runs the function across a pool of worker threads and returns results in the original input order."),
        ("Code:\nfrom concurrent.futures import ProcessPoolExecutor\n\ndef square(n):\n    return n * n\n\nif __name__ == '__main__':\n    with ProcessPoolExecutor() as executor:\n        results = list(executor.map(square, [1, 2, 3, 4]))\n    print(results)\n\nWhen would ProcessPoolExecutor be preferred over ThreadPoolExecutor?", "For CPU-bound work, since ProcessPoolExecutor uses separate processes that can run truly in parallel across cores, unlike threads which are limited by the GIL."),
        ("Code:\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef task(n):\n    return n * 2\n\nwith ThreadPoolExecutor() as executor:\n    future = executor.submit(task, 5)\n    print(future.result())\n\nWhat is the output, and what does submit() return?", "10 — submit() schedules the task and immediately returns a Future object, whose .result() blocks until the task completes and then returns its value."),
        ("Code:\nfrom concurrent.futures import ThreadPoolExecutor, as_completed\n\ndef task(n):\n    return n * n\n\nwith ThreadPoolExecutor() as executor:\n    futures = [executor.submit(task, n) for n in [3, 1, 2]]\n    for f in as_completed(futures):\n        print(f.result())\n\nWhat does as_completed() do, and is the print order guaranteed to match the input order?", "as_completed() yields futures as they finish, not in submission order, so the print order reflects completion time and is not guaranteed to match [3, 1, 2]."),
        ("What is asyncio?", "Python's standard library framework for writing concurrent code using coroutines, an event loop, and async/await syntax, typically for I/O-bound tasks."),
        ("Code:\nimport asyncio\n\nasync def greet():\n    print('hello')\n\nasyncio.run(greet())\n\nWhat is the output, and what does asyncio.run() do?", "hello — asyncio.run() creates an event loop, runs the given coroutine to completion, and then closes the loop."),
        ("What is a coroutine, in the context of asyncio?", "A special function defined with async def that can be paused at await points and resumed later by the event loop, without blocking the whole program."),
        ("Code:\nimport asyncio\n\nasync def say_after(delay, message):\n    await asyncio.sleep(delay)\n    print(message)\n\nasync def main():\n    await say_after(1, 'hello')\n    await say_after(1, 'world')\n\nasyncio.run(main())\n\nAbout how long does this take to run, and why?", "About 2 seconds — because each say_after call is awaited sequentially, one after the other, rather than running concurrently."),
        ("Code:\nimport asyncio\n\nasync def say_after(delay, message):\n    await asyncio.sleep(delay)\n    print(message)\n\nasync def main():\n    await asyncio.gather(\n        say_after(1, 'hello'),\n        say_after(1, 'world'),\n    )\n\nasyncio.run(main())\n\nAbout how long does this take to run, and what does asyncio.gather do?", "About 1 second — gather() runs multiple coroutines concurrently and waits for all of them to finish, so the two 1-second sleeps overlap instead of stacking."),
        ("What does the await keyword do?", "It pauses the current coroutine until the awaited operation (another coroutine, task, or future) completes, yielding control back to the event loop in the meantime."),
        ("Code:\nimport asyncio\n\nasync def worker(n):\n    await asyncio.sleep(0.1)\n    return n * n\n\nasync def main():\n    task = asyncio.create_task(worker(5))\n    print('task started')\n    result = await task\n    print(result)\n\nasyncio.run(main())\n\nWhat is the output, and what does asyncio.create_task() do?", "task started\n25 — create_task() schedules the coroutine to run concurrently on the event loop right away, returning a Task handle that can be awaited later, rather than running it immediately inline."),
        ("Code:\nimport asyncio\n\nasync def slow():\n    await asyncio.sleep(5)\n    return 'done'\n\nasync def main():\n    try:\n        result = await asyncio.wait_for(slow(), timeout=1)\n    except asyncio.TimeoutError:\n        print('timed out')\n\nasyncio.run(main())\n\nWhat is the output, and what does asyncio.wait_for do?", "timed out — wait_for() runs a coroutine but cancels it and raises TimeoutError if it doesn't finish within the given time limit."),
        ("What is the event loop in asyncio?", "The core scheduler that runs coroutines, dispatches callbacks, and handles I/O events, deciding which task to run next whenever one is paused at an await."),
        ("What is the key difference between asyncio concurrency and threading concurrency?", "asyncio uses a single thread with cooperative multitasking (coroutines voluntarily yield control at await points), while threading uses OS-level preemptive scheduling across multiple threads."),
        ("Why can asyncio code run into trouble if a coroutine calls a blocking (synchronous) function instead of an async one?", "Because a blocking call doesn't yield control back to the event loop, so it freezes the entire event loop and prevents any other coroutine from making progress during that time."),
        ("Code:\nimport asyncio\n\nasync def worker(n):\n    if n == 2:\n        raise ValueError('bad input')\n    return n\n\nasync def main():\n    tasks = [asyncio.create_task(worker(n)) for n in range(4)]\n    results = await asyncio.gather(*tasks, return_exceptions=True)\n    print(results)\n\nasyncio.run(main())\n\nWhat is the output, and what does return_exceptions=True change?", "[0, 1, ValueError('bad input'), 3] — normally gather() would immediately raise the first exception it encounters; return_exceptions=True instead collects exceptions as regular results in the returned list."),
        ("Code:\nimport asyncio\n\nasync def gen():\n    for i in range(3):\n        await asyncio.sleep(0)\n        yield i\n\nasync def main():\n    async for value in gen():\n        print(value)\n\nasyncio.run(main())\n\nWhat is the output, and what is 'gen' an example of?", "0\n1\n2 — this is an async generator, which supports async for to iterate over values produced asynchronously."),
        ("What does asyncio.Lock provide, and how does it differ from threading.Lock?", "It serializes access to a shared resource among coroutines, similar in purpose to threading.Lock, but designed to be awaited (async with lock) so it cooperates with the event loop instead of blocking a whole OS thread."),
        ("What is the producer-consumer pattern, and what data structure commonly implements it in concurrent Python code?", "A pattern where one or more 'producer' threads/processes generate work items and one or more 'consumer' threads/processes process them; a thread-safe Queue (or multiprocessing.Queue / asyncio.Queue) is typically used to hand items off safely between them."),
        ("Code:\nimport queue\nimport threading\n\nq = queue.Queue()\n\ndef producer():\n    for i in range(3):\n        q.put(i)\n\ndef consumer():\n    for _ in range(3):\n        print(q.get())\n\nt1 = threading.Thread(target=producer)\nt2 = threading.Thread(target=consumer)\nt1.start(); t2.start()\nt1.join(); t2.join()\n\nWhy is queue.Queue safe to share between threads without an explicit lock?", "queue.Queue has its own internal locking, making put() and get() thread-safe operations on their own, so callers don't need to add extra synchronization for basic producer/consumer use."),
        ("When would you choose multiprocessing over asyncio for a task?", "When the work is CPU-bound (heavy computation) rather than I/O-bound, since asyncio's concurrency model doesn't provide true parallelism on a single core and won't speed up CPU-heavy code."),
        ("When would you choose asyncio over threading for a task?", "When handling a very large number of concurrent I/O-bound operations (like thousands of network connections), since coroutines are much lighter-weight than OS threads and avoid thread-related overhead and locking complexity."),
        ("What is 'embarrassingly parallel' work, and why does it suit multiprocessing well?", "Work that can be split into independent chunks with little or no communication needed between them (e.g. processing separate files); it maps cleanly onto multiple worker processes since there's minimal need for shared state or synchronization."),
        ("Code:\nimport time\nimport concurrent.futures\n\ndef io_task(n):\n    time.sleep(1)\n    return n\n\nstart = time.time()\nwith concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:\n    list(executor.map(io_task, range(5)))\nprint(round(time.time() - start))\n\nAbout what does this print, and why?", "About 1 (second) — since all 5 I/O-bound tasks run concurrently across the thread pool, the total time is close to that of a single task rather than 5 tasks run one after another."),
        ("What is a common risk of using too many threads or processes at once?", "Excessive context-switching or process-creation overhead can outweigh the benefits of concurrency, actually slowing the program down and consuming excessive memory/CPU resources."),
        ("What does GIL contention mean in a CPU-bound multithreaded Python program?", "Threads spend time waiting to acquire the GIL from each other instead of doing useful work, which can make heavily multithreaded CPU-bound code perform worse than a single-threaded version."),
    ],
}


def _parse_code_question(question: str):
    """Detect an embedded code/command snippet inside a question string.

    Returns a tuple: (code_text_or_None, language, remaining_question_text).
    If no snippet is found, code_text is None and remaining_question_text
    is just the original question.
    """
    if question.startswith("Code:\n"):
        body = question[len("Code:\n"):]
        lang = "python"
    elif question.startswith("Command"):
        # Handles "Command: ..." and "Command (Linux/Mac): ..." variants
        colon_index = question.find(":")
        body = question[colon_index + 1:].lstrip(" ")
        lang = "bash"
    else:
        return None, None, question

    if "\n\n" in body:
        code, rest = body.split("\n\n", 1)
    else:
        code, rest = body, ""

    return code.strip("\n"), lang, rest.strip()


def main(page: ft.Page):
    # App-wide window configuration
    page.title = "PyQuizy"
    page.window.width = 600
    page.window.height = 750
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- Navigation -----------------------------------------------------
    # Everything below drives page.views instead of clearing/re-adding
    # page.controls directly. This matters for mobile: Flet only wires the
    # Android hardware/gesture back button up to something meaningful when
    # there's an actual view stack to pop. Without it, the back button has
    # nothing to do and the app gets torn down uncleanly on every press,
    # which is what was causing the slow, stuck-session relaunch.

    def build_home_view() -> ft.View:
        menu_buttons = [
            ft.ElevatedButton(
                topic,
                height=56,
                on_click=lambda e, t=topic: show_quiz(t),
            )
            for topic in QUIZ_DATA.keys()
        ]

        return ft.View(
            route="/",
            scroll=ft.ScrollMode.AUTO,
            padding=ft.Padding(left=16, right=16, top=20, bottom=20),
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text(
                    "Welcome To PyQuizy\U0001f40d!",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Column(
                    menu_buttons,
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            ],
        )

    def show_home(e=None):
        # Reset the view stack back down to just the home screen. Used both
        # for the initial launch and for the AppBar/back-button navigation.
        page.views.clear()
        page.views.append(build_home_view())
        page.update()

    def build_question_control(index: int, question: str, answer: str):
        """Build a single question block: a numbered question (with a
        syntax-highlighted code block if present), a copy button, and an
        expandable 'Show Answer' tile.
        """
        code, lang, remaining_text = _parse_code_question(question)

        async def copy_question(e):
            # Flet's clipboard API differs across versions: older Flet uses
            # the synchronous page.set_clipboard(), newer Flet (1.0+) uses
            # an async ft.Clipboard() service instead. Try both so this
            # works regardless of which Flet version is installed.
            #
            # The asyncio.wait_for timeout below is a deliberate safety
            # net: if the app loses focus mid-await (e.g. the user hits
            # back right as they tap copy), an unresolved await here can
            # leave the session's event loop stuck waiting forever, which
            # is exactly the kind of stuck state that made relaunching the
            # app slow. Timing out guarantees this can never hang.
            copied = False
            if hasattr(page, "set_clipboard"):
                try:
                    page.set_clipboard(question)
                    copied = True
                except Exception:
                    copied = False
            if not copied:
                try:
                    await asyncio.wait_for(ft.Clipboard().set(question), timeout=3)
                    copied = True
                except Exception:
                    copied = False

            message = "Question copied!" if copied else "Couldn't copy question"
            snackbar = ft.SnackBar(ft.Text(message), duration=1200)
            if hasattr(page, "open"):
                page.open(snackbar)
            elif hasattr(page, "show_dialog"):
                page.show_dialog(snackbar)
            else:
                page.snack_bar = snackbar
                page.snack_bar.open = True
                page.update()

        copy_button = ft.IconButton(
            icon=ft.Icons.COPY,
            icon_size=18,
            tooltip="Copy question",
            on_click=copy_question,
        )

        body_controls = []
        if code:
            body_controls.append(
                ft.Row(
                    [
                        ft.Text(f"{index}.", size=16, weight=ft.FontWeight.BOLD),
                        copy_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
            body_controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Markdown(
                                f"```{lang}\n{code}\n```",
                                selectable=True,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                code_theme=ft.MarkdownCodeTheme.ATOM_ONE_DARK,
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO,  # long lines scroll, never clip
                    ),
                    bgcolor="#1e1e1e",
                    border_radius=8,
                    padding=10,
                )
            )
            if remaining_text:
                body_controls.append(
                    ft.Text(remaining_text, size=16, selectable=True)
                )
        else:
            body_controls.append(
                ft.Row(
                    [
                        ft.Text(
                            f"{index}. {question}",
                            size=16,
                            selectable=True,
                            expand=True,
                        ),
                        copy_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )

        return ft.Column(
            body_controls
            + [
                ft.ExpansionTile(
                    title=ft.Text("Show Answer"),
                    controls=[
                        ft.Container(
                            content=ft.Text(answer, selectable=True),
                            padding=10,
                        )
                    ],
                ),
            ],
            spacing=4,
        )

    def show_quiz(topic: str):
        """Push the quiz as its own View on page.views (instead of clearing
        and re-adding page.controls). Questions still load in small batches
        so opening a topic stays instant, but now the view is a real entry
        on the navigation stack — which is what lets the Android hardware
        back button pop back to the topic menu on its own, matching the
        AppBar back arrow, instead of tearing the whole app down.
        """
        questions = QUIZ_DATA[topic]
        total = len(questions)
        batch_size = 10
        state = {"loaded": 0}

        question_list = ft.Column(spacing=8)
        load_more_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        def load_more(e=None):
            start = state["loaded"]
            end = min(start + batch_size, total)
            for i in range(start, end):
                question, answer = questions[i]
                question_list.controls.append(
                    build_question_control(i + 1, question, answer)
                )
            state["loaded"] = end

            load_more_row.controls.clear()
            if state["loaded"] < total:
                load_more_row.controls.append(
                    ft.ElevatedButton(
                        f"Load More ({state['loaded']}/{total})",
                        on_click=load_more,
                    )
                )
            else:
                load_more_row.controls.append(ft.Container(height=12))
            page.update()

        def go_back(e=None):
            if len(page.views) > 1:
                page.views.pop()
                page.update()

        quiz_view = ft.View(
            route=f"/quiz/{topic}",
            scroll=ft.ScrollMode.AUTO,
            padding=ft.Padding(left=16, right=16, top=12, bottom=12),
            appbar=ft.AppBar(
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                title=ft.Text(topic),
                center_title=False,
            ),
            controls=[question_list, load_more_row],
        )

        page.views.append(quiz_view)
        page.update()
        load_more()

    def handle_view_pop(e: ft.ViewPopEvent):
        # Fires for the AppBar back arrow and for the Android
        # hardware/gesture back button, since Flet routes both through the
        # views stack. Popping here keeps both paths in sync. When only the
        # home view is left, there's nothing to pop, so Flet/Android falls
        # through to their normal "exit app" behavior — which is now a
        # clean shutdown instead of the previous undefined state.
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_view_pop = handle_view_pop

    # Start the app on the home menu screen
    show_home()


ft.app(target=main)
