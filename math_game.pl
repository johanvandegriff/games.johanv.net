#!/usr/bin/perl

use warnings;
use strict;
use CGI qw(:standard);

my $min = param("min");
my $max = param("max") + $min;
my $num_questions = param("questions");

start();
print h2("The Math Game");
# start the form and the table
print start_form("get","math_score.pl",&CGI::URL_ENCODED);
print '<table border="0">',"\n";

my @p;

for(my $i = 1; $i <= $num_questions; $i++) {
  # create and print the problem
  $p[$i] = create_problem($min,$max);
  print '<tr><td>',$p[$i],
        '</td><td>=</td><td>',
        '<input type="text" name="a',$i,'">',
        '</td></tr>',"\n";
}

print "</table>\n";

# put the problems in a hidden file
for(my $i = 1; $i <= $num_questions; $i++) {
print '<input type="hidden" name="p',
      $i,'" value="',$p[$i],'">',"\n";
}

print '<input type="hidden" name="questions"',
      ' value="',$num_questions,'">',"\n";
print '<input type="submit" value="Submit">',"\n";
print end_form;
end();

#################################
# create_problem                #
# Inputs:                       #
#   The minimum and maximum     #
#   values of the numbers to be #
#   added or subtracted         #
# Outputs:                      #
#   A math problem              #
#################################
sub create_problem {
  my $min = shift;
  my $max = shift;
  my $o;
  my $n1 = my_rand($min,$max);
  my $n2 = my_rand($min,$max);
  if (my_rand(0,1) == 0) {
    $o = "-";
    if ($n2 > $n1) {
      my $n3 = $n1;
      $n1 = $n2;
      $n2 = $n3;
    }
  } else {
    $o = "+";
  }
  my $problem = $n1." ".$o." ".$n2;
  return $problem;
}
#################################
# my_rand                       #
# Inputs:                       #
#   The minimum and maximum     #
#   values of the random        #
#   integers                    #
# Outputs:                      #
#   A random number from the    #
#   minimum to the maximum      #
#################################
sub my_rand {
  my $min = shift;
  my $max = shift;
  my $number = $min + int(rand($max - $min + 1));
  return $number;
}
#################################
# start                         #
# Inputs:                       #
#   None                        #
# Outputs:                      #
#   The beginning of a web page #
#################################
sub start {
#  print "Content-type: text/html\n\n";
#  print `/usr/bin/php ../header.php`;
#  print header(), start_html("The Math Game");
#  print header(), start_html(-title=>"The Math Game", -style =>{-src=>["../stylesheet.css"],-media=> 'all'});
}
#################################
# end                           #
# Inputs:                       #
#   None                        #
# Outputs:                      #
#   The end of a web page       #
#################################
sub end {
  print h6("Made by Johan");
#  print `/usr/bin/php ../footer.php`;
#  print end_html();
}
