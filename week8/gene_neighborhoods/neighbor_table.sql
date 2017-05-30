CREATE TABLE neighborhood (
    gene_1 INT(10) UNSIGNED NOT NULL,
    gene_2 INT(10) UNSIGNED NOT NULL,
    distance SMALLINT(5) UNSIGNED NOT NULL,
    ortholog_distance SMALLINT(5) UNSIGNED NOT NULL,
    KEY (gene_1),
    KEY (gene_2)
) ENGINE=InnoDB;
