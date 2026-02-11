import click, csv

@click.command()
@click.option("-v", "--verbose", is_flag=True, help="Be more verbose")
def hello(verbose):
    with open('to-crack.txt', 'r', encoding='utf-8') as f:
        to_crack_list = f.readlines()
    to_crack_list = [line.strip() for line in to_crack_list]
    cracked_list = []

    with open('hashes.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            for hash in to_crack_list:

                if row[1] == hash:
                    if verbose: print("Password cracked!")
                    print(hash, '->', row[0])
                    cracked_list.append((hash, row[0]))
                    to_crack_list.remove(hash)
            if len(cracked_list) == len(to_crack_list):
                break # stop the loop if all passwords have been cracked
            
        print(cracked_list)

        if verbose:
            if to_crack_list:
                n_cracked = len(cracked_list)
                n_not_cracked = len(to_crack_list)
                print("Cracked:",n_cracked, f"({n_cracked/(n_cracked+n_not_cracked)*100}%)")
                print("Not Cracked:",n_not_cracked, f"({n_not_cracked/(n_cracked+n_not_cracked)*100}%)")
                print("List of cracked passwords:", cracked_list)
                print("List of not cracked passwords:", to_crack_list)
            else: 
                print("All passwords have been cracked!")
                print("List of cracked passwords:", cracked_list)


if __name__ == '__main__':
    hello()
