import sys
import os
import signal

#Me, caveman like color
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
        if conv == 'all':
            conv_list = ['dot', 'dash', 'underscore']
        else:
            conv_list = [conv]

        for convention in conv_list:
            symbol = convention_symbols[convention]

            if symbol:
                concatenations.append(name + symbol + surname)
                concatenations.append(surname + symbol + name)
                concatenations.append(name[0] + symbol + surname)
                concatenations.append(surname[0] + symbol + name)
                concatenations.append(name[0] + symbol + surname[0])
                concatenations.append(surname[0] + symbol + name[0])
                concatenations.append(name[:3] + symbol + surname[:3])
                concatenations.append(surname[:3] + symbol + name[:3])
                concatenations.append(name[:3] + symbol + surname)
                concatenations.append(surname[:3] + symbol + name)
                concatenations.append(surname + symbol + name[:3])
                concatenations.append(name + symbol + surname[:3])

            concatenations.extend([
                name + surname[0],
                surname + name[0],
                name + surname,
                surname + name,

            ])


            if include_numbers:
                for i in range(1000):
                    concatenations.append(name + symbol + str(i) + surname)
                    concatenations.append(surname + symbol + str(i) + name)
                    concatenations.append(name + symbol + surname + str(i))
                    concatenations.append(surname + symbol + name + str(i))
                    concatenations.append(name + symbol + str(i) + surname)
                    concatenations.append(surname + symbol + str(i) + name)
                    concatenations.append(name[0] + symbol + surname + str(i))
                    concatenations.append(surname[0] + symbol + name + str(i))
                    concatenations.append(name[0] + symbol + surname[0] + str(i))
                    concatenations.append(surname[0] + symbol + name[0] + str(i))
                    concatenations.append(name[:3] + symbol + surname[:3] + str(i))
                    concatenations.append(name[:3] + symbol + surname[:3] + str(i))
                    concatenations.append(name + symbol + surname[0] + str(i))
                    concatenations.append(surname + symbol + name[0] + str(i))
                    concatenations.append(name[:3] + symbol + surname[:3] + str(i))
                    concatenations.append(surname[:3] + symbol + name[:3] + str(i))
                    concatenations.append(name[:3] + symbol + surname + str(i))
                    concatenations.append(surname[:3] + symbol + name + str(i))
                    concatenations.append(surname + symbol + name[:3] + str(i))
                    concatenations.append(name + symbol + surname[:3] + str(i))

                    concatenations.extend([
                        name + surname[0] + str(i),
                        surname + name[0] + str(i),
                        name + surname + str(i),
                        surname + name + str(i),
                        surname[0] + name[0] + str(i),
                        name[0] + surname[0] + str(i),
                        name[:3] + surname[:3] + str(i),
                        surname[:3] + name[:3] + str(i),
                        name[:3] + surname + str(i),
                        surname[:3] + name + str(i),
                        surname + name[:3] + str(i),
                        name + surname[:3] + str(i),
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
                name, surname = line.strip().lower().split()
                concatenations = generate_concatenations(name, surname, conventions, include_numbers)

                for concat_string in concatenations:
                    out_file.write(f"{concat_string}\n")
                    
        print(GREEN + "\nGenerated combinations saved to --> " + END + YELLOW + f"{output_file}" + END + BLUE + "\nHappy Hacking!" + END)
          
    except FileNotFoundError:
        print(RED + f"\nInput file '{filename}' not found." + END)
        sys.exit(1)
    except Exception as e:
        print(RED + "An error occurred:", e + END)
        sys.exit(1)

def signal_handler(sig, frame):
    print(RED + '\n[!] Exiting...' + END)
    sys.exit(1)

signal.signal(signal.SIGINT, signal.SIG_DFL)

def main():
    if len(sys.argv) < 2:
        print("\nUsage: [usergenerator.py] [userlistFile] [options]")
        print(GREEN + '[!] Name and surname in the user list should be separated by a space' + END)

        print(BLUE + 'Example usage:' + END + ' python3 usernamegenerator.py users.txt -c dot underscore -o output_file.txt\n')

        print("-c {all}{dot}{dash}{underscore} --> Specify a convention used in concatenations (Can use multiple)")
        print('-n --> Generate combinations using numbers from 0 to 999 at the end of the string, off by default')
        print('-o --> Output file (Default: generated_users.txt)')

        sys.exit(0)

    input_file = sys.argv[1]
    output_file = 'generated_users.txt'
    conventions = ['dot']  
    include_numbers = '-n' in sys.argv


    if '-o' in sys.argv:
        try:
            output_index = sys.argv.index('-o') + 1
            output_file = sys.argv[output_index]
        except IndexError:
            print("Output file name is missing after -o")
            sys.exit(1)


    if '-c' in sys.argv:
        try:
            convention_index = sys.argv.index('-c')
            conventions_args = sys.argv[convention_index + 1:]
            conventions = []
                  
            seen = set()
            for arg in conventions_args:
                if arg.startswith('-'):
                    break
                if arg not in seen:
                    conventions.append(arg)
                    seen.add(arg)
                else:
                    print(RED + f"\nRepeated convention detected --> {seen} Interrupted to avoid filling your disk!" + END)
                    sys.exit(1)

            if len(conventions) > 3:
                print(RED + "\nToo many conventions. Use 1,2 or ALL. Interrupted to avoid filling your disk!" + END)
                sys.exit(1)

            valid_conventions = {'dot', 'dash', 'underscore', 'all'}
            if not all(convention in valid_conventions for convention in conventions):
                print(RED + "\nInvalid convention." + END + GREEN + " Available options: all, dot, dash, underscore" + END + BLUE + " (I will use dot by default)" + END)
                sys.exit(1)
        except IndexError:
            print("Convention name is missing after -c")
            sys.exit(1)
    else:
        conventions = ['dot']

    generate_user_combinations(input_file, output_file, include_numbers, conventions)


if __name__ == '__main__':
    main()
