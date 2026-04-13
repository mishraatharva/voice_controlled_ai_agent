def factorial(n: int) -> int:
    """Calculate the factorial of a non‑negative integer n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        try:
            number = int(sys.argv[1])
            print(factorial(number))
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Usage: python generated.py <non-negative integer>")