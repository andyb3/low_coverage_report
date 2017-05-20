# Title: 		Low Coverage Gene Reporter
# Version: 		1.0 (May 2017)
# Author: 		Andy Bond
# Purpose: 		Takes Sambamaba coverage bed file and produces report listing
# 		   		genes that do not meet coverage requirements (100% @ >=30x)
# Requires:		Python 2.7
# 			    Pandas v0.18.0 or higher
# Usage: 		python low_coverage_report.py -i <input_file_path> -o <output_file_path>
# 		 		Input file: Sambamba coverage report conforming to format specified at:
#						    github.com/andyb3/low_coverage_report
#		 		Output file: Tab separated report listing genes + RefSeq IDs that 
#						     did not meet coverage requirements 

import sys
import os.path
import time
import pandas as pd


class LowGeneCov(object):
	"""
	Takes Sambamba coverage report as input and produces a report 
	listing genes with <100% coverage at >=30x
	"""
	def __init__(self, sambamba_report, output_path):
		self.sambamba_report = sambamba_report
		self.output_path = output_path

	def find_genes(self):
		# Read sambamba output into pandas dataframe. 
		# Error and exit if file isn't valid or contains no data
		try: 
			df = pd.read_csv(self.sambamba_report, sep='\t', 
							 usecols=["GeneSymbol;Accession", "percentage30"],
							 dtype={"GeneSymbol;Accession": str, "percentage30": float})
			# Check file actually contains some data
			assert (not df.empty), ("Input Sambamba coverage report contains no data")
		except Exception,e:
			print "\nERROR: " + str(e)
			print "\nUnable to process input file: " + self.sambamba_report
			print "See github.com/andyb3/low_coverage_report for allowed format.\n"
			return
		# Get any rows that have <100% coverage at 30x.
		df = df.loc[df['percentage30'] < 100.00]
		# If no rows found, all genes are covered at >=30x, so report can be generated.
		if df.empty:
			self.make_report(df)
		else:
			# Split GeneSymbol and Accession to separate fields.
			df['#Gene'], df['#RefSeq IDs'] = df['GeneSymbol;Accession'].str.split(';', 1).str
			# Reduce to one row per gene and sort alphabetically by gene symbol.
			df.drop_duplicates(subset='#Gene', inplace=True)
			df.sort_values('#Gene', inplace=True)
			# Pass dataframe to make report method.
			self.make_report(df)

	def make_report(self, df):
		# Create report header with input file and timestamp
		header = ("Report Generated: " + time.strftime("%d/%m/%Y %H:%M:%S") 
				  + "\nInput File: " + os.path.basename(self.sambamba_report))
		if df.empty:
			# If dataframe is empty, indicate that all genes had sufficient coverage...
			header += "\n\n**All genes had 100% coverage at 30x or higher**"
		else:
			# ...otherwise indicate that listed genes did not have sufficient coverage.
			header += "\n\n**Genes listed below did NOT meet the required minimum coverage of 30x**\n\n"
		try:
			# Write header line to output file.
			with open(self.output_path, 'w') as output:
				output.write(header)
			# If any genes had insufficient coverage, append Gene list and RefSeq IDs to output file.
			if not df.empty:
				df.to_csv(self.output_path, columns=['#Gene', '#RefSeq IDs'],
					      sep="\t", index=False, mode='a')
		except Exception,e:
			print "\nERROR: " + str(e)
			print "\nUnable to write output to location: " + self.output_path + "\n"



def main():
	# Help message to be displayed if supplied arguments are incorrect.
	help_message = ("\nlow_coverage_report.py requires the following arguments:"
					"\n-i <input_file>\n-o <output_file>\n")
	# Create dictionary of supplied arguments.
	arg_dict = dict(zip(sys.argv[1::2], sys.argv[2::2]))
	# Check correct arguments have been supplied
	if len(sys.argv) == 5 and sorted(arg_dict.keys()) == ['-i', '-o']:
		# Create low coverage gene report.
		lgc = LowGeneCov(arg_dict['-i'], arg_dict['-o'])
		lgc.find_genes()
	else:
		print help_message


if __name__ == '__main__':
	main()

