#! /usr/bin/env python
#
# BSF Python script to list a hierarchy of BSF ProcessedRunFolder, BSF Project and
# BSF Sample objects as CSV file.
#
#
# Copyright 2013 Michael K. Schuster
#
# Biomedical Sequencing Facility (BSF), part of the genomics core facility
# of the Research Center for Molecular Medicine (CeMM) of the
# Austrian Academy of Sciences and the Medical University of Vienna (MUW).
#
#
# This file is part of BSF Python.
#
# BSF Python is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BSF Python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with BSF Python.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import csv
import os
import re

from bsf import Default
from bsf.data import ProcessedRunFolder


parser = argparse.ArgumentParser(description='List projects and samples.')

# Only a --full flag, with out a value.
parser.add_argument('--full', dest='full', required=False,
                    help='Full listing with file paths',
                    nargs='?', const=True, default=False)

parser.add_argument('--input', dest='input_directory', required=True,
                    help='Input directory')

parser.add_argument('--output', dest='output_file', required=True,
                    help='Output (CSV) file')

args = parser.parse_args()

# Open the output file, create a csv.DictWriter and write a header line.

csv_file = open(name=args.output_file, mode='wb')

csv_fields = ['ProcessedRunFolder', 'Project', 'Sample']

if args.full:
    csv_fields.extend(['File1', 'Reads1', 'File2', 'Reads2'])

csv_writer = csv.DictWriter(f=csv_file, fieldnames=csv_fields)

csv_writer.writeheader()

# Assemble the input directory.

input_directory = str(args.input_directory)
input_directory = os.path.expanduser(input_directory)
input_directory = os.path.expandvars(input_directory)

if not os.path.isabs(input_directory):
    input_directory = os.path.join(Default.absolute_sequences(), input_directory)

prf = ProcessedRunFolder.from_file_path(file_path=input_directory, file_type='Automatic')

project_names = prf.projects.keys()
project_names.sort(cmp=lambda x, y: cmp(x, y))

for project_name in project_names:

    project = prf.projects[project_name]

    sample_names = project.samples.keys()
    sample_names.sort(cmp=lambda x, y: cmp(x, y))

    for sample_name in sample_names:
        sample = project.samples[sample_name]

        row_dict = dict(ProcessedRunFolder=prf.name, Project=project.name, Sample=sample.name)

        if args.full:
            for paired_reads in sample.paired_reads:
                if paired_reads.reads1:
                    row_dict['File1'] = paired_reads.reads1.file_path
                    # row_dict['Reads1'] = paired_reads.reads1.name
                    # Deduce the Reads.name from the base name without file extensions.
                    file_name = str(paired_reads.reads1.file_path)
                    file_name = os.path.basename(file_name.rstrip('/ '))
                    # Remove any file-extensions like .bam, .fastq.gz, ...
                    match = re.search(pattern=r'^([^.]*)', string=file_name)
                    if match:
                        file_name = match.group(1)
                    row_dict['Reads1'] = file_name
                else:
                    row_dict['File1'] = str()
                    row_dict['Reads1'] = str()
                if paired_reads.reads2:
                    row_dict['File2'] = paired_reads.reads2.file_path
                    # row_dict['Reads2'] = paired_reads.reads2.name
                    # Deduce the Reads.name from the base name without file extensions.
                    file_name = str(paired_reads.reads2.file_path)
                    file_name = os.path.basename(file_name.rstrip('/ '))
                    # Remove any file-extensions like .bam, .fastq.gz, ...
                    match = re.search(pattern=r'^([^.]*)', string=file_name)
                    if match:
                        file_name = match.group(1)
                    row_dict['Reads2'] = file_name
                else:
                    row_dict['File2'] = str()
                    row_dict['Reads2'] = str()
                # A line for each PairedReads replicate.
                csv_writer.writerow(rowdict=row_dict)
        else:
            # A line for each Sample, containing PairedReads replicates.
            csv_writer.writerow(rowdict=row_dict)

csv_file.close()
