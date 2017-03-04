import optparse
import os
import boto3
from botocore.utils import fix_s3_host


usage = ''' script <parameters>
A script to simply upload an object using boto3
boto3 under the hood figures out if the upload needs to be a multi part or regular upload
'''

def main():

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--access_key', dest='access_key', help="Access Key associated with a user for the migration", action="store")
    parser.add_option('-s', '--secret_key', dest='secret_key', help="Secret Key associated with a user for the migration", action="store")
    parser.add_option('-i', '--accesser', dest='accesser', help="IP address of the Accesser", action="store")
    parser.add_option('-b', '--vault', dest='source_vault_name', help="The name of the Vault the objects are being copied from", action="store")
    parser.add_option('-f', '--file', dest='file_name', help="The name of the file to be uploaded", action="store")

    (options, args) = parser.parse_args()

    if options.access_key is None:
        print 'Access Key is not specified. This is the access key associated with a user with read permissions to the Source Vault.'
        return 0
    if options.secret_key is None:
        print 'Secret Key is not specified. This is the secret key associated with a user with read permissions to the Source Vault.'
        return 0
    if options.accesser is None:
        print 'Accesser not specified. Please provide the IP of the Accesser being used for migration.'
        return 0
    if options.source_vault_name is None:
        print 'Source Vault Name not specified. Please provide the name of the Vault being migrated from.'
        return 0
    if options.file_name is None:
        print 'File name not provided. Exiting.'
        return 0
    s3 = boto3.resource('s3', endpoint_url = options.accesser, aws_access_key_id=options.access_key, aws_secret_access_key=options.secret_key)
    s3.meta.client.meta.events.unregister('before-sign.s3', fix_s3_host)

#list all buckets (checking basic connectivity)
    for bucket in s3.buckets.all():
	 print(bucket.name)

#Following is a simple put, works
#data = open('text1.txt', 'rb')
#s3.Bucket('V2').put_object(Key='text1.txt', Body=data)

#Following should be multipart upload, needs to be testes
#s3.meta.client.upload_file('hello.txt', 'V2', 'hello.txt')
    s3.meta.client.upload_file(options.file_name, options.source_vault_name, options.file_name)

#Creating Multipart

#bucket = 'V2'
#key = 'mp-test.txt'

main()
