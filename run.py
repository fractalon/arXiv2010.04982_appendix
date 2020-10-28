import os
from matplotlib import pyplot as plt

from validate import validate_modulo



def is_prime(n):
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True

START_VALUE = 3
END_VALUE = 1000

# We show graphic where $y$ equal to
#  fraction of $A \in (1;x)$ such that
#  $2 F(1/2)/Q(1/2) < 4 A^2 / |R_A| - A$
all_xx = []
all_yy = []
n_all_falses = 0
prime_xx = []
prime_yy = []
n_prime_falses = 0
n_primes = 0
false_values = []
print(f"Values from {START_VALUE} to {END_VALUE}:")
for mod in range(START_VALUE, END_VALUE + 1):
    if not validate_modulo(mod):
        false_values.append(mod)
        print(mod)

        n_all_falses += 1
        if is_prime(mod):
            n_prime_falses += 1

    all_xx.append(mod)
    all_yy.append(n_all_falses * 1. / mod)
    if is_prime(mod):
        n_primes += 1
        prime_xx.append(mod)
        prime_yy.append(n_prime_falses * 1. / n_primes)



OUTPUT_DIR = "output"

values_filename = os.path.join(
    OUTPUT_DIR,
    f"values_less_then_{END_VALUE}.txt"
)
with open(values_filename, "wt") as fout:
    fout.write("\n".join(map(str, false_values)))

plt.plot(all_xx, all_yy)
plt.xlabel("$N$")
plt.title("$N\\ \\to\\ N^{-1} \\# \\{ A \\leq N : 2f_A(0.5) > \\frac{4 A^2}{|R_A|} - A \\}$")
plt.savefig(os.path.join(
    OUTPUT_DIR,
    f"all_numbers_less_then_{END_VALUE}.png"
))
plt.clf()

plt.plot(prime_xx, prime_yy)
plt.xlabel("$N$")
plt.title("$N\\ \\to\\ |\\mathcal{P} \\cap [1;N]|^{-1} \\# \\{ A \\in \\mathcal{P} \\cap [1;N] : 2f_A(0.5) > \\frac{4 A^2}{|R_A|} - A \\}$")
plt.savefig(os.path.join(
    OUTPUT_DIR,
    f"primes_less_then_{END_VALUE}.png"
))

print("The end")
