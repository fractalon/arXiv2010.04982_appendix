def get_quadratic_residues(mod):
    squares = set()
    for k in range(mod):
        squares.add((k * k) % mod)

    squares = list(squares)
    squares.sort()
    
    return squares

def get_dists_between_squares(mod):
    squares = get_quadratic_residues(mod)

    return [
        right - left 
        for left, right in zip(squares[:-1], \
                               squares[1:])
    ] + [squares[0] + mod - squares[-1]]

def calculate_polynom(coefs, arg):
    value = 0
    power = 1
    for single_coef in coefs:
        value += single_coef * power
        power *= arg
        if power < 0:
            print("ERROR")
            exit()
    return value

# @diffs is list [s_0, s_1, ..., s_r]
# Return t^{|R_A|} F(1/t)
#  where $F(y) = \sum_{0<=i<=r-1, 0<=k<=r} {s_i s_{i+k} y^k}$
# We use $p_i(y) = \sum_{0<=k<=r-1} {s_{i+k} y^k}$
# (see "readme" file for details)
def smart_calculate_main_polynom(diffs, t):
    size = len(diffs)

    # $t^{|R_A|} p_0(1/t)$
    factor = calculate_polynom(diffs[::-1], t) * t
    normalize_factor = t ** size
    value = 0
    for index in range(size):
        value += diffs[index] * factor

        # change @factor value
        # from $t^{|R_A|} p_i(1/t)$
        # to $t^{|R_A|} p_{i+1}(1/t)$
        factor -= diffs[index] * normalize_factor
        factor *= t
        factor += diffs[index] * t
    value *= 2

    sum_sqr_diffs = sum(map(lambda x: x * x, diffs))
    value -= sum_sqr_diffs * normalize_factor
    value += sum_sqr_diffs

    return value

# @modulo : value of A
# Return True if $f_A(1/2) < (4 A^2 / |R_A| - A)$
def validate_modulo(modulo):
    dists = get_dists_between_squares(modulo)
    n_squares = len(dists)
    # $2^{|R_A|} F(1/2)$
    main_polynom = \
            smart_calculate_main_polynom(dists, 2).numerator

    # $2^{|R_A|+1} |R_A| F(1/2)$
    left = 2 * main_polynom * n_squares
    # $2^{|R_A|} Q(1/2)$
    q_factor = (2 ** (n_squares + 1) - 2)
    # $2^{|R_A|} Q(1/2) (4 A^2 - |R_A| A)$
    right = q_factor * modulo * (4 * modulo - n_squares)

    return left < right
