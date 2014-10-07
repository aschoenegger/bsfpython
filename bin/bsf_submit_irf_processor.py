#! /usr/bin/env python
#
# BSF Python script to process an Illumina Run Folder (IRF) after sequencing and
# drive the IlluminaToBamTools IlluminaToBam and BamIndexDecoder analyses.
#
#
# Copyright 2014 Michael K. Schuster
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

from argparse import ArgumentParser

from Bio.BSF import Default
from Bio.BSF.Analyses.IlluminaToBamTools import BamIndexDecoder, IlluminaToBam


argument_parser = ArgumentParser(
    description='IlluminaToBamTools Illumina2bam and BamIndexDecoder analysis driver script.')

argument_parser.add_argument(
    '--debug',
    help='Debug level',
    required=False,
    type=int)

argument_parser.add_argument(
    '--stage',
    help='Limit job submission to a particular Analysis stage',
    required=False,
    type=str)

argument_parser.add_argument(
    '--irf',
    help='Illumina Run Folder name or file path',
    required=False,
    type=str)

argument_parser.add_argument(
    '--library-file',
    dest='library_file',
    help='Library annotation sheet',
    required=False,
    type=str)

argument_parser.add_argument(
    '--configuration',
    default=Default.global_file_path,
    help='Configuration (*.ini) file',
    required=False,
    type=str)

arguments = argument_parser.parse_args()

# Create a BSF IlluminaToBam analysis, run and submit it.

itb = IlluminaToBam.from_config_file(config_file=arguments.configuration)

# Set arguments that override the configuration file.

if arguments.debug:
    itb.debug = arguments.debug

if arguments.irf:
    itb.illumina_run_folder = arguments.irf

# Do the work.

itb.run()
itb.submit(drms_name=arguments.stage)

# Create a BSF BamIndexDecoder analysis, run and submit it.

bid = BamIndexDecoder.from_config_file(config_file=arguments.configuration)

# Transfer the project name from the IlluminaToBam to the BamIndexDecoder analysis.

bid.project_name = itb.project_name

# Set arguments that override the configuration file.

if arguments.debug:
    bid.debug = arguments.debug

if arguments.library_file:
    bid.library_file = arguments.library_file

# Do the work.

bid.run()
bid.submit(drms_name=arguments.stage)

print 'IlluminaToBamTools IlluminaToBam Analysis'
print 'Project name:         ', itb.project_name
print 'Project directory:    ', itb.project_directory
print 'Illumina Run Folder:  ', itb.illumina_run_folder
print 'Experiment directory: ', itb.experiment_directory
print ''
print 'IlluminaToBamTools BamIndexDecoder Analysis'
print 'Project name:         ', bid.project_name
print 'Project directory:    ', bid.project_directory
print 'Sequences directory:  ', bid.sequences_directory
print 'Experiment directory: ', bid.experiment_directory
