import click, csv

@click.command()
def hello():
    with open('to-crack.txt', 'r', encoding='utf-8') as f:
        to_crack_list = f.readlines()
    to_crack_list = [line.strip() for line in to_crack_list]
    cracked_list = []

    with open('hashes.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            for hash in to_crack_list:

                if row[1] == hash:
                    print("Password cracked!", hash, '->', row[0])
                    cracked_list.append((hash, row[0]))
                    to_crack_list.remove(hash)
            if len(cracked_list) == len(to_crack_list):
                break # stop the loop if all passwords have been cracked
            
        print(cracked_list)


if __name__ == '__main__':
    hello()
