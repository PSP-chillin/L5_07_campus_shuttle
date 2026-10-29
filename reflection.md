# Reflection

## 1. Which issue was the most serious, and why?

The deleted-route lookup was the most immediately serious issue because it
caused the program to terminate with a `KeyError` during normal execution.
Invalid passenger data and the broad exception handler were also serious
because they could produce incorrect reports while hiding the underlying
cause.

## 2. How did the analysis tools help?

Pylint identified maintainability problems such as the mutable default
argument, naming style, missing documentation, and global-state handling.
Flake8 checked formatting and whitespace consistency. Bandit reviewed
security-sensitive patterns; the final implementation uses `secrets.choice`
for driver selection and produced no Bandit findings.

## 3. What could static analysis not find?

Static tools did not reliably identify the runtime sequence in which `R3`
was removed and then accessed, nor did they decide that `"full"` and `-6`
were invalid business data. Running the program with default and invalid
route inputs exposed those behavior problems.

## 4. How will you prevent similar issues in future?

I will validate inputs at the point where they enter the program, avoid
mutable defaults and broad exception handlers, use context managers for
resources, and run Pylint, Flake8, Bandit, and representative runtime tests
before submitting changes. I will also keep the main entry point behind an
`if __name__ == "__main__":` guard so the module can be tested safely.

