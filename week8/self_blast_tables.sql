CREATE TABLE blast_gid1_self (
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
    scov DOUBLE PRECISION NOT NULL,
    KEY (qseqid),
    KEY (sseqid)
) ENGINE=InnoDB;

CREATE TABLE blast_gid2_self (
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
    scov DOUBLE PRECISION NOT NULL,
    KEY (qseqid),
    KEY (sseqid)
) ENGINE=InnoDB;
