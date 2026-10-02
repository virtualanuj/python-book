# Lesson 1: First steps

Welcome! This lesson assumes you have **never written Python before**. Take it slowly. There is no time limit, and getting stuck is a normal part of learning, not a sign you're doing it wrong. If anything is confusing, paste it into the chat and ask.

**What you'll build today:** four tiny pieces of ThreatDesk, each just one line long.

**What you'll learn:** how to run Python, what values and variables are, how to build text with f-strings, and how to write a function.

---

## Part 1: Say hello to Python (5 minutes)

Open a terminal, go to the repo folder, and start Python's interactive prompt:

```bash
cd ~/workspace/python-book
uv run --python 3.14 python
```

You'll see `>>>`. That's Python waiting for you. Type each line below and press Enter:

```python
>>> 2 + 3
5
>>> print("Hello, ThreatDesk!")
Hello, ThreatDesk!
```

That's it: you've run Python code. Type `exit()` (or press Ctrl+D) when you want to leave.

## Part 2: Values and variables (5 minutes)

Text in Python is called a **string**. You write it inside quotes:

```python
>>> "198.51.100.7"
'198.51.100.7'
```

A **variable** is a name you give to a value, so you can use it later. The `=` sign means "store this value under this name":

```python
>>> ip = "198.51.100.7"
>>> ip
'198.51.100.7'
```

Think of a variable as a sticky label on a box. `ip` is the label; `"198.51.100.7"` is what's in the box.

> 💡 The IP addresses in this course (like 198.51.100.7) are special "documentation" addresses. They don't belong to anyone, so they're safe to use in examples.

## Part 3: Building text with f-strings (5 minutes)

Put an `f` before the opening quote, and anything inside `{curly braces}` gets replaced by its value:

```python
>>> ip = "198.51.100.7"
>>> f"Suspicious address: {ip}"
'Suspicious address: 198.51.100.7'
```

You can use more than one:

```python
>>> kind = "ipv4-addr"
>>> f"{kind} = {ip}"
'ipv4-addr = 198.51.100.7'
```

## Part 4: Two handy string tools (5 minutes)

Strings come with built-in tools called **methods**. You use them with a dot:

```python
>>> "  hello  ".strip()          # removes spaces at the start and end
'hello'
>>> "EVIL.Example".lower()       # makes every letter lowercase
'evil.example'
>>> "  EVIL.Example ".strip().lower()   # you can chain them
'evil.example'
```

## Part 5: Your first function (10 minutes)

A **function** is a small, named recipe. You give it some input, it gives you back a result. Here is a complete one:

```python
def greet(name):
    return f"Hello, {name}!"
```

Reading it line by line:

- `def greet(name):` means "define a function called `greet` that takes one input, called `name`". Note the colon at the end.
- The next line is **indented** (4 spaces). Indentation tells Python "this line belongs to the function".
- `return` sends the result back.

Using it:

```python
>>> greet("Anuj")
'Hello, Anuj!'
```

That's every idea you need for the exercise.

---

## Exercise: four tiny steps

Open `lessons/01-first-steps/exercise.py` in your editor (VS Code is a good free choice). You'll see four functions. Each one currently returns an empty string `""`. Your job is to replace that one line in each.

Run the checks whenever you like:

```bash
uv run --python 3.14 lessons/01-first-steps/exercise.py
```

The checker goes **one step at a time**. It tells you which step to work on next and gives you a hint. Fix that step, save the file, and run it again.

| Step | Function | Should return |
|---|---|---|
| 1 | `welcome()` | `"Welcome to ThreatDesk"` |
| 2 | `label(value)` | `"Indicator: "` followed by the value |
| 3 | `make_key(kind, value)` | the kind and the value joined by a pipe character (see the example in the file) |
| 4 | `clean(value)` | the value with outside spaces removed and in lowercase |

When all four pass, you'll see a celebration message. 🎉 Then take a look at [`solutions/01-first-steps/solution.py`](../../solutions/01-first-steps/solution.py) to compare.

## If you see an error

Python errors look scary but are actually helpful. Read the **last line** first: it says what went wrong. The line above usually points to where. Common ones today:

- `IndentationError`: a line inside a function needs 4 spaces in front of it.
- `SyntaxError`: often a missing quote `"`, bracket `)`, or colon `:`.
- `NameError: name 'x' is not defined`: a typo in a name, or using a variable before creating it.

Stuck for more than 10 minutes? Paste the error into the chat. That's what it's there for.

## Why this matters for ThreatDesk

Every threat feed sends values like `"  EVIL.Example "` with messy spaces and mixed case. Your `clean()` function makes them consistent, and `make_key()` gives each indicator a simple ID. ThreatDesk will use both of these for real in the coming lessons.
