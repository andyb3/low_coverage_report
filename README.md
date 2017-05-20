# Low Coverage Gene Reporter

**Takes exon-level coverage data from Sambamba and produces a report listing any genes that don't meet minimum coverage requirements of the Viapath genomics laboratory.**

**Author**

Andy Bond


**Requirements:**

* Python 2.7
* Pandas 0.18.0 or higher (untested on earlier versions)
* Tested on Linux only

**Input**

A Sambamba coverage file adhering to the format (including column headers) shown in the included example:
*  NGS148_34_139558_CB_CMCMD_S33_R1_001.sambamba_output.txt

**Output**

A tab separated report listing all genes (and their RefSeq IDs) that do not meet the minimum coverage requirements of the Viapath genomics laboratory (i.e. all coding bases at 30x or higher). See example outputs:
* example_output.tsv

**Usage**

Download or clone this repository

Execute the following command from the downloaded directory:

    >> python low_gene_coverage.py [options]

Required options:

>-i  &nbsp;&nbsp;&nbsp;input file path

>-o  &nbsp;&nbsp;output file path

For example:

    >> python low_gene_coverage.py -i ./path/to/sambamba_coverage.txt -o ./path/to/output.tsv
