import matplotlib.pyplot as plt
try:
    import colorama
    from colorama import Fore, Style
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

    class _NoColor:
        def __getattr__(self, name):
            return ""

    Fore = _NoColor()
    Style = _NoColor()

    
def compute_grundy_values(game_function, max_n):
    """
    Compute the Sprague-Grundy values G(0), G(1), ..., G(max_n)
    for a game defined by a given game_function.

    Parameters:
        game_function (function): A function that takes an integer n and returns a list of reachable positions.
        max_n (int): The maximum value of n for which to compute Grundy values.

    Returns:
        list: A list of Grundy values from G(0) to G(max_n).
    """
    grundy = [0] * (max_n + 1)

    for n in range(1, max_n + 1):
        reachable_values = set()
        for next_pos in game_function(n):
            reachable_values.add(grundy[next_pos])
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
        max_p = n // 2

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
        max_p = n // 2

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
    if period is None:
        return
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

def plot_grundy_values(grundy, l, p, title, filename="grundy_plot.png", num_periods=3):
    n = len(grundy)
    plot_range = min(n, l + p * num_periods + 1)
    x = range(plot_range)
    plt.figure(figsize=(10, 6))
    plt.plot(x, grundy[:plot_range], label="Grundy Values", marker="o", linestyle="-")

    plt.axvline(x=l, color="red", linestyle="--", label=f"Start of Period (l={l})")
    for i in range(1, num_periods + 1):
        plt.axvline(x=l + i * p, color="orange", linestyle="--")

    plt.title(title)
    plt.xlabel("Game State (n)")
    plt.ylabel("Grundy Value")
    plt.legend()
    plt.grid()
    plt.savefig(filename)
    print(f"Plot saved to {filename}")
