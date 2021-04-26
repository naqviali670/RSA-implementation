#!/usr/bin/env python3
import random

"""
RSA implementation program

author: Syed Kausar Ali Naqvi    
email: naqviali670@gmail.com
"""

#calculating gcd using euclidean algo
def extended_euclidean(a , b):
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1
    i = 2
    q = a // b
    temp = q 
    temp1 = temp
    while b!=0:
        a , b = b , a%b
        if(b==0):break
        q = a // b
        temp1 = temp
        temp = q
        x = x1*temp1 + x0
        y = y1*temp1 + y0
        x0 = x1
        x1 = x
        y0 = y1
        y1 = y
        i = i +1
    x = ((-1)**(i - 1)) * x
    y = ((-1)**(i)) * y   
    return a , x , y 



#calculating modulu using fastModularExponentitaion algo
def fastModularExponentitaion(base , exponent , m):
    Y = 1
    first = True
    while exponent > 0:
        if exponent % 2 == 0:
            if first == True:
                base = base % m
                first = False
            else:
                base = (base * base) % m    
            exponent = exponent // 2
        else:
            if first == True:
                base = base % m
                first = False
            else:
                base = (base * base) % m   
            Y = (base * Y) % m     
            exponent = exponent // 2
    return Y         
            
         
# check whether the number is prime or not using Miller algo
def millerrabin(p , a = 5):
    n = p - 1
    n1 = p
    s = 0
    first = True
    while n % 2 == 0:
        n = n // 2
        s = s + 1
    
    if fastModularExponentitaion(a , n , p) == 1:
        print("prime")
        return True
    else:
        for i in range(0 , s):
            if first == True:
                m = fastModularExponentitaion(a , n , p) 
                first = False   
            else:
                m = (m * m) % p
            if m == (p - 1):
                print("prime")
                return True                          
    return False            
  
#to generate big prime numbers  
def generate_random_bignumber(b):
    from random import getrandbits
    while True:
        p = getrandbits(b)
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239,
                  241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
        if any(p % x == 0 for x in primes):
            continue
        if millerrabin(p):
            return p    
    
        
#to generate public and private key        
def generate_Keys(b):
    p = generate_random_bignumber(b)
    q = generate_random_bignumber(b)
    
    n = p * q
    phin = (p - 1)*(q - 1)
    for x in range(2 , phin):
        gcd , d , y = extended_euclidean(x , phin)
        d = d % phin
        if gcd == 1:
            e = x
            break;
    return n , e , d , p , q
           
           
def encrypt(key_pair , message):
    n , e = key_pair
    cipher = [str(fastModularExponentitaion(ord(c) , e , n)) for c in message]
    return " ".join(cipher)  
      
      
def chinese_remainder(dp , dq , c , p , q):
    mp = fastModularExponentitaion(c , dp , p)
    mq = fastModularExponentitaion(c , dq , q)
    _ , yp , yq = extended_euclidean(p , q)  
    return ((mp * yq * q) + (mq * yp * p)) % (p * q)  
                                
def decrypt(key_pair , cipher , p , q):
    d , n = key_pair
    dp = (d % (p - 1))
    dq = (d % (q - 1))
    m = [chr(chinese_remainder(dp , dq , int(c) , p , q))
              for c in cipher.split(' ')]
    return ''.join(m)                                
                                   
def main():
    while True:
        print("1:Generate Keys\n2:Encrypt\n3:Decrypt\n")
        option = int(input("Please select one: "))
        if option not in (1 , 2 , 3):
            print("Please select the valid option")  
        else:
            break      
    
    if option == 1:
    #We can change 16 to the bigger one as well.
        n , e , d , p , q = generate_Keys(2048)
        print("*******Important Note*******")
       
        print("Public Key is being stored in public.txt, private key is being stored in the private.txt and big prime numbers are being stored in big_prime_numbers.txt file in your current directory......")
        with open("public.txt", 'w') as file:
            file.write("n = "+str(n)+"\ne  = "+str(e))
        with open("private.txt", 'w') as file:
            file.write("d = "+str(d))
        with open("big_prime_numbers.txt", 'w') as file:
            file.write("p = "+str(p)+"\nq  = "+str(q))
    elif option == 2:
        print("***Step 1***")
        print("Enter the public key")
        n = int(input("Enter n: "))   
        e = int(input("Enter e: ")) 
        print("***Step 2***")
        message = input("Enter the message you want to encrypt: ")  
        print("Encryption Started.....Please be patient")
        cipher = encrypt((n , e) , message)
        print("Encrypted message is being stored in encrypted_message.txt file in your current directory.....")
        with open("encrypted_message.txt", 'w') as file:
            file.write("encrypted_message : "+cipher)
       
    else:
        print("***Step 1***")
        d = int(input("Enter the private key(d): "))
        n = int(input("Enter n: "))  
        print("***Step 2***")
        cipher = input("Enter the message you want to decrypt: ") 
        print("***Step 3***")
        p = int(input("Enter the first big prime number (p): "))
        q = int(input("Enter the first big prime number (q): "))
        print("Decryption Starts.......Please be patient")
        message = decrypt((d , n) , cipher , p , q) 
        print("***Your message after decryption is***")
        print(message)
    
    
    
   

############################################################################

if __name__ == "__main__":
    main()

