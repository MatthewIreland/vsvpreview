#!/usr/bin/perl

# Matthew Ireland, 15 July MMXV
# Removes empty lists in a tex file.

use strict;
use warnings;
use File::Slurp;

my $filename = $ARGV[0] or die "No input file $!";

my $tex = read_file($filename) or die "Could not open '$filename' for reading $!";

$tex =~ s/\\begin\{(itemize|enumerate|description)\}\s*\\end\{(itemize|enumerate|description)\}//g;

open (my $OUTFH, '>', $filename) or die "Could not open 'filename' for writing $!";

print $OUTFH $tex;

close $OUTFH;
