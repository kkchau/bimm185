import pymysql
import getpass


# sql table field names
fields = ['qseqid', 'sseqid', 'qlen', 'slen', 'bitscore', 'evalue', 'pident',
          'nident', 'length', 'qcovs', 'qstart', 'qend', 'sstart', 'send',
          'scov']

# database connection
print("Connecting to bm185s-mysql.ucsd.edu as kkchau; using kkchau_db")
passwd = getpass.getpass("Input password: ")
sqlconnection = pymysql.connect(host='bm185s-mysql.ucsd.edu',
                                user='kkchau',
                                password=str(passwd),
                                db='kkchau_db',
                                cursorclass=pymysql.cursors.DictCursor)

c = sqlconnection.cursor()

with open('./blast_scratch1.out', 'r') as scratch:
    for line in scratch:
        record = line.strip().split()
        record[0] = record[0].strip().split('.')[0]
        record[1] = record[1].strip().split('.')[0]
        record[1] = record[1].strip().split('|')[1]

        # skip self alignments
        if record[0] == record[1]:
            continue

        record.append(float(record[8]) / float(record[3]))      # scov
        record = ['\"{}\"'.format(str(x)) for x in record]
        
        insert_command = "INSERT INTO blast_gid1_self({}) VALUES ({});".format(','.join(fields), ','.join(record))
        print(insert_command)
        c.execute(insert_command)
        sqlconnection.commit()


with open('./blast_scratch2.out', 'r') as scratch:
    for line in scratch:
        record = line.strip().split()
        record[0] = record[0].strip().split('.')[0]
        record[1] = record[1].strip().split('.')[0]
        record[1] = record[1].strip().split('|')[1]

        # skip self alignments
        if record[0] == record[1]:
            continue

        record.append(float(record[8]) / float(record[3]))      # scov
        record = ['\"{}\"'.format(str(x)) for x in record]
        
        insert_command = "INSERT INTO blast_gid2_self({}) VALUES ({});".format(','.join(fields), ','.join(record))
        print(insert_command)
        c.execute(insert_command)
        sqlconnection.commit()

sqlconnection.close()
