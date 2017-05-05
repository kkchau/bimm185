/* genome table */
CREATE TABLE genomes (
  genome_id        INT(10) UNSIGNED NOT NULL,
  name             VARCHAR(256) NOT NULL,
  tax_id           INT(10) UNSIGNED NOT NULL,
  domain           ENUM('bacteria','archaea','eukarya') NOT NULL,
  num_replicons    SMALLINT(5) UNSIGNED NOT NULL,
  num_genes        INT(10) UNSIGNED NOT NULL,
  size_bp          BIGINT(15) UNSIGNED NOT NULL,
  assembly         VARCHAR(25) NOT NULL,
  PRIMARY KEY (genome_id),
  KEY tax_id (tax_id)
) ENGINE=InnoDB;

/* replicon table */
CREATE TABLE replicons (
  replicon_id    INT(10) UNSIGNED NOT NULL,
  genome_id      INT(10) UNSIGNED NOT NULL,
  name           VARCHAR(256) NOT NULL,
  type           ENUM('chromosome','plasmid') NOT NULL,
  shape          ENUM('circular','linear') NOT NULL,
  num_genes      INT(10) UNSIGNED NOT NULL,
  size_bp        BIGINT(15) UNSIGNED NOT NULL,
  accession      VARCHAR(25) NOT NULL,
  release_date   VARCHAR(25) NOT NULL,
  PRIMARY KEY (replicon_id),
  KEY(genome_id)
) ENGINE=InnoDB;

/* gene table */
CREATE TABLE genes (
  gene_id     INT(10) UNSIGNED NOT NULL,
  genome_id   INT(10) UNSIGNED NOT NULL,
  replicon_id INT(10) UNSIGNED NOT NULL,
  locus_tag   CHAR(25) NOT NULL,
  protein_id  CHAR(25) NOT NULL,
  name        CHAR(10) NOT NULL,
  strand      ENUM('F','R') NOT NULL,
  num_exons   SMALLINT(5) UNSIGNED NOT NULL,
  length      MEDIUMINT(7) UNSIGNED NOT NULL,
  product     VARCHAR(1024) NOT NULL,
  PRIMARY KEY (gene_id),
  KEY (genome_id),
  KEY (replicon_id),
  KEY (locus_tag),
  KEY (protein_id)
) ENGINE=InnoDB;

/* external references table */
CREATE TABLE gene_xrefs (
  gene_id INT(10) UNSIGNED NOT NULL,
  xdb VARCHAR(32) NOT NULL,
  xid VARCHAR(24) NOT NULL,
  KEY (gene_id),
  KEY (xid)
) ENGINE=InnoDB;

/* exons */
CREATE TABLE exons (
    gene_id INT(10) UNSIGNED NOT NULL,
    exon INT(10) UNSIGNED NOT NULL,
    l_position INT(10) UNSIGNED NOT NULL,
    r_position INT(10) UNSIGNED NOT NULL,
    length BIGINT(15) UNSIGNED NOT NULL,
    KEY (gene_id),
    KEY (exon)
) ENGINE=InnoDB;

/* synonyms */
CREATE TABLE gene_synonyms (
    gene_id INT(10) UNSIGNED NOT NULL,
    synonym VARCHAR(25) NOT NULL,
    KEY (gene_id),
    KEY (synonym)
) ENGINE=InnoDB;

/* functions */
CREATE TABLE functions (
    gene_id INT(10) UNSIGNED NOT NULL,
    function VARCHAR(225) NOT NULL,
    KEY (gene_id)
) ENGINE=InnoDB;
