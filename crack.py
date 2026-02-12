import click, csv, time

def predict_hash_algorithm(hash_str: str) -> int | None:
    """
    Predicts the hashing algorithm
    Returns:
        1 - MD5
        2 - SHA1
        3 - SHA256
        None - unknown
    """
    hash_str = hash_str.lower()  # To ensure letters are lower case
    # Check if hex
    if not all(c in "0123456789abcdef" for c in hash_str):
        return "Unknown"

    length = len(hash_str)
    if length == 32:
        return 1
    elif length == 40:
        return 2
    elif length == 64:
        return 3
    else:
        return None


def return_algorithm_name(i: int) -> str:
    if i == 1:
        return 'MD5'
    if i == 2:
        return 'SHA1'
    if i == 3:
        return 'SHA256'

@click.command()
@click.option("-v", "--verbose", is_flag=True, help="Be more verbose")
@click.option(
    "--algorithm",
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
def hello(verbose, algorithm, hash_file, output):

    start_time = time.time()
    with open(hash_file, 'r', encoding='utf-8') as f:
        hashed_passwords = f.readlines()
    to_crack_list = [line.strip() for line in hashed_passwords]
    if not to_crack_list:
        print(f"There are no passwords to crack in the {hash_file} file")
        return -1
    cracked_list = []
    
    match algorithm:
        case 'md5':
            hash_algo = 1
        case 'sha1':
            hash_algo = 2
        case 'sha256':
            hash_algo = 3
        case None:
            hash_algo = predict_hash_algorithm(to_crack_list[0])
        case _:
            hash_algo = None

    if verbose and not algorithm:
        print("Detected hashing algorithm:", return_algorithm_name(hash_algo), '\n')

    with open('hashes.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
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
                    to_crack_list.remove(hash)
            if len(cracked_list) == len(hashed_passwords):
                break # stop the loop if all passwords have been cracked
            

        if verbose:
            n_cracked = len(cracked_list)
            n_not_cracked = len(to_crack_list)
            fg_color = 'green' if not to_crack_list else ('red' if n_cracked == 0 else 'yellow')
            click.secho("\n======================", fg=fg_color)
            print("Cracked:",n_cracked, f"({n_cracked/(n_cracked+n_not_cracked)*100}%)")
            print("Not Cracked:",n_not_cracked, f"({n_not_cracked/(n_cracked+n_not_cracked)*100}%)")
            click.secho("======================\n", fg=fg_color)
            if n_not_cracked:
                print("List of not cracked passwords:", to_crack_list)
            if not to_crack_list: 
                click.secho("All passwords have been cracked! Check the output.csv file.", bg='green')
        else:
            for item in cracked_list:
                print(item[0], '->', item[1]) 
            if not cracked_list:
                click.secho("Couldn't crack any password", fg='red')

        # todo: move this up
        with open(output, 'w', newline='', encoding='utf-8') as o:
            writer = csv.writer(o)
            writer.writerow(['hash','password'])
            for item in cracked_list:
                writer.writerow(item)

        end_time = time.time()
        if verbose:
            elapsed_time = end_time - start_time
            if elapsed_time > 1: elapsed_time = int(elapsed_time)
            print(f"\nTime elapsed: {elapsed_time} seconds")


if __name__ == '__main__':
    hello()
