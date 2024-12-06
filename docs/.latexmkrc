# Building glossaries. Copied from
# http://mirrors.ctan.org/support/latexmk/example_rcfiles/glossary_latexmkrc

add_cus_dep( 'acn', 'acr', 0, 'makeglossaries' );
add_cus_dep( 'glo', 'gls', 0, 'makeglossaries' );
$clean_ext .= " acr acn alg bbl glo gls glg";
sub makeglossaries {
    my ($base_name, $path) = fileparse( $_[0] );
    pushd $path;
    my $return = system "makeglossaries", $base_name;
    popd;
    return $return;
}

# Ensure that the chapters and appendixes subdirectories exist within the build directory
if (! -d 'build') {
    mkdir 'build' or die "Cannot create build directory: $!";
}
if (! -d 'build/chapters') {
    mkdir 'build/chapters' or die "Cannot create build/chapters directory: $!";
}
if (! -d 'build/appendixes') {
    mkdir 'build/appendixes' or die "Cannot create build/appendixes directory: $!";
}

# $emulate_aux = 1;
$out_dir    = '.';
$aux_dir    = 'build';

$pdf_mode   = 5;      # compile to pdf using xelatex
