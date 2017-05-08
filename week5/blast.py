import pymysql
import getpass
import subprocess
import os


# define mysql functions so I don't have to type everything out all of the time
def sqlInsert(sql_connection, table, col_list, values):
    with sql_connection.cursor() as cursor:
        sub_set = ','.join(['%s' for _ in range(len(values))])
        command = "INSERT INTO " + table + "(" + ','.join(col_list) + ") VALUES (" + sub_set + ");"
        cursor.execute(command, values)

    sql_connection.commit()

    return 0        # return code


# change to blastdb folder for all database files
os.chdir('/home/linux/ieng6/bm185s/kkchau/bimm185/week5/blastdb')

# filenames
genomes_dir = '/home/linux/ieng6/bm185s/kkchau/bimm185/week4/genomes/'
ecoli_dir = genomes_dir + 'e_coli/GCF_000005845.2_ASM584v2_protein.faa.gz'
atuma_dir = genomes_dir + 'a_tumafaciens/GCF_000576515.1_ASM57651v1_protein.faa.gz'

# for blasting proteome of a_tumafaciens against e_coli database
gid_1 = 1
gid_2 = 2

# DATABASE CONNECTION
print("Connecting to bm185s-mysql.ucsd.edu as kkchau; using kkchau_db")
passwd = getpass.getpass("Input password: ")
sqlconnection = pymysql.connect(host='bm185s-mysql.ucsd.edu',
                                user='kkchau',
                                password=str(passwd),
                                db='kkchau_db',
                                cursorclass=pymysql.cursors.DictCursor)

# sql table field names
fields = ['qseqid', 'sseqid', 'qlen', 'slen', 'bitscore', 'evalue', 'pident',
          'nident', 'length', 'qcovs', 'qstart', 'qend', 'sstart', 'send',
          'scov']

# blast a_tumafaciens against e_coli
print("blast 1")
zcat = subprocess.Popen(['zcat', atuma_dir], stdout=subprocess.PIPE)
subprocess.Popen(['blastp', '-query', '-', '-out', 'blast_scratch.out',
                  '-db', 'ecoli_blastdb', '-evalue', '0.01', '-outfmt',
                  "6 qseqid sseqid qlen slen bitscore evalue pident nident length qcovs qstart qend sstart send"],
                  stdin=zcat.stdout)
zcat.wait()

print("sql 1")
# process blast output and export to database (blast_gid1)
with open('blast_scratch.out', 'r') as scratch1:
    for line in scratch1:
        record = line.strip().split()
        record.append(float(record[8]) / float(record[3]))              # scov
        sqlInsert(sqlconnection, 'blast_gid1', fields, record)

print("blast 2")
# blast e_coli against a_tumafaciens
zcat = subprocess.Popen(['zcat', ecoli_dir], stdout=subprocess.PIPE)
subprocess.Popen(['blastp', '-query', '-', '-out', 'blast_scratch.out',
                  '-db', 'atuma_blastdb', '-evalue', '0.01', '-outfmt',
                  "6 qseqid sseqid qlen slen bitscore evalue pident nident length qcovs qstart qend sstart send"],
                  stdin=zcat.stdout)
zcat.wait()

print("sql 2")
# process blast output and export to database (blast_gid2)
with open('blast_scratch.out', 'r') as scratch1:
    for line in scratch1:
        record = line.strip().split()
        record.append(float(record[8]) / float(record[3]))              # scov
        sqlInsert(sqlconnection, 'blast_gid2', fields, record)

sqlconnection.close()
