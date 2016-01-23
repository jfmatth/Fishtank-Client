import logging
import os
import pathlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

from archive import ArchiveManager
import constants
import logconfig


logger = logging.getLogger(__name__)


class BasePyEncryptor(object):

    def __init__(self):
        self.public = None         # public key


    def EncryptAString(AString):
        """
        Encrypts a string with the included public Key.
            AString - String to Encrypt
            PK - Pycrypto PublicKey to encrypt with.
            sEncrypted = EncryptAString("This will be encrypted", myPK)
        """
        key = RSA.importKey(self.public)
        return key.encrypt(AString, 101)


    #def EncryptAFile(filein = None, fileout=None, key=None, blocks=16384):
    #    """
    #    Encrypts a file with the key specified, using simplecrypt
    #
    #    key - string to use as an encryption key
    #    filein - full pathname of file to encrypt
    #    fileout - full pathname of encrypted file.
    #
    #    Encryptafile("filein.txt", "fileout.enc", "thisisakey")
    #    """
    #
    ##    s = simplecrypt.SimpleCrypt(key, BLOCK_SZ=(int(settings["block_sz"]) or 1024) )
    #    s = simplecrypt.SimpleCrypt(key, BLOCK_SZ=blocks)
    #
    #    fi = open(filein,"rb")
    #    fo = open(fileout,"wb")
    #
    #    # loop over the file and save to the encrypted version.
    #    for block in s.EncryptFile(fi):
    #        #time.sleep(.1)
    #        fo.write(block)
    #
    #    fi.close()
    #    fo.close()
    #


    # taken from http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/

    def encrypt_file(key=self.public, in_filename, out_filename=None, chunksize=64*1024):
        """ Encrypts a file using AES (CBC mode) with the
            given key.

            key:
                The encryption key - a string that must be
                either 16, 24 or 32 bytes long. Longer keys
                are more secure.

            in_filename:
                Name of the input file

            out_filename:
                If None, '<in_filename>.enc' will be used.

            chunksize:
                Sets the size of the chunk which the function
                uses to read and encrypt the file. Larger chunk
                sizes can be faster for some files and machines.
                chunksize must be divisible by 16.
        """
        if not out_filename:
            out_filename = in_filename + '.enc'

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

    def decrypt_file(key=self.public, in_filename, out_filename=None, chunksize=24*1024):
        """ Decrypts a file using AES (CBC mode) with the
            given key. Parameters are similar to encrypt_file,
            with one difference: out_filename, if not supplied
            will be in_filename without its last extension
            (i.e. if in_filename is 'aaa.zip.enc' then
            out_filename will be 'aaa.zip')
        """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)


class BaseArchiveEncryptor(object):

    def __init__(self, filepath=None):
        logger.debug("En: Initializing")

        self.archivepath = filepath or pathlib.Path(os.getcwd())
        self.archive = ArchiveManager(self.archivepath)

        self.stopbackup = False

    def _stop(self):
        return False

    def stop(self):
        if self._stop():
            self.stopbackup = True
            return True
        else:
            return False

    def _key(self):
        # key to seed with.
        return None

    def encrypt(self):



    def run(self):
        # process all the archives that are NOT encrypted and write out the encrypted version.

        for archive in self.archive.unencrypted_archives():
            # archive will be a record of the meta-info for the archive we need to encrypy.




        pass




    pass


