import hashlib
import itertools

#hashlib.sha256(line.strip().encode()).hexdigest()
def main():
    cont = True
    while cont == True:
        choice = input("What type of attack?\n1. Dictionary\n2. Random String Brute Force (up to 6char)\n3. Word w/trail\n4. Common Passwords\n5. Quit\n>")
        if choice == '1':
            randCapWord()
        if choice == '2':
            strBF()
        if choice == '3':
            trail()
        if choice == '4':
            commonPW()
        if choice == '5':
            cont = False

def randCapWord():
    print("Dictionary Attack - Random caps")
    hashes = open("hashes.txt", "r")
    out = open("cracked.txt", "a")
    # Build array of hashes to check against
    hashList = []
    for h in hashes:
        hashList.append(h)
    with open("english_words.txt", "r") as pwlist:
        for password in pwlist:
            combList = map("".join, itertools.product(*((char.upper(), char.lower()) for char in password)))
            for word in combList:
                encoded = hashlib.sha256(word.strip().encode()).hexdigest()
                for hash in hashList:
                    if(encoded.strip() == hash.strip()):
                        print(encoded+":"+password)
                        out.write(encoded + ":" + password)
    out.close()


def strBF():
    print("String brute force\n--WARNING: THIS WILL TAKE A LONG TIME")
    hashes = open("hashes.txt", "r")
    out = open("cracked.txt", "a")
    # Build array of hashes to check against
    hashList = []
    for h in hashes:
        hashList.append(h)
    asciiList = []
    for char in range(33, 126):
        asciiList.append(''.join(chr(char)))
    status = 1
    for i in range(1, 6):
        for tup in itertools.combinations_with_replacement(asciiList, i):
            if(status != i):
                print(str(status) + " keyspace completed")
                status = i
            encoded = hashlib.sha256("".join(tup).strip().encode()).hexdigest()
            for hash in hashList:
                if(encoded.strip() == hash.strip()):
                    print(encoded + ":" + "".join(tup))
                    out.write("\n" + encoded + ":" + "".join(tup))
    out.close()


def trail():
    print("Dict with trail")
    hashes = open("hashes.txt", "r")
    out = open("cracked.txt", "a")
    # Ranges for Non-alpha ascii codes
    l1 = range(33,64)
    l2 = range(91,96)
    l3 = range(123,126)
    # Build array of hashes to check against
    hashList = []
    for h in hashes:
        hashList.append(h)
    with open("english_words.txt", "r") as pwlist:
        for password in pwlist:
            trailList = itertools.combinations_with_replacement(list(chr(ascii) for ascii in itertools.chain(l1,l2,l3)), 4)
            for trail in trailList:
                encoded = hashlib.sha256((password.strip() + "".join(trail).strip()).encode()).hexdigest()
                for hash in hashList:
                    if(encoded.strip() == hash.strip()):
                        print(encoded+":"+password)
                        out.write(encoded + ":" + password)
    out.close()


def commonPW():
    print("Common Passwords")
    out = open("cracked.txt", "a")
    with open("cracked.txt", "a") as out:
        with open("passwords.txt", "r") as pwlist:
            hashes = open("hashes.txt", "r")
            hashList = []
            for h in hashes:
                hashList.append(h)
            for password in pwlist:
                encoded = hashlib.sha256(password.strip().encode()).hexdigest()
                for hash in hashList:
                    if(encoded.strip() == hash.strip()):
                        print(encoded+":"+password)
                        out.write(encoded + ":" + password)
    out.close()

def twoWords():
    print("Two words smashed together")
    with open("cracked.txt","a") as out:
        wordList = open("english_lc.txt", "r")
        hashes = open("hashes.txt", "r")
        hashList = []
        for h in hashes:
            hashList.append(h)
        wordArray = []
        for word in wordList:
            wordArray.append(word.strip())
            wordArray.append(word.title().strip())
        for password in itertools.combinations(wordArray, 2):
            encoded = hashlib.sha256("".join(password).strip().encode())
            for hash in hashes:
                if(hash.strip() == encoded.strip()):
                    print(encoded+":"+password)
                    out.write(encoded+":"+password)
    out.close()


def all():
    commonPW()
    strBF()
    randCapWord()
    trail()
    twoWords()


if __name__ == "__main__":
    main()