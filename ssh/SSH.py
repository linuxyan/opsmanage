#!/usr/bin/python
# coding=utf-8
#__author__ = 'CY'

import os,paramiko
from config import Config, basedir

paramiko_log = os.path.join(basedir,'logs/paramiko.log')

def ssh_cmd(ip,port,username,privatekeyfile,cmd):

    paramiko.util.log_to_file(paramiko_log)
    ssh_obj = paramiko.SSHClient()
    ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshkey = paramiko.RSAKey.from_private_key_file(filename=privatekeyfile)
    try:
        ssh_obj.connect(hostname=ip,port=port,username=username ,pkey=sshkey,timeout=15)
        stdin,stdout,sterr=ssh_obj.exec_command(cmd)
        stdout = stdout.read()
        sterr = sterr.read()
        if sterr:
            return 'ERROR',sterr
        else:
            return 'SUCCESS',stdout
        ssh_obj.close()
    except Exception,ex:
        ssh_obj.close()
        print Exception,":",ex
        print '%s\tError\n'%(ip)
        return 'Error'



# def upload_file(ip,port,username,privatekeyfile,local_file,remote_file):
#     try:
#         paramiko.util.log_to_file('logs/paramiko_putfile.log')
#         ssh_ftp = paramiko.SSHClient()
#         sshkey = paramiko.RSAKey.from_private_key_file(filename=privatekeyfile)
#         ssh_ftp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh_ftp.connect(hostname=ip,port=port,username=username ,pkey=sshkey,timeout=15)
#         sftp =paramiko.SFTPClient.from_transport(ssh_ftp)
#         sftp.put(local_file, remote_file)
#         ssh_ftp.close()
#         return remote_file
#     except Exception,ex:
#         ssh_ftp.close()
#         print Exception,":",ex
#         print '%s\tError\n'%(ip)


if __name__ == '__main__':
    pass
    #ssh_cmd(ip='10.0.5.93',port=22,username='mysqluser',privatekeyfile="E:\\tmp\\key\\mysqluser",cmd='uname -a')