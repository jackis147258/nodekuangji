from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)

t_gasbnbToken='gAAAAABlFY3BcTxu5jzj_rwzCZqDTaXPbA2dzwseJh4-uhEsfFM_oNJwh42Tn8l1JKELkzPmL_4XNStzCkyY7zyyPW5urgSY6VQxn70q5t9Ce9cl5TriJT41Mu0gD6PQDOflgRd-HyrFtU_WYegq0hOSU4K_lnc14tSc1ZpinPiH613c_2nc_ZI='
cipher_suite = Fernet('FRrgJ5KhZNgtdctTbQWV2-Xam9zZP-pdsUsLDDPg0pY=') 
gasbnbToken = cipher_suite.decrypt(t_gasbnbToken) 

print (gasbnbToken)


