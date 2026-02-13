import click, csv, time, datetime, itertools
from utils import predict_hash_algorithm, return_algorithm_name, initialize_hash_algo, hash_password

def brute_force_attack(verbose, to_crack_list, algorithm, min, max, skip_digits, skip_special):
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if not skip_digits:
        charset = charset + '0123456789'
    if not skip_special:
        charset = charset + '!@#$%^&*()_|[]-'

    if algorithm is None:
        predicted_algorithm = predict_hash_algorithm(to_crack_list[0])
        algorithm = return_algorithm_name(predicted_algorithm)

    i = 0
    for length in range(min, max + 1):  # Od długości 1 do max_length
        if verbose:
            print(f"Considering {length}-letter passwords...\n")

        for password_tuple in itertools.product(charset, repeat=length):
            plain = ''.join(password_tuple)
            i+=1
            if i % 10_000_000 == 0:
                # print(i, plain)
                pass

            hashed_password = hash_password(algorithm, plain)

            for target in to_crack_list:
                # hashed_password = hash_password(plain, hash_algo, target)
                if algorithm == 'mixed':
                    hashed_password = hash_password('mixed', plain, target)

                if hashed_password == target:
                    click.secho("Password cracked!", bg='green')
                    print(hashed_password, '->', plain)
                    cracked_list.append((hashed_password, plain))
                    to_crack_list.remove(hashed_password)
                if not to_crack_list:
                    return

    print("Brute force failed")
    return (cracked_list, to_crack_list) 



@click.command()
@click.argument('hashed_passwords', nargs=-1)
@click.option("-v", "--verbose", is_flag=True, help="Be more verbose")
@click.option(
    "-a", "--algorithm",
    type=click.Choice(['md5', 'sha1', 'sha256', 'mixed'], case_sensitive=False),
    help="Provide hashing algorithm. If not provided, the script will guess it by itself and assume all of the hashes use the same hashing algorithm."
)
@click.option(
    '--hash-file',
    type=click.Path(exists=True),
    default='to-crack.txt',
    help="Path to .txt file with passwords to crack."
)
@click.option('-o', '--output', type=click.Path(), default='output.csv', 
            help="Specify output file. If not provided, results will be saved to 'output.csv'."
)
@click.option("--brute-force", is_flag=True, default=False, help='Skip dictionary attack.')
@click.option("-m", "--min", type=click.IntRange(min=1), default=1, help='Minimal length of the password.')
@click.option("-M", "--max", type=click.IntRange(min=1), default=12, help='Maximal length of the password.')
@click.option("--skip-digits", is_flag=True, help="Assumes, passwords don't contain digits.")
@click.option("--skip-special", is_flag=True, help="Assumes, passwords don't contain special signs.")
def crack(hashed_passwords, verbose, algorithm, hash_file, output, brute_force, min, max, skip_digits, skip_special):

    start_time = time.time()

    global to_crack_list 
    to_crack_list=None #list of passwords left to crack
    if hashed_passwords:
        to_crack_list=list(hashed_passwords)
    else:
        with open(hash_file, 'r', encoding='utf-8') as f:
            hashed_passwords = f.readlines()
        to_crack_list = [line.strip() for line in hashed_passwords]
        
    if not to_crack_list:
        print(f"There are no passwords to crack in the {hash_file} file")
        return -1
    global cracked_list
    cracked_list = []

    if algorithm:
        algorithm = algorithm.lower()
    
    hash_algo = initialize_hash_algo(algorithm, to_crack_list)

    if brute_force:
        print("Starting at: ",datetime.datetime.now().time().strftime("%H:%M:%S"))

    if verbose and not algorithm:
        print("Detected hashing algorithm:", return_algorithm_name(hash_algo), '\n')

    with open('hashes.csv', 'r', encoding='utf-8') as csv_file, \
        open(output, 'w', newline='', encoding='utf-8') as output_file:

        csv_reader = csv.reader(csv_file)
        output_writer = csv.writer(output_file)
        output_writer.writerow(['hash','password'])

        if not brute_force:
            for row in csv_reader:
                for hash in to_crack_list:

                    if algorithm == 'mixed':
                        hash_algo = predict_hash_algorithm(hash)
                        if not hash_algo: continue

                    if row[hash_algo] == hash:
                        if verbose: 
                            click.secho("Password cracked!", bg='green')
                            print(hash, '->', row[0])
                        cracked_list.append((hash, row[0]))
                        output_writer.writerow((hash, row[0]))
                        to_crack_list.remove(hash)
                if len(cracked_list) == len(hashed_passwords):
                    break # stop the loop if all passwords have been cracked
            else:
                use_brute = input("\nSeems like some passwords less common. Do you want to use brute force? y/n ")
                print('\n')
                # todo: stop the time count here
                if use_brute == 'y':
                    print("Starting at: ",datetime.datetime.now().time().strftime("%H:%M:%S"))
                    brute_force_attack(verbose, to_crack_list, algorithm, min, max, skip_digits, skip_special)
        else:
            brute_force_attack(verbose, to_crack_list, algorithm, min, max, skip_digits, skip_special)

        if verbose:
            n_cracked = len(cracked_list)
            n_not_cracked = len(to_crack_list)
            cracked_percent = round(n_cracked/(n_cracked+n_not_cracked)*100,2)
            not_cracked_percent = round(n_not_cracked/(n_cracked+n_not_cracked)*100,2)

            fg_color = 'green' if not to_crack_list else ('red' if n_cracked == 0 else 'yellow')
            click.secho("\n======================", fg=fg_color)
            print("Cracked:",n_cracked, f"({cracked_percent}%)")
            print("Not Cracked:",n_not_cracked, f"({not_cracked_percent}%)")
            click.secho("======================\n", fg=fg_color)

            if n_not_cracked:
                print("List of not cracked passwords:")
                for hash in to_crack_list:
                    print(' ',hash)
            if n_cracked == 0:
                click.secho("None of the passwords have been cracked", bg='red')
            if not to_crack_list: 
                click.secho("All passwords have been cracked! Check the output.csv file.", bg='green')
        else:
            for item in cracked_list:
                print(item[0], '->', item[1]) 
            if not cracked_list:
                click.secho("Couldn't crack any password", fg='red')


        end_time = time.time()
        if verbose:
            elapsed_time = end_time - start_time
            if elapsed_time > 1: elapsed_time = int(elapsed_time)
            print(f"\nTime elapsed: {elapsed_time} seconds")


if __name__ == '__main__':
    crack()
