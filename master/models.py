import hashlib
from django.db import models
from django.db import models
import random
import string
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from .utils import encrypt,decrypt
from django.conf import settings
from django.contrib.auth.models import User
from user.models import UserProfile

# Create your models here.
class Secrets(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE, related_name="user_profile")
    masterkey_hash = models.TextField(null=False)
    device_secret = models.TextField(null=False)

    def generate_random_password(self,length=50):
        # Define character sets
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        special_characters = string.punctuation

        # Generate password with at least one uppercase letter, one digit, and one special character
        password = random.choice(uppercase_letters)  # Ensure at least one uppercase letter
        password += random.choice(digits)  # Ensure at least one digit
        password += random.choice(special_characters)  # Ensure at least one special character

        # Fill the remaining characters with a mix of uppercase letters, digits, and special characters
        remaining_length = length - 3  # Subtract 3 for the already chosen characters
        password += ''.join(random.choices(uppercase_letters + digits + special_characters, k=remaining_length))

        # Shuffle the password to randomize the order of characters
        password_list = list(password)
        random.shuffle(password_list)
        password = ''.join(password_list)

        return password

    def generate_device_secret(self, length=10):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

    def set_masterkey(self,password, user_id):
        try:
            user = User.objects.get(id=user_id)
            print(user)
        except User.DoesNotExist:
           return False

        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            print("UserProfile does not exist for this user")

        user_profile.onboarding = False
        user_profile.save()
        self.user = user
        self.masterkey_hash = hashlib.sha256(password.encode()).hexdigest()
        self.device_secret = self.generate_device_secret()
        self.save()
        return True

    def validate_master_password(self,password, user_id):
        user = User.objects.get(id=user_id)
        hashed_mp = hashlib.sha256(password.encode()).hexdigest()
        result = Secrets.objects.get(user=user)
        if hashed_mp == result.masterkey_hash:
            return result
        else :
            return False

class Entries(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_related', null=True)
    site_name = models.TextField(null=False)
    site_url = models.TextField(null=True)
    site_image = models.TextField(null=True)
    email = models.TextField(null=True)
    username = models.TextField(null=True)
    password = models.TextField(null=False)

    def compute_master_key(self,mp,ds):
        password = mp.encode()
        salt = ds.encode()
        key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
        return key

    def add_entry(self, mp, ds, sitename, siteurl, siteimage, email, username, password, user_id):
        try:
            user = User.objects.get(id=user_id)
            print(user)
        except User.DoesNotExist:
            # Handle the case where user does not exist
            print('---------------------', user_id)
            return False

        mk = self.compute_master_key(mp,ds)
        encrypted_mk = encrypt(key=mk, source=password,keyType="bytes")

        self.site_name = sitename
        self.site_url = siteurl
        self.site_image = siteimage
        self.email = email
        self.username = username
        self.password = encrypted_mk
        self.user = user
        self.save()

    def retrieve_entries(self,search, user_id):
        user = User.objects.get(id=user_id)
        if search == "" or search == None:
            all_data = Entries.objects.filter(user=user)
            return all_data
        else:
            data = Entries.objects.get(user=user,site_name=search)            
            return [data]
    
    def decrypted_entry(self,mp,ds,search,user_id):
        user = User.objects.get(id=user_id)
        data = Entries.objects.get(user=user,site_name=search)            
        mk = self.compute_master_key(mp, ds)
        decrypted_mk = decrypt(key=mk, source=data.password,keyType="bytes")
        data.password = decrypted_mk.decode()
        return [data]
    
    def delete_entry(self, search):
        data = Entries.objects.get(site_name=search)             
        print('data: ', data)
        copied_data = data
        data.delete()
        return copied_data

        



#    def create_key(self, path):
        #self.key = Fernet.generate_key()
        #with open(path, 'wb') as key_file:  # Open the file at the given path
            #key_file.write(self.key)        # Write the generated key to the file
    
    #def set_master_password(self, master_password):
        ## Store the hashed master password securely
        #if not PasswordManager.objects.exists():
            ## Store the hashed master password securely
            #self.master_password_hash = hashlib.sha256(master_password.encode()).hexdigest()
            #self.save()  # Save the instance to the database
            #return True
        #else:
            #return False

    #def verify_master_password(self, entered_password):
        ## Verify the entered master password against the stored hash
        #entered_password_hash = hashlib.sha256(entered_password.encode()).hexdigest()
        #curent_password = PasswordManager.objects.all()
        ## print(entered_password_hash, self.master_password_hash)
        #return curent_password[0].master_password_hash == entered_password_hash

    #def derive_key_from_master_password(self):
        ## Derive the encryption key from the master password
        #return hashlib.sha256(self.master_password_hash.encode()).digest()

    #def add_new_password(self, password, site):
        #curent_password = PasswordManager.objects.all()
        #key = hashlib.sha256(curent_password[0].master_password_hash.encode()).digest() #curent_password[0].master_password_hash
        #print(key, "key")
##    def create_password_file(self,path,initial_values=None):
        #self.password_file = path

        #if initial_values is not None:
            #for key, value in initial_values.items():
                #self.add_password(key,value)
                
    #def load_password_file(self,path):
        #self.password_file = path
        #key = self.derive_key_from_master_password()

        #with open(path, "r") as f:
            #for line in f:
                #site, encrypted = line.split(" : ")
                #self.password_dict[site] : Fernet(key).decrypt(encrypted.encode()).decode()

    #def add_password(self,site,password):
        #self.password_dict[site] = password
        #key = self.derive_key_from_master_password()
        
        #if self.password_file is not None:
            #with open(self.password_file, "a+") as f:
                #encypted = Fernet(key).encrypt(password.encode())
                #f.write(site + " : " + encypted.decode() + "\n")
                
    #def get_password(self,site):
        #return self.password_dict[site]