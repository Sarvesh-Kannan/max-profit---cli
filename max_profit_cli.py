#!/usr/bin/env python3
"""
Max Profit Solver - Command Line Interface
A standalone tool to solve the maximum profit building construction problem.
"""

from typing import Tuple, List, Dict
import argparse
#import sys
#from datetime import datetime

# Building configurations
BUILDINGS = {
    'Theatre': {'time': 5, 'earning': 1500, 'code': 'T'},
    'Pub': {'time': 4, 'earning': 1000, 'code': 'P'},
    'Commercial Park': {'time': 10, 'earning': 3000, 'code': 'C'}
}

class MaxProfitSolver:
    def __init__(self):
        self.memo = {}
    
    def solve_dp_all_solutions(self, time_units: int) -> Tuple[int, List[Dict[str, int]]]:
        """
        Dynamic Programming solution to find maximum profit and ALL optimal solutions
        Key insight: Building earns money for each period it's operational after construction
        """
        # dp[i] = (max_profit, list_of_all_optimal_solutions)
        dp = [(0, [{'Theatre': 0, 'Pub': 0, 'Commercial Park': 0}] )] * (time_units + 1)
        
        for t in range(1, time_units + 1):
            max_profit = dp[t-1][0]
            best_solutions = list(dp[t-1][1])  # Copy previous solutions (do nothing)
            
            for building, config in BUILDINGS.items():
                build_time = config['time']
                earning = config['earning']
                
                if t >= build_time:
                    # Building finishes construction at time t
                    # It earns for periods (t+1, t+2, ..., time_units) => (time_units - t) periods
                    operational_periods = time_units - t
                    total_earning = earning * operational_periods
                    
                    prev_profit, prev_solutions = dp[t - build_time]
                    new_profit = prev_profit + total_earning
                    
                    if new_profit > max_profit:
                        max_profit = new_profit
                        best_solutions = []
                        for prev_solution in prev_solutions:
                            new_solution = prev_solution.copy()
                            new_solution[building] += 1
                            best_solutions.append(new_solution)
                    elif new_profit == max_profit:
                        for prev_solution in prev_solutions:
                            new_solution = prev_solution.copy()
                            new_solution[building] += 1
                            if new_solution not in best_solutions:
                                best_solutions.append(new_solution)
            
            dp[t] = (max_profit, best_solutions)
        
        return dp[time_units]
    
    def calculate_profit(self, time_units: int, solution: Dict[str, int]) -> int:
        """Calculate the total profit for a given solution"""
        total_profit = 0
        current_time = 0
        
        for building, count in solution.items():
            if count > 0:
                config = BUILDINGS[building]
                build_time = config['time']
                earning_per_period = config['earning']
                
                for _ in range(count):
                    construction_end_time = current_time + build_time
                    current_time = construction_end_time
                    operational_periods = time_units - construction_end_time
                    if operational_periods > 0:
                        building_profit = earning_per_period * operational_periods
                        total_profit += building_profit
        
        return total_profit
    
    def validate_solution(self, time_units: int, solution: Dict[str, int]) -> Tuple[bool, int, str]:
        """
        Validate if the solution is correct
        Returns: (is_valid, calculated_profit, message)
        """
        total_profit = 0
        current_time = 0
        
        for building, count in solution.items():
            if count > 0:
                config = BUILDINGS[building]
                build_time = config['time']
                earning_per_period = config['earning']
                
                for _ in range(count):
                    construction_end_time = current_time + build_time
                    current_time = construction_end_time
                    operational_periods = time_units - construction_end_time
                    if operational_periods > 0:
                        building_profit = earning_per_period * operational_periods
                        total_profit += building_profit
        
        total_time_used = current_time
        is_valid = total_time_used <= time_units
        message = f"Time used: {total_time_used}/{time_units}, Profit: ${total_profit:,}"
        
        return is_valid, total_profit, message

def format_solution(solution: Dict[str, int]) -> str:
    """Format solution as 'T: 1 P: 0 C: 0' format"""
    codes = []
    for building in ['Theatre', 'Pub', 'Commercial Park']:
        code = BUILDINGS[building]['code']
        count = solution[building]
        codes.append(f"{code}: {count}")
    return " ".join(codes)

def print_header():
    """Print application header"""
    print("=" * 80)
    print("🏗️  MAXIMUM PROFIT BUILDING CONSTRUCTION SOLVER")
    print("=" * 80)
    print("Building Types:")
    for building, config in BUILDINGS.items():
        print(f"  • {building} ({config['code']}): {config['time']} time units, ${config['earning']:,}/period")
    print("=" * 80)

def print_solution_details(time_units: int, solution: Dict[str, int], solution_idx: int, solver: MaxProfitSolver):
    """Print detailed information about a specific solution"""
    print(f"\n📋 SOLUTION #{solution_idx + 1}")
    print("-" * 40)
    
    # Format solution
    formatted = format_solution(solution)
    print(f"Building Configuration: {formatted}")
    
    # Validate and get details
    is_valid, calculated_profit, message = solver.validate_solution(time_units, solution)
    print(f"Validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
    print(f"Details: {message}")
    
    # Show construction timeline
    print("\n🏗️  Construction Timeline:")
    current_time = 0
    for building, count in solution.items():
        if count > 0:
            build_time = BUILDINGS[building]['time']
            for i in range(count):
                start_time = current_time
                end_time = current_time + build_time
                operational_periods = time_units - end_time
                period_earning = BUILDINGS[building]['earning']
                total_earning = period_earning * operational_periods if operational_periods > 0 else 0
                
                print(f"  {building} #{i+1}: Time {start_time}-{end_time} "
                      f"(Earns ${period_earning:,}/period for {operational_periods} periods = ${total_earning:,})")
                current_time = end_time
    
    if current_time == 0:
        print("  No buildings constructed")

def print_summary(time_units: int, max_profit: int, solutions: List[Dict[str, int]], solver: MaxProfitSolver):
    """Print summary of all solutions"""
    print(f"\n📊 SUMMARY")
    print("=" * 80)
    print(f"Time Units Available: {time_units}")
    print(f"Maximum Profit: ${max_profit:,}")
    print(f"Number of Optimal Solutions: {len(solutions)}")
    
    if len(solutions) > 1:
        print(f"\n🏆 All Optimal Solutions:")
        for i, solution in enumerate(solutions):
            formatted = format_solution(solution)
            is_valid, calculated_profit, _ = solver.validate_solution(time_units, solution)
            status = "✅" if is_valid else "❌"
            print(f"  {status} Solution {i+1}: {formatted} (Profit: ${calculated_profit:,})")
    else:
        print(f"\n🏆 Optimal Solution:")
        formatted = format_solution(solutions[0])
        is_valid, calculated_profit, _ = solver.validate_solution(time_units, solutions[0])
        status = "✅" if is_valid else "❌"
        print(f"  {status} {formatted} (Profit: ${calculated_profit:,})")

def interactive_mode():
    """Run the solver in interactive mode"""
    print_header()
    
    while True:
        try:
            print(f"\n⏰ Enter time units (1-100, or 'q' to quit): ", end="")
            user_input = input().strip()
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("\n👋 Goodbye!")
                break
            
            time_units = int(user_input)
            if time_units < 1 or time_units > 100:
                print("❌ Please enter a number between 1 and 100.")
                continue
            
            # Solve the problem
            print(f"\n🔍 Solving for {time_units} time units...")
            solver = MaxProfitSolver()
            max_profit, all_solutions = solver.solve_dp_all_solutions(time_units)
            
            # Print results
            print_summary(time_units, max_profit, all_solutions, solver)
            
            # Ask if user wants detailed view
            if len(all_solutions) > 0:
                print(f"\n📋 Show detailed breakdown? (y/n): ", end="")
                show_details = input().strip().lower()
                if show_details in ['y', 'yes']:
                    for i, solution in enumerate(all_solutions):
                        print_solution_details(time_units, solution, i, solver)
            
            print("\n" + "=" * 80)
            
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

def batch_mode(time_units: int, detailed: bool = False):
    """Run the solver for a specific time value"""
    print_header()
    
    print(f"\n⏰ Time Units: {time_units}")
    print(f"🔍 Solving...")
    
    solver = MaxProfitSolver()
    max_profit, all_solutions = solver.solve_dp_all_solutions(time_units)
    
    print_summary(time_units, max_profit, all_solutions, solver)
    
    if detailed and len(all_solutions) > 0:
        for i, solution in enumerate(all_solutions):
            print_solution_details(time_units, solution, i, solver)

def main():
    """Main function to handle command line arguments and run the solver"""
    parser = argparse.ArgumentParser(
        description="Maximum Profit Building Construction Solver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python max_profit_cli.py                    # Interactive mode
  python max_profit_cli.py 20                 # Solve for 20 time units
  python max_profit_cli.py 20 --detailed      # Solve with detailed breakdown
  python max_profit_cli.py --help             # Show this help message
        """
    )
    
    parser.add_argument(
        'time_units', 
        nargs='?', 
        type=int, 
        help='Number of time units (1-100). If not provided, runs in interactive mode.'
    )
    
    parser.add_argument(
        '--detailed', 
        action='store_true', 
        help='Show detailed breakdown of each solution'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='Max Profit Solver v1.0'
    )
    
    args = parser.parse_args()
    
    try:
        if args.time_units is None:
            # Interactive mode
            interactive_mode()
        else:
            # Batch mode
            if args.time_units < 1 or args.time_units > 100:
                print("❌ Error: Time units must be between 1 and 100.")
                sys.exit(1)
            
            batch_mode(args.time_units, args.detailed)
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 