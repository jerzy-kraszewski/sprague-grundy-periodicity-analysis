import argparse
from utils import compute_grundy_values, detect_arithmetic_period, \
    detect_pure_period, print_periodic_segment, plot_grundy_values
import os
import shutil

parser = argparse.ArgumentParser(
    description="Compute and analyze Sprague-Grundy values for the Subtraction(S) and Allbut(S) games.")
parser.add_argument("--s",
                    nargs="+",
                    type=int,
                    default=[2, 3],
                    help="Set S, allowed moves in Subtraction game, disallowed moves in Allbut game")
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


def get_subtraction_game_function(S):
    func = lambda x: set(x - s for s in S if x - s >= 0)
    return func


def get_allbut_game_function(S):
    func = lambda x: set(i for i in range(1, x+1) if i not in S)
    return func


def main():
    args = parser.parse_args()

    moves = args.s
    max_n = args.n
    num_periods = args.num_periods
    max_p = args.max_period
    
    try:
        shutil.rmtree('out')
    except:
        pass
    finally:
        os.mkdir('out')

    print(f"Analyzing Subtraction Game: S = {moves}, up to n = {max_n}")
    
    game_function = get_subtraction_game_function(moves)
    grundy_values = compute_grundy_values(game_function, max_n)

    l_pure, p_pure = detect_pure_period(grundy_values)
    if p_pure is not None and p_pure <= max_n / 2:
        print(f"[Pure Periodicity] Found: pre-period = {l_pure}, period = {p_pure}")
        print_periodic_segment(grundy_values, l_pure, p_pure)
        title = f"Subtraction({moves}), pure p={p_pure}"
        plot_grundy_values(grundy_values, l_pure, p_pure, title, filename="out/subtraction_pure.png")
    else:
        print("[Pure Periodicity] No period found in the naive search range.")

    l_arith, p_arith, d_arith = detect_arithmetic_period(grundy_values)
    if p_arith is not None and p_arith <= max_n / 2:
        print(f"[Arithmetic Periodicity] Found: pre-period = {l_arith}, period = {p_arith}, saltus = {d_arith}")
        print_periodic_segment(grundy_values, l_arith, p_arith)
        title = f"Subtraction({moves}), arith p={p_arith} d={d_arith}"
        plot_grundy_values(grundy_values, l_arith, p_arith, title, filename="out/subtraction_arith.png")
    else:
        print("[Arithmetic Periodicity] No arithmetic period found in the naive search range.")
  
    print('---' * 10)
    print(f"Analyzing Allbut Game: S = {moves}, up to n = {max_n}")
    
    game_function = get_allbut_game_function(moves)
    grundy_values = compute_grundy_values(game_function, max_n)

    l_pure, p_pure = detect_pure_period(grundy_values)
    if p_pure is not None and p_pure <= max_n / 2:
        print(f"[Pure Periodicity] Found: pre-period = {l_pure}, period = {p_pure}")
        print_periodic_segment(grundy_values, l_pure, p_pure)
        title = f"Allbut({moves}), pure p={p_pure}"
        plot_grundy_values(grundy_values, l_pure, p_pure, title, filename="out/allbut_pure.png")
    else:
        print("[Pure Periodicity] No period found in the naive search range.")

    l_arith, p_arith, d_arith = detect_arithmetic_period(grundy_values)
    if p_arith is not None and p_arith <= max_n / 2:
        print(f"[Arithmetic Periodicity] Found: pre-period = {l_arith}, period = {p_arith}, saltus = {d_arith}")
        print_periodic_segment(grundy_values, l_arith, p_arith)
        title = f"Allbut({moves}), arith p={p_arith} d={d_arith}"
        plot_grundy_values(grundy_values, l_arith, p_arith, title, filename="out/allbut_arith")
    else:
        print("[Arithmetic Periodicity] No arithmetic period found in the naive search range.")
        

if __name__ == "__main__":
    main()

