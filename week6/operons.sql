/*
 * Create table based on gene-operon associations
 */
CREATE TABLE operons (
gene_id INT(10) UNSIGNED NOT NULL,
operon VARCHAR(25) NOT NULL,
confidence VARCHAR(25) NOT NULL,
KEY (operon),
KEY (gene_id)
) ENGINE=InnoDB;
