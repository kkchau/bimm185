/* genome table */
CREATE TABLE genomes (
genome_id int (10) UNSIGNED NOT NULL AUTO_INCREMENT,
tax_id int (10) UNSIGNED NOT NULL,
gen_short_name varchar (100) NOT NULL,
gen_long_name varchar (100) NOT NULL,
bp_size int (15) UNSIGNED,
domain enum('bacteria', 'archaea', 'eukarya'),
accession varchar (100) NOT NULL,
release_date varchar (100) NOT NULL,
PRIMARY KEY (genome_id),
KEY (tax_id)
) ENGINE=InnoDB;

/* replicon table */
CREATE TABLE replicons (
replicon_id INT (10) UNSIGNED NOT NULL,
genome_id INT (10) UNSIGNED NOT NULL,
name VARCHAR (100) NOT NULL,
CDS INT (10) UNSIGNED NOT NULL,
rep_type enum('chromosome', 'plasmid'),
rep_structure enum('linear', 'circular'),
PRIMARY KEY (replicon_id),
KEY (genome_id)
) ENGINE=InnoDB;

/* gene table */
CREATE TABLE genes (
gene_id INT (10) UNSIGNED NOT NULL,
genome_id INT (10) UNSIGNED NOT NULL,
replicon_id INT (10) UNSIGNED NOT NULL,
locus_tag VARCHAR (100) NOT NULL,
name VARCHAR (100) NOT NULL,
strand enum('+', '-'),
num_exons INT (10) UNSIGNED,
length INT (20) UNSIGNED,
product_name VARCHAR (100),
PRIMARY KEY (gene_id),
KEY (genome_id),
KEY (replicon_id)
) ENGINE=InnoDB;

/* exon table */
CREATE TABLE exons (
gene_id VARCHAR (100) UNSIGNED NOT NULL,
exon VARCHAR (100) NOT NULL,
l_position INT (10) UNSIGNED NOT NULL,
r_position INT (10) UNSIGNED NOT NULL,
length INT (10) UNSIGNED NOT NULL,
PRIMARY KEY (gene_id)
) ENGINE=InnoDB;

/* gene synonyms table */
CREATE TABLE gene_synonyms (
gene_id VARCHAR (100), 
synonym VARCHAR (100) NOT NULL,
KEY (gene_id)
) ENGINE=InnoDB;

/* external references table */
CREATE TABLE ex_ref (
gene_id VARCHAR (100), 
external_db VARCHAR (100) NOT NULL,
external_id VARCHAR (100) NOT NULL,
KEY (gene_id)
) ENGINE=InnoDB;

/* functions table */
CREATE TABLE functions (
gene_id VARCHAR (100),
function VARCHAR(100) NOT NULL,
KEY (gene_id)
) ENGINE=InnoDB;
