/*
query id, subject id, query length, subject length, bit score, evalue, % identity, identical, alignment length, % query coverage per subject, q. start, q. end, s. start, s. end
qseqid, sseqid, qlen, slen, bitscore, evalue, pident, nident, length, qcovs, qstat, qend, sstart, send
NP_414542.1     ref|NP_414542.1|        21      21      38.1    1.13e-07        100.000 21      21      100     1       21      1       21
*/

CREATE TABLE blast_gid1 (
    qseqid VARCHAR(25) NOT NULL,
    sseqid VARCHAR(25) NOT NULL,
    qlen INT(10) UNSIGNED NOT NULL,
    slen INT(10) UNSIGNED NOT NULL,
    bitscore DOUBLE PRECISION NOT NULL, 
    evalue DOUBLE PRECISION NOT NULL,
    pident DOUBLE PRECISION NOT NULL,
    nident INT(10) NOT NULL,
    length BIGINT(15) NOT NULL,
    qcovs DOUBLE PRECISION NOT NULL,
    qstart BIGINT(15) NOT NULL,
    qend BIGINT(15) NOT NULL,
    sstart BIGINT(15) NOT NULL,
    send BIGINT(15) NOT NULL,
    PRIMARY KEY (qseqid),
    KEY (sseqid)
) ENGINE=InnoDB;

CREATE TABLE blast_gid2 (
    qseqid VARCHAR(25) NOT NULL,
    sseqid VARCHAR(25) NOT NULL,
    qlen INT(10) UNSIGNED NOT NULL,
    slen INT(10) UNSIGNED NOT NULL,
    bitscore DOUBLE PRECISION NOT NULL, 
    evalue DOUBLE PRECISION NOT NULL,
    pident DOUBLE PRECISION NOT NULL,
    nident INT(10) NOT NULL,
    length BIGINT(15) NOT NULL,
    qcovs DOUBLE PRECISION NOT NULL,
    qstart BIGINT(15) NOT NULL,
    qend BIGINT(15) NOT NULL,
    sstart BIGINT(15) NOT NULL,
    send BIGINT(15) NOT NULL,
    PRIMARY KEY (qseqid),
    KEY (sseqid)
) ENGINE=InnoDB;
