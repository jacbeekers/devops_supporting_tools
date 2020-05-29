Module supporting.encryption
============================

Functions
---------

    
`decrypt(key, source, decode=True)`
:   

    
`verify()`
:   

Classes
-------

`Encryption()`
:   

    ### Class variables

    `encrypted_session_key`
    :

    `nonce`
    :

    `private_filename`
    :

    `public_filename`
    :

    `tag`
    :

    ### Methods

    `cleanup(self, key_instance)`
    :

    `decrypt(self, token, key: bytes) -> bytes`
    :

    `decrypt_with_certificates(self, key_instance, encrypted_file)`
    :

    `encrypt(self, message, key: bytes) -> bytes`
    :

    `encrypt_with_certificates(self, data, key_instance, encrypted_file)`
    :

    `get_key(self) -> bytes`
    :