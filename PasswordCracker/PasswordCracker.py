import hashlib

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
            tail()
        if choice == '4':
            commonPW()
        if choice == '5':
            cont = False

def randCapWord():
    print("Capitalize each letter in a word")

def strBF():
    print("String brute force")

def trail():
    print("Dict with trail")

def commonPW():
    print("Common Passwords")
    with open("cracked.txt", "w") as out:
        with open("passwords.txt", "r") as pwlist:
            hashes = open("hashes.txt", "r")
            hashList = []
            for h in hashes:
                hashList.append(h)
            for password in pwlist:
                encoded = hashlib.sha256(password.strip().encode()).hexdigest()
                for hash in hashList:
                    if encoded.strip() == hash.strip():
                        print(encoded+":"+password)
                        out.write(encoded + ":" + password)
    out.close()


if __name__ == "__main__":
    main()