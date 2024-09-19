import argparse
import os
import signal
import sys

# Me, caveman like color
RED = "\033[91m"
GREEN = "\033[92m"
END = "\033[0m"
BLUE = "\033[94m"
YELLOW = "\033[93m"

def generate_concatenations(name, surname, conventions, include_numbers=False):
    concatenations = []
    convention_symbols = {
        'dot': '.',
        'dash': '-',
        'underscore': '_',
    }

    for conv in conventions:
        conv_list = ['dot', 'dash', 'underscore'] if conv == 'all' else [conv]

        for convention in conv_list:
            symbol = convention_symbols[convention]

            concatenations.extend([
                f"{name}{symbol}{surname}", f"{surname}{symbol}{name}",
                f"{name[0]}{symbol}{surname}", f"{surname[0]}{symbol}{name}",
                f"{name[0]}{symbol}{surname[0]}", f"{surname[0]}{symbol}{name[0]}",
                f"{name[:3]}{symbol}{surname[:3]}", f"{surname[:3]}{symbol}{name[:3]}",
                f"{name[:3]}{symbol}{surname}", f"{surname[:3]}{symbol}{name}",
                f"{surname}{symbol}{name[:3]}", f"{name}{symbol}{surname[:3]}"
            ])

            concatenations.extend([f"{name}{surname[0]}", f"{surname}{name[0]}", f"{name}{surname}", f"{surname}{name}"])

            if include_numbers:
                for i in range(1000):
                    concatenations.extend([
                        f"{name}{symbol}{i}{surname}", f"{surname}{symbol}{i}{name}",
                        f"{name}{symbol}{surname}{i}", f"{surname}{symbol}{name}{i}",
                        f"{name[0]}{symbol}{surname}{i}", f"{surname[0]}{symbol}{name}{i}",
                        f"{name[:3]}{symbol}{surname[:3]}{i}", f"{surname[:3]}{symbol}{name[:3]}{i}",
                        f"{name}{surname[0]}{i}", f"{surname}{name[0]}{i}",
                        f"{name}{surname}{i}", f"{surname}{name}{i}",
                    ])
    return concatenations

def generate_user_combinations(filename, output_file, include_numbers=False, conventions=['dot']):
    try:
        if os.path.exists(output_file):
            choice = input(RED + f"The output file '{output_file}' already exists. Do you want to overwrite it?" + END + GREEN + " (y/N): " + END)
            if choice.lower() != 'y':
                print("Exiting without overwriting the file. You can use -o to specify a different output file.")
                sys.exit(0)

        with open(filename, 'r') as f, open(output_file, 'w') as out_file:
            for line in f:
                try:
                    name, surname = line.strip().lower().split()
                    concatenations = generate_concatenations(name, surname, conventions, include_numbers)
                    out_file.write("\n".join(concatenations) + "\n")
                except ValueError:
                    print(RED + f"Skipping malformed line: {line.strip()}" + END)
                    
        print(GREEN + "\nGenerated combinations saved to --> " + END + YELLOW + f"{output_file}" + END + BLUE + "\nHappy Hacking!" + END)
          
    except FileNotFoundError:
        print(RED + f"\nInput file '{filename}' not found." + END)
        sys.exit(1)
    except Exception as e:
        print(RED + f"An error occurred: {e}" + END)
        sys.exit(1)

def signal_handler(sig, frame):
    print(RED + '\n[!] Exiting...' + END)
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def main():
    parser = argparse.ArgumentParser(description='Generate username combinations from name and surname pairs in a file.')
    parser.add_argument('input_file', type=str, help='Input file containing names and surnames.')
    parser.add_argument('-o', '--output', type=str, default='generated_users.txt', help='Output file (default: generated_users.txt)')
    parser.add_argument('-n', '--numbers', action='store_true', help='Include numbers in the generated combinations.')
    parser.add_argument('-c', '--convention', type=str, nargs='+', default=['dot'], choices=['dot', 'dash', 'underscore', 'all'],
                        help='Specify convention(s) for username generation. Choices: dot, dash, underscore, all. (default: dot)')

    args = parser.parse_args()

    conventions = args.convention
    if len(conventions) > 3:
        print(RED + "\nToo many conventions. Use up to 3 or ALL." + END)
        sys.exit(1)

    generate_user_combinations(args.input_file, args.output, args.numbers, conventions)

if __name__ == '__main__':
    main()
