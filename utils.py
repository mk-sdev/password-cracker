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
        return 'md5'
    if i == 2:
        return 'sha1'
    if i == 3:
        return 'sha256'
    

def initialize_hash_algo(algorithm, to_crack_list) -> int | None:
    match algorithm:
        case 'md5':
            return 1
        case 'sha1':
            return 2
        case 'sha256':
            return 3
        case None:
            return predict_hash_algorithm(to_crack_list[0])
        case _:
            return None