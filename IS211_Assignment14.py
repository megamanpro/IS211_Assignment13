def fibonnaci(n):
    if n == 1 or n == 2:
        return 1
    return fibonnaci(n - 1) + fibonnaci(n - 2)

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def compareTo(s1, s2):

    if len(s1) == 0 and len(s2) == 0:
        return 0
    if len(s1) == 0:
        return -1
    if len(s2) == 0:
        return 1

    if s1[0] < s2[0]:
        return -1
    elif s1[0] > s2[0]:
        return 1
    else:
        return compareTo(s1[1:], s2[1:])



if __name__ == "__main__":

    print("Fibonacci(6):", fibonnaci(6))   # Expected 8
    print("Fibonacci(10):", fibonnaci(10)) # Expected 55


    print("GCD(48, 18):", gcd(48, 18))     # Expected 6
    print("GCD(101, 10):", gcd(101, 10))   # Expected 1


    print("compareTo('apple', 'banana'):", compareTo("apple", "banana"))  # Expected -1
    print("compareTo('cat', 'cat'):", compareTo("cat", "cat"))            # Expected 0
    print("compareTo('dog', 'cat'):", compareTo("dog", "cat"))            # Expected 1
