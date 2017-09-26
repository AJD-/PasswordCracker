import hashlib
import itertools
import threading

#hashlib.sha256(line.strip().encode()).hexdigest()
def main():
    cont = True
    while cont:
        choice = input("What type of attack?\n1. Dictionary w/random caps\n2. Random String Brute Force (up to 6char)\n3. Word w/trail\n4. Common Passwords\n5. Dictionary Attack\n6. Trailing number\n7. Two Words\n8. Run All (Multi-Threaded)\n9. Quit\n>")
        if choice == '1':
            randCapWord(True)
        if choice == '2':
            strBF(True)
        if choice == '3':
            trail(True)
        if choice == '4':
            commonPW(True)
        if choice == '5':
            dict(True)
        if choice == '6':
            numTrail(True)
        if choice == '7':
            twoWords(True)
        if choice =='8':
            all()
        if choice == '9':
            cont = False

def randCapWord(verbose):
    print("Dictionary Attack - Random caps - This will take a long time depending on the file")
    outName = "cracked-caps.txt"
    hashes = open("hashes.txt", "r")    
    # Build array of hashes to check against
    hashList = []
    for h in hashes:
        hashList.append(h)
    hashes.close()
    with open("google-10000-english.txt", "r") as pwlist:
        index = 0
        for password in pwlist:
            # Get every combination of upper and lowercase letters in each word
            combList = map("".join, itertools.product(*((char.upper(), char.lower()) for char in password)))
            for word in combList:
                encoded = hashlib.sha256(word.strip().encode()).hexdigest()
                for hash in hashList:
                    checkHash(encoded, hash, password.strip(), outName)
                index += 1
                if((index % 100000 == 0) and verbose):
                    print(str(index) + " words checked")


def strBF(verbose):
    print("String brute force\n--WARNING: THIS WILL TAKE A LONG TIME")
    hashes = open("hashes.txt", "r")
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
                    out = open("cracked-bf.txt", "a")
                    print(encoded + ":" + "".join(tup))
                    out.write(encoded + ":" + "".join(tup)+"\n")
                    out.close()


def trail(verbose):
    print("Dict with trail")
    outName = "cracked-trail.txt"
    hashes = open("hashes.txt", "r")        
    # Ranges for Non-alpha ascii codes
    l1 = range(33,64)
    l2 = range(91,96)
    l3 = range(123,126)
    # Build array of hashes to check against
    hashList = []
    for h in hashes:
        hashList.append(h)
    pwlist = open("google-10000-english.txt", "r")
    wordArray = []
    for word in pwlist:
        wordArray.append(word.strip())
        wordArray.append(word.title().strip())
    pwlist.close()
    index = 0
    trailArr = []
    for password in wordArray:
        index += 1
        trailArr.append(itertools.combinations_with_replacement(list(chr(ascii) for ascii in itertools.chain(l1,l2,l3)), 1))
        trailArr.append(itertools.combinations_with_replacement(list(chr(ascii) for ascii in itertools.chain(l1,l2,l3)), 2))
        trailArr.append(itertools.combinations_with_replacement(list(chr(ascii) for ascii in itertools.chain(l1,l2,l3)), 3))
        trailArr.append(itertools.combinations_with_replacement(list(chr(ascii) for ascii in itertools.chain(l1,l2,l3)), 4))
        for trailList in trailArr:
            for trail in trailList:
                encoded = hashlib.sha256((password.strip() + "".join(trail).strip()).encode()).hexdigest()
                for hash in hashList:
                    checkHash(encoded, hash, password, outName)
            if(index % 10000 == 0 and verbose):
                print(str(index) + " words completed")
    out.close()


def commonPW(verbose):
    print("Common Passwords")
    outName = "cracked-common.txt"
    with open("passwords.txt", "r") as pwlist:
        hashes = open("hashes.txt", "r")
        hashList = []
        for h in hashes:
            hashList.append(h)
        for password in pwlist:
            encoded = hashlib.sha256(password.strip().encode()).hexdigest()
            for hash in hashList:
                checkHash(encoded, hash, password.strip(), outName)

def twoWords(verbose):
    print("Two words smashed together")
    wordList = open("english_lc.txt", "r")
    hashes = open("hashes.txt", "r")
    hashList = []
    for h in hashes:
        hashList.append(h)
    wordArray = []
    index = 0
    for word in wordList:
        index += 1
        wordArray.append(word.strip())
        wordArray.append(word.title().strip())
    for password in itertools.combinations(wordArray, 2):
        encoded = hashlib.sha256("".join(password).strip().encode())
        for hash in hashes:
            checkHash(encoded, hash, "".join(password).strip())
        if(index%5000 == 0 and verbose):
            print(str(index) + " words completed")


def dict(verbose):
    print("Standard dictionary attack - only checks title case/lowercase")
    outName = "cracked-dictionary-std.txt"
    wordList = open("english_lc.txt", "r")
    hashes = open("hashes.txt", "r")
    hashList = []
    for h in hashes:
        hashList.append(h)
    hashes.close()
    wordArray = []
    for word in wordList:
        wordArray.append(word.strip())
        wordArray.append(word.title().strip())
    wordList.close()
    index = 0
    for password in wordArray:
        index += 1
        encoded = hashlib.sha256(password.strip().encode()).hexdigest()
        for hash in hashList:
            checkHash(encoded, hash, password, outName)
        if(index % 5000 == 0 and verbose):
            print(str(index) + " words completed")


def numTrail(verbose):
    print("Dictionary attack with trailing number")
    outName = "cracked-dictwTrail.txt"
    wordList = open("google-10000-english.txt", "r")
    hashes = open("hashes.txt", "r")
    hashList = []
    wordArray = []
    for h in hashes:
        hashList.append(h)
    for word in wordList:
        wordArray.append(word.strip())
        wordArray.append(word.title().strip())
    wordList.close()
    index = 0
    trailListArr = []
    for password in wordArray:
        trailListArr.append(itertools.combinations_with_replacement(['0','1','2','3','4','5','6','7','8','9'], 4))
        trailListArr.append(itertools.combinations_with_replacement(['0','1','2','3','4','5','6','7','8','9'], 3))
        trailListArr.append(itertools.combinations_with_replacement(['0','1','2','3','4','5','6','7','8','9'], 2))
        trailListArr.append(itertools.combinations_with_replacement(['0','1','2','3','4','5','6','7','8','9'], 1))
        index += 1
        for trailList in trailListArr:
            for trail in trailList:
                encoded = hashlib.sha256((password.strip() + "".join(str(trail))).encode()).hexdigest()
                for hash in hashList:
                    checkHash(encoded, hash, password, outName)
        if(index % 5000 == 0 and verbose):
            print(str(index) + " words completed")


def checkHash(encoded, hash, password, outName):
    if(encoded.strip() == hash.strip()):
        lock = threading.Lock()
        lock.acquire()
        out = open(outName, "a")
        print(encoded+":"+password)
        out.write(encoded + ":" + password+"\n")
        out.close()
        lock.release()


def all():
    threads = []
    threads.append(threading.Thread(target=commonPW, args=(False,)))
    threads.append(threading.Thread(target=strBF, args=(False,)))
    threads.append(threading.Thread(target=randCapWord, args=(False,)))
    threads.append(threading.Thread(target=trail, args=(False,)))
    threads.append(threading.Thread(target=twoWords, args=(False,)))
    threads.append(threading.Thread(target=dict, args=(False,)))
    for thr in threads:
        thr.start()
    for thr in threads:
        thr.join()

    
if __name__ == "__main__":
    main()