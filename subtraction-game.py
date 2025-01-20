import argparse

# Conditionally import colorama
try:
    import colorama
    from colorama import Fore, Style
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

    # Create "fake" classes and variables so code runs even if colorama is unavailable.
    class _NoColor:
        def __getattr__(self, name):
            return ""  # Return empty string for any color attribute

    Fore = _NoColor()
    Style = _NoColor()


parser = argparse.ArgumentParser(description="Compute and analyze Sprague-Grundy values for a subtraction game.")
parser.add_argument("--moves",
                    nargs="+",
                    type=int,
                    default=[2, 3],
                    help="List of allowed subtractions (integers). Default is [2, 3].")
parser.add_argument("--n",
                    type=int,
                    default=1000,
                    help="Compute Grundy values up to this n. Default is 1000.")
parser.add_argument("--num_periods",
                    type=int,
                    default=3,
                    help="Number of consecutive periods to print for demonstration. Default is 3.")
parser.add_argument("--max_period",
                    type=int,
                    default=None,
                    help="Maximum period candidate to check. If None, uses len(grundy)-1.")


def compute_grundy_values(moves, max_n):
    """
    Compute the Sprague-Grundy values G(0), G(1), ..., G(max_n)
    for a subtraction game with the given moves.
    """
    grundy = [0] * (max_n + 1)

    for n in range(1, max_n + 1):
        reachable_values = set()
        for m in moves:
            if n >= m:
                reachable_values.add(grundy[n - m])
        # mex: smallest nonnegative integer not in reachable_values
        g = 0
        while g in reachable_values:
            g += 1
        grundy[n] = g

    return grundy

def detect_pure_period(grundy, max_p=None):
    """
    Detect the smallest (l, p) such that for all n >= l:
       grundy[n + p] == grundy[n].

    Parameters:
    -----------
    grundy : list of integers (the Sprague-Grundy sequence)
    max_p  : int or None
        Maximum period to check. If None, periods up to length of `grundy` - 1 will be checked.

    Returns:
    --------
    (l, p) if a period is found,
    or (None, None) if no period is found within naive search bounds.
    """
    n = len(grundy)
    if max_p is None:
        max_p = n - 1

    for l in range(n):
        for p in range(1, min(max_p + 1, n - l)):
            is_periodic = True

            for i in range(l, n - p):
                if grundy[i] != grundy[i + p]:
                    is_periodic = False
                    break
            if is_periodic:
                return (l, p)

    return (None, None)

def detect_arithmetic_period(grundy, max_p=None, max_d=None):
    """
    Detect the smallest (l, p, d) such that for all n >= l:
       grundy[n + p] == grundy[n] + d.

    This is a naive approach, checking all l, p, d within the
    provided bounds. For large sequences, this can be slow.

    Parameters:
    -----------
    grundy : list[int]
        The Sprague-Grundy sequence.
    max_p  : int or None
        Maximum period to check. If None, periods up to length of `grundy` - 1 will be checked.

    Returns:
    --------
    (l, p, d) if an arithmetic period is found,
    or (None, None, None) if no arithmetic period is found within search bounds.
    """
    n = len(grundy)
    if max_p is None:
        max_p = n - 1

    for l in range(n):
        for p in range(1, min(max_p + 1, n - l)):
            d_candidate = grundy[l + p] - grundy[l]

            is_arith_periodic = True
            for i in range(l, n - p):
                if grundy[i] + d_candidate != grundy[i + p]:
                    is_arith_periodic = False
                    break
            if is_arith_periodic:
                return (l, p, d_candidate)

    return (None, None, None)

def print_periodic_segment(grundy_values, start, period, num_periods=3):
    if COLORAMA_AVAILABLE:
        colorama.init()
    
    colors = [
        Fore.RED, Fore.GREEN, Fore.YELLOW,
        Fore.BLUE, Fore.MAGENTA, Fore.CYAN,
        Fore.WHITE
    ]

    length = num_periods * period + 1
    end = start + length
    end = min(end, len(grundy_values))

    for i in range(start, end):
        color_index = (i - start) % period
        color = colors[color_index % len(colors)]
        print(f"{color}[{i}] {grundy_values[i]}{Style.RESET_ALL}")

def main():
    args = parser.parse_args()

    moves = args.moves
    max_n = args.n
    num_periods = args.num_periods
    max_p = args.max_period

    print(f"Analyzing Subtraction Game: S = {moves}, up to n = {max_n}")
    
    grundy_values = compute_grundy_values(moves, max_n)

    # 2) Detect pure period:
    l_pure, p_pure = detect_pure_period(grundy_values)
    if p_pure is not None:
        print(f"[Pure Periodicity] Found: pre-period = {l_pure}, period = {p_pure}")
        print_periodic_segment(grundy_values, l_pure, p_pure)
    else:
        print("[Pure Periodicity] No period found in the naive search range.")

    # 3) Detect arithmetic period:
    l_arith, p_arith, d_arith = detect_arithmetic_period(grundy_values)
    if p_arith is not None:
        print(f"[Arithmetic Periodicity] Found: pre-period = {l_arith}, period = {p_arith}, saltus = {d_arith}")
        print_periodic_segment(grundy_values, l_pure, p_pure)
    else:
        print("[Arithmetic Periodicity] No arithmetic period found in the naive search range.")

if __name__ == "__main__":
    main()

