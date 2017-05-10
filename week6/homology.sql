CREATE TABLE homology_1 (
seqid_1 VARCHAR(25) NOT NULL,
seqid_2 VARCHAR(25) NOT NULL,
h_type VARCHAR(25) NOT NULL,
method VARCHAR(25) NOT NULL,
KEY (seqid_1),
KEY (seqid_2)
) ENGINE=InnoDB;
