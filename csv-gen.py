# This script generates csv look-up table of most common passwords and their hashes computed using various hashing algorithms

import hashlib
import csv

with open("passwords.txt", 'r', encoding='utf-8') as file, \
     open('hashes.csv', 'w', newline='', encoding='utf-8') as out_csv:

    writer = csv.writer(out_csv)
    writer.writerow(['plain', 'md5', 'sha1', 'sha256'])

    for line in file:
        plain = line.strip()
        data = plain.encode()

        writer.writerow([
            plain,
            hashlib.md5(data).hexdigest(),
            hashlib.sha1(data).hexdigest(),
            hashlib.sha256(data).hexdigest()
        ])


