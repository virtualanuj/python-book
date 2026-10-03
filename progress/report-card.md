# Report card: Lessons 1 to 6

*For Anuj, last updated 3 October 2026*

## Progress report

- **Lessons done:** 6 out of 42.
- **Current module:** Module 1, Python from zero. You've done 6 of its 7 lessons.
- **Up next:** Lesson 7, *Files, modules and project layout*. ThreatDesk becomes a real `threatdesk` package. That finishes Module 1.

| Lesson | Finished | Commit |
|---|---|---|
| 1. First steps | 2 Oct 2026 | `efa1aed` |
| 2. Making decisions | 2 Oct 2026 | `07101ba` |
| 3. Lists and loops | 2 Oct 2026 | `6b810d4` |
| 4. Slicing and splitting | 2 Oct 2026 (tidied the same day in `a0f55dd`) | `7cf7be1` |
| 5. Dictionaries and sets | 3 Oct 2026 | `494d5ed` |
| 6. Errors and exceptions | 3 Oct 2026 | `9fa9524` |

(`Lessons.md` still shows lesson 6 as 👉, but your commit `9fa9524` and the checker both say it's done.)

**Pace:** six lessons in two days is fast, and the code shows you're understanding the ideas, not just rushing through them.

## Scorecard

Every checker passes (all steps, all six lessons). I ran each one with `uv run --python 3.14 lessons/NN-slug/exercise.py`.

| Lesson | Correctness (4) | Clarity (3) | Python style (3) | Total (10) | Grade |
|---|---|---|---|---|---|
| 1. First steps | 4 | 3 | 3 | **10** | Excellent |
| 2. Making decisions | 4 | 2 | 2 | **8** | Good |
| 3. Lists and loops | 4 | 2 | 3 | **9** | Great |
| 4. Slicing and splitting | 4 | 2 | 2 | **8** | Good |
| 5. Dictionaries and sets | 4 | 3 | 2 | **9** | Great |
| 6. Errors and exceptions | 4 | 2 | 2 | **8** | Good |
| **Overall average** | | | | **8.7** | **Great** |

As a guide: 8 means working, readable code from a beginner, and that's a good result. Every lesson is at 8 or above.

---

## Lesson feedback

### Lesson 1: First steps (10/10)

**What went well**
- Clean, one-line answers that use exactly what the lesson taught. Chaining two methods in `lessons/01-first-steps/exercise.py:32` is just right: `return value.strip().lower()`
- You added a guard nobody asked for (`lessons/01-first-steps/exercise.py:24-25`):
  ```python
  if not kind or not value:
      raise ValueError("kind and value must be non-empty strings")
  ```
  `make_key("", "")` now raises a clear error, where a quieter version would hand back a broken key `"|"`. That's good security-product thinking, and it's why lesson 6 opens by mentioning you.

**To improve**
Nothing to take points off for here.

**Try this (optional)**
Your guard lets text made only of spaces through: `make_key("  ", "x")` gives `'  |x'` (I tried this). Can you make it reject that too? Hint: what does `"  ".strip()` give you?

### Lesson 2: Making decisions (8/10)

**What went well**
- `is_ipv4` is a neat one-liner that combines two questions with `and` (`lessons/02-making-decisions/exercise.py:26`): `return value.count(".") == 3 and value.replace(".", "").isdigit()`
- `guess_kind` calls your own three functions and checks for a URL first, just as the hint asked (lines 38-45).

**To improve**
1. **The error message says something the check doesn't do.** Line 36 says "non-empty string", but `guess_kind("")` still returns `'domain-name'` (I tried it). Also, `value is None` is already covered by `not isinstance(value, str)`, because `None` isn't a string. (`isinstance` asks "is this value of this type?". The course hasn't covered it yet.)
   ```python
   # before (lines 36-37)
   if value is None or not isinstance(value, str):
       raise ValueError("value must be a non-empty string")
   # after
   if not isinstance(value, str) or value == "":
       raise ValueError("value must be a non-empty string")
   ```
2. **Trailing spaces.** Line 45 has four spaces after `return "domain-name"`. You can't see them, but tools flag them. Most editors have a "trim trailing whitespace on save" setting (in VS Code it's `files.trimTrailingWhitespace`). Turn it on and you won't have to think about this again.
   ```python
   # before
   return "domain-name"····
   # after
   return "domain-name"
   ```

**Try this (optional)**
`guess_kind("HTTPS://x.example")` returns `'domain-name'` (I tried it), because `startswith` cares about upper and lower case. Fix `is_url` so capital letters still count as a URL. Small tip for later: `startswith` also accepts a tuple, so `value.startswith(("http://", "https://"))` asks both questions at once.

### Lesson 3: Lists and loops (9/10)

**What went well**
- You found **list comprehensions** on your own. A list comprehension is a one-line way to build a new list. `lessons/03-lists-and-loops/exercise.py:47` reads almost like English: `result = [value for value in values if guess_kind(value) == kind]`
- You remembered that indexes start at 0 (`return values[0]`, line 28), and you used `len()` where it belongs (line 34).

**To improve**
1. **`without_duplicates` is clever but hard to read.** Line 55 combines `enumerate`, a slice and `not in` on one line. `enumerate` gives you each item's position along with the item, and the course hasn't covered it yet. The code works, but each round it copies the start of the list, and a reader has to stop and puzzle it out. The plain loop from Part 5 says the same thing more clearly:
   ```python
   # before (line 55)
   result = [value for i, value in enumerate(values) if value not in values[:i]]
   # after
   result = []
   for value in values:
       if value not in result:
           result.append(value)
   ```
   (Lesson 5's `seen` set made this fast too, and you did that perfectly there.)
2. **A small leftover from the template.** Lines 40-41 (and 47-48, 55-56) store the list in `result` and then return it on the next line. With a comprehension you can return it directly:
   ```python
   # before
   result = [clean(value) for value in values]
   return result
   # after
   return [clean(value) for value in values]
   ```

**Try this (optional)**
`without_duplicates(["A", "a", " a"])` keeps all three (I tried it), but to ThreatDesk they're the same indicator. Write `clean_unique(values)`, which cleans every value and *then* removes duplicates, by joining two functions you already have.

### Lesson 4: Slicing and splitting (8/10)

**What went well**
- `split_once` uses `partition` and tuple unpacking just as the lesson taught, with `_` for the part you don't need (`lessons/04-slicing-and-splitting/exercise.py:25-26`): `before, _, after = text.partition(sep)`
- `parse_pattern` uses steps 1 to 4 and early returns, and it rejects every broken pattern I tried (`""`, `"["`, `"[]"`, `"[ipv4-addr = 'x']"`, `"[:value = 'x']"`, `"[a:b = '']"`). It all returns `None`, just as a strict parser should.
- You came back after passing and simplified it (commit `a0f55dd` merged two `if` checks into one). Going back to tidy code that already works is a great habit.

**To improve**
1. **Strip once, use it twice.** Line 12 calls `pattern.strip()` two times. Store it in a variable first:
   ```python
   # before (line 12)
   return pattern.strip().startswith("[") and pattern.strip().endswith("]")
   # after
   p = pattern.strip()
   return p.startswith("[") and p.endswith("]")
   ```
2. **A name that says the wrong thing.** At line 44, `value` holds the whole inside of the brackets, not the indicator's value. The real value turns up later as `right[1:-1]`. Following the README plan (remove the quotes, then check for `""`) also makes the special `right == "''"` check on line 47 unnecessary:
   ```python
   # before (lines 44-55, shortened)
   value = strip_brackets(pattern)
   left, right = split_once(value, "=")
   if not is_quoted(right) or right == "''":
       return None
   ...
   return (kind, prop, right[1:-1])
   # after
   left, right = split_once(strip_brackets(pattern), "=")
   if not is_quoted(right):
       return None
   kind, prop = split_once(left, ":")
   value = right[1:-1]
   if not kind or not prop or not value:
       return None
   return (kind, prop, value)
   ```
3. **Trailing spaces.** Line 49 is a blank line with four spaces in it. The editor setting from lesson 2 fixes this.

**Try this (optional)**
`parse_pattern("[a:b = ' ']")` returns `('a', 'b', ' ')` (I tried it), so a value that's just a space gets through. Make the parser reject values that are empty *after* stripping spaces.

### Lesson 5: Dictionaries and sets (9/10)

**What went well**
- `ingest` follows the 6-line plan cleanly. The `seen_keys` set gives it the fast "have I seen this?" check, and `continue` skips broken patterns (`lessons/05-dicts-and-sets/exercise.py:72-79`). In my test it kept `ipv4-addr|1.2.3.4` and `domain-name|1.2.3.4` as two separate indicators, dropped the repeat, and skipped `"broken"` and `""`. That's exactly right.
- The counting line is the dict pattern from Part 3, used perfectly (line 62): `counts[ind["type"]] = counts.get(ind["type"], 0) + 1`
- `seen_keys` (line 70) is a better name than plain `seen`, because it says *what* has been seen.

**To improve**
1. **`type` is a built-in name.** Line 32 uses `type` as a variable. Python already has a built-in called `type()`, and your variable hides it inside this function. Code there that tried to call `type(...)` would break in a confusing way. The course style is to use `object_type`:
   ```python
   # before (lines 32-33)
   type, prop, value = parsed
   return {"type": type, "property": prop, "value": value, "key": f"{type}|{value}"}
   # after
   object_type, prop, value = parsed
   return {"type": object_type, "property": prop, "value": value,
           "key": f"{object_type}|{value}"}
   ```
   (The dict key `"type"` is fine. It's only the variable name that matters.)

**Try this (optional)**
The README's stretch goal is still waiting: `remove_allowed(indicators, allow_list)`. It drops any indicator whose value is on your own allow-list. Turn the list into a set first.

### Lesson 6: Errors and exceptions (8/10)

**What went well**
- `ingest` catches only the error it expects and uses the error's message, just as Part 3 taught (`lessons/06-errors-and-exceptions/exercise.py:88-89`): `except PatternError as err:` / `errors.append(f"{pattern!r}: {err}")`. In my test, `ingest(["[a:b = 'x']", "[a:b = 'x']", "nope", "[a:b = x]"])` gave one indicator and two clear error reports.
- Every one of the four error messages appears on the right input. I checked each one, including tricky ones like `"[]"` and `"[a: = '']"`.
- You followed the new type-hint style exactly. Hints are on the function lines only (for example line 77), and the local lists at lines 78-80 have none.

**To improve**
1. **Reuse `require_brackets`.** Lines 49-51 copy the bracket check you'd already written in step 2, and the comment on line 42 asks you to use it. When the same rule lives in two places, sooner or later someone fixes one copy and forgets the other.
   ```python
   # before (lines 49-52)
   patt = pattern.strip()
   if not (patt.startswith("[") and patt.endswith("]")):
       raise PatternError("missing [ ] brackets")
   left, _, right = patt[1:-1].partition("=")
   # after
   inner = require_brackets(pattern)
   left, _, right = inner.partition("=")
   ```
2. **Two blank lines between functions.** Line 39 is the only blank line between `require_brackets` and the comment above `parse_pattern`. The template had two, and you removed one.
3. **Keep the `try` block small.** At lines 82-87, everything sits inside `try`, including the de-duplication. Only `parse_pattern` can raise `PatternError`, so wrap just that line. A reader can then see straight away which line you expect to fail:
   ```python
   try:
       parsed = parse_pattern(pattern)
   except PatternError as err:
       errors.append(f"{pattern!r}: {err}")
       continue
   indicator = to_indicator(parsed)
   if indicator["key"] not in seen:
       seen.add(indicator["key"])
       indicators.append(indicator)
   ```

**Try this (optional)**
Write `error_summary(patterns)`, which returns a count of each kind of error, like `{"missing [ ] brackets": 2, "value is empty": 1}`. It combines `try`/`except` from this lesson with the counting pattern from lesson 5.

---

## Patterns across lessons

**Strengths that keep showing up**
- **You think about bad input without being asked.** You added guards in lessons 1 and 2, `None` checks in lesson 4, and precise error messages in lesson 6. A security product needs exactly this instinct, and you have it already.
- **Short, direct code.** You reach for the right string method (`strip`, `lower`, `startswith`, `partition`) and often get a step into one clear line.
- **You go back and tidy up.** The second lesson 4 commit shows you improving code that already passed.

**The two habits most worth working on next**
1. **Reuse what you've already built.** Twice now you've rewritten logic you already had: the bracket check in lesson 6 (lines 49-51), and the double `strip()` in lesson 4 (line 12). Before writing a check, ask yourself: "Do I have a function or variable that already does this?" This matters even more in lesson 7, when your code moves into modules that import from each other.
2. **A quick tidy pass before committing.** The style points you lost were all small: trailing spaces (lesson 2 line 45, lesson 4 line 49), a missing blank line (lesson 6 line 39) and the `type` variable name (lesson 5 line 32). Turning on "trim trailing whitespace" in your editor fixes the first one forever. Lesson 15 adds Ruff, a tool that catches the rest for you automatically.

Brilliant start, Anuj. Six lessons in, ThreatDesk can already ingest a feed, drop duplicates and explain what's wrong with bad data.
