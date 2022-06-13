import hashlib

def read_salts(filename):
    with open(filename) as f:
        for salt in f:
            yield salt.strip()
            
def read_passwords(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()
            


###
# Create a password cracker to figure out passwords that were hashed using SHA-1
#
# Important: SHA1 is not a secure hash algorithm. Why, we will proove it to you here.  
# By nature, we don't want to memorize complicated passwords, so hackers came up with 
# a list of frequently used passwords called the Rainbow Table.
#
# SHA1 hashing is a one-way hashing algorithm.  Therefore, we hash.sha1 on the given 
# rainbow table in top-10000-passwords and match each to the given hashed string 
# looking for a match.  i.e. matching two hashed strings to arrive at the original password.
#
# e.g. 
# salts=False, b305921a3723cd5d70a375cd21a61e60aabb84ec should return "sammy123"
# salts=True, 53d8b3dc9d39f0184144674e310185e41a87ffd5 should return "superman"
###
def crack_sha1_hash(hash, use_salts=False):
    # Read the Rainbow Table
    for line in read_passwords('top-10000-passwords.txt'):
        password = line.strip()                   
        if use_salts:
            for salt in read_salts("known-salts.txt"):
                # Appending the salt to the password
                hp = hashlib.sha1((password + salt).encode('utf-8')).hexdigest()        
                if len(hp) == len(hash) and hp == hash:
                    print(hp + " <==> " + hash, end="\n")
                    return line      
                # Prepending the salt to the password
                hp = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()        
                if len(hp) == len(hash) and hp == hash:
                    print(hp + " <==> " + hash, end="\n")
                    return line                        
        else:
            hp = hashlib.sha1(password.encode('utf-8')).hexdigest()
            if len(hp) == len(hash) and hp == hash:
                print(hp + " <==> " + hash, end="\n")
                return line
        
    return "PASSWORD NOT IN DATABASE"


