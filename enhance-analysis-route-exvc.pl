#!/usr/bin/perl
use lib "/home/hfzhang/perl5/lib/perl5";

#Load module
use Expect;
use FindBin '$Bin';
use Getopt::Std;
use Spreadsheet::WriteExcel;

#Others parameters
$fabric_drop_threshold = 1000000;
$cli_width = "set cli screen-width 0";
$timeout = 10;
$logstdout_switch = 1;
$prompt = '(assword:)|(id_[dr]sa\':)|(you sure you want to continue)|(sername:)|(ogin:)';
chomp($year = `date '+%Y'`);
chomp($today = `date '+%b %e'`);
chomp($yesterday = `date --date 'yesterday' '+%b %e'`);
chomp($time = `date '+%Y%m%d-%H'`);
chomp($time_1 = `date -d '-1 hour' '+%Y%m%d-%H'`);
chomp($hour = `date '+%H'`);
$firstlogcheck = "$today (0[0-7]:[0-9][0-9])";
$secondlogcheck = "$today (0[8-9]:[0-9][0-9]|1[0-5]:[0-9][0-9])";
$thirdlogcheck = "$yesterday (1[6-9]:[0-9][0-9]|2[0-3]:[0-9][0-9])";

#Proceed options
getopts("hr:dpo:STs:t:w:y", \%opt);
unless ($opt{h}||$opt{r}||$opt{d}||$opt{p}||$opt{T}||$opt{S}||$opt{s}||$opt{t}||$opt{y}||$opt{w}) {
	output_usage();
	exit(1);
}
if ($opt{h}) {
	output_usage();
	exit(1);
}
if ($opt{d} && $opt{p}) {
	print "Option 'd' and option 'p' are mutually exclusive.\n";
	exit(1);
}
unless ($opt{d} || $opt{p}) {
	print "You must choose option 'd' or option 'p'.\n";
	exit(1);
}
if ($opt{T} && $opt{S}) {
	print "Option 'T' and option 'S' are mutually exclusive.\n";
	exit(1);
}
if (!$opt{w}) {
	print "Must specific work path, e.g /asphc/CUSTOMER-NAME\n";
	exit(1);
}
if ($opt{s} && $opt{t}) {
	if ($opt{d}) {
		print "Option 's', 't' and 'd' are mutually exclusive.\n";
		exit(1);
	} elsif ($opt{T}) {
		print "Option 's', 't' and 'T' are mutually exclusive.\n";
		exit(1);
	} elsif ($opt{S}) {
		print "Option 's', 't' and 'S' are mutually exclusive.\n";
		exit(1);
	} elsif (!($opt{s} eq "proxy" || $opt{s} eq "router")) {
		print "Wrong value! The usable option for option 's' are 'proxy' or 'router'.\n";
		exit(1);
	} elsif (!($opt{t} eq "proxy" || $opt{t} eq "router")) {
		print "Wrong value! The usable option for option 't' are 'proxy' or 'router'.\n";
		exit(1);
	} elsif ($opt{t} eq $opt{s}) {
		print "Can not use same value for option 't' and 's'.\n";
		exit(1);
	}
} elsif ($opt{s} || $opt{t}) {
	print "Option 's' and 't' are mutually required.\n";
	exit(1);
} else {
	unless ($opt{T} || $opt{S}) {
		print "You must choose option 'T' or 'S'.\n";
		exit(1);
	}
}


$router_list = $opt{r};
open(LIST,$router_list) or die "Cannot open file $router_list: $!";
@router = <LIST>;
close LIST;

#Read config
$work_path = $opt{w};

open(CONFIG, "$work_path/CONFIG.TXT") or die "Cannot open config file CONFIG.TXT: $!";
while ( <CONFIG> ) {
	chomp;
	if ( /^username="(.*)"/ ) {
		$username = $1;
	}
	if ( /^passwd="(.*)"/ ) {
		$passwd = $1;
	}
	if ( /^rtr_prompt="(.*)"/ ) {
		$rtr_prompt = "$1";
	}
	if ( /^proxy_ip="(.*)"/ ) {
		$proxy_ip = $1;
	}
	if ( /^proxy_username="(.*)"/ ) {
		$proxy_username = $1;
	}
	if ( /^proxy_passwd="(.*)"/ ) {
		$proxy_passwd = $1;
	}
	if ( /^proxy_prompt="(.*)"/ ) {
		$proxy_prompt = "$1";
	}
	if ( /^mail_sub="(.*)"/ ) {
		$mail_sub = $1;
	}
	if ( /^mail_receiver="(.*)"/ ) {
		$mail_receiver = $1;
	}
	if ( /^link_flap_threshold="(.*)"/ ) {
                $flap_threshold = $1;
        }
}

#Main Program
#Login router and get data
@command = generate_cmd();
foreach $router (@router) {
        chomp($router);
        @ip_name = split(" ",$router);

        if ($opt{d}) {
                $session = login($ip_name[0]);
        } else {
                $session = login_proxy($ip_name[0]);
        }
        unless (-d "$work_path/syslog/") {
                mkdir("$work_path/syslog/");
        }
        if (!defined($session)) {
                print "Can not login router $ip_name[1]\n";
        } else {

		if ( ($hour == 0) || ($hour == 8) || ($hour == 16) ) {
			$session->log_file("$work_path/syslog/$ip_name[1]","w");
	    
			if ($ip_name[2] =~ /EXVC/) {
				getlog_vc($session,$ip_name[1],@command);
			} else {
				getlog($session,$ip_name[1],@command);
			}
		}

		$session->log_file("$work_path/syslog/$ip_name[1]-alarm","w");
		getalarm($session,$ip_name[1]);
		
		#add code to capture interface stats
		unless (-d "$work_path/capture/") {
			mkdir("$work_path/capture/");
		}
		
		unless (-d "$work_path/capture/$time/") {
			mkdir("$work_path/capture/$time/");
		}
		$session->log_file("$work_path/capture/$time/$ip_name[1]-stats","w");
		getstats($session,$ip_name[1]);
					
		#cleanup session
		$session->send("exit\n");
		$session->expect( $timeout , "-re" , $rtr_prompt );
	
		if ($opt{p}) {
			$session->expect( $timeout , "-re" , $proxy_prompt );
			$session->send("exit\n");
		}
		$session->log_file( undef );
		$session->hard_close();
        }
}

#check fabric drop increasing. If fabric drop increase cross threshold, list the router
foreach $router (@router) {
	chomp($router);
	@ip_name = split(" ",$router);
 
	$fabric_drop_current = `cat $work_path/capture/$time/$ip_name[1]-stats | grep "Fabric drops" | awk '{ print \$NF }'`;
	$fabric_drop_before = `cat $work_path/capture/$time_1/$ip_name[1]-stats | grep "Fabric drops" | awk '{ print \$NF }'`;
	chomp($fabric_drop_current);
	chomp($fabric_drop_before);
 
	$delta = $fabric_drop_current - $fabric_drop_before;

	if ( $delta > $fabric_drop_threshold ) {
		if ($opt{d}) {
                	$session = login($ip_name[0]);
        	} else {
                	$session = login_proxy($ip_name[0]);
        	}		
		my $current_value = get_fabric_drop($session,$ip_name[1]);
                sleep(30);
                my $next_value = get_fabric_drop($session,$ip_name[1]);
                my $delta_minute = $next_value - $current_value;
                print "Router: $ip_name[1], Previous value, $current_value; Next value, $next_value.\n";
                if ( $delta_minute > 1000 ) {
			`echo "$ip_name[1], Fabric drop counter before: $fabric_drop_before, current: $fabric_drop_current, delta: $delta\n\n" > $work_path/TODAY_ALARMS`;
		}
	}
}

#check alarms on all routers and save in local file
chdir("$work_path/syslog/");
`echo "** Alarm report **" >> $work_path/TODAY_ALARMS`;
#`egrep -i "major|minor" *alarm | sed 's/-alarm:/\t/g' | sort -rk 2 >> $work_path/TODAY_ALARMS`;
`egrep -i "major|minor" *alarm | sed 's/-alarm:/\t/g' | sort -rk 2 >> $work_path/TODAY_ALARMS`;

`echo "\n\n** LACP Status report **" >> $work_path/TODAY_ALARMS`;
`egrep -i defaulted *alarm | sed 's/-alarm:/\t/g' >> $work_path/TODAY_ALARMS`;


#Only check route for CMNET backbone customer
if ($work_path =~ /cmnet/) {
	check_route();
}

# send wechat message to mobile. if any alarm reported in current alarm check
`python /asphc/wechat-tjcloud.py $work_path/TODAY_ALARMS "hanjhui|dongkui|jeremyzhu|Haofeng"`;

#Process data and generate excel
#Only when it's the right time
if ( ($hour == 0) || ($hour == 8) || ($hour == 16) ) {
	chdir("$work_path/syslog/");
	
	open(FULL,">$work_path/full_syslog.txt") or die "Cannot open file full_syslog.txt: $!";
	foreach $router (@router) {
		chomp($router);
		@ip_name = split(" ",$router);
		process_log($ip_name[1]);
	}
	close FULL;
	
	chdir("$work_path");
	gen_excel_log_text();
}

if ( -e "$work_path/$time-log.xls" ) {
	`mutt -s "$mail_sub" "$mail_receiver" -a "$work_path/$time-log.xls" < $work_path/TODAY_ALARMS`
} else {
	
	if ( -s "$work_path/TODAY_ALARMS" ) {
		`mutt -s "$mail_sub" "$mail_receiver" < $work_path/TODAY_ALARMS`
	}
}

#main program over. Do some clean up.
`rm -rf $work_path/TODAY_ALARMS`;
`rm -rf $work_path/syslog/*`;
`rm -rf $work_path/full_syslog.txt`;
`rm -rf $work_path/$time-log.xls`;

sub check_route
{	
	foreach $router (@router) {
        chomp($router);
        @ip_name = split(" ",$router);
		
		open(ROUTE,"$work_path/syslog/$ip_name[1]-alarm") or print "Cannot open alarm and route file: $!";
		my $total_route = 0;
		my $active_route = 0;
		my $hold_route = 0;
		my $hidden_route = 0;
		
		#inet.0: 547169 destinations, 1088761 routes (547161 active, 4 holddown, 10 hidden)
		while (<ROUTE>) {
			chomp;
			if ( /hidden/ ) {
				@route_log = split(" ",$_);
				$total_route += $route_log[3];
				$hold_route += $route_log[-4];
				$hidden_route += $route_log[-2];
				
				$route_log[5] =~ s/\(//;
				$active_route += $route_log[5]; 
			}
		}
		
		if (( $total_route >= 4000000 ) || ( $active_route >= 900000 )) {
			$total_route =~ s/(?<=\d)(?=(\d\d\d)+$)/,/g;
			$active_route =~ s/(?<=\d)(?=(\d\d\d)+$)/,/g;
			$hold_route =~ s/(?<=\d)(?=(\d\d\d)+$)/,/g;
			$hidden_route =~ s/(?<=\d)(?=(\d\d\d)+$)/,/g;
			
			`echo "RIB/FIB alert: $ip_name[1], Total=$total_route\tActive=$active_route\tHold=$hold_route\tHidden=$hidden_route" >> $work_path/TODAY_ALARMS`;	
		}				
	}
	
}

#Function generate cmd by date
sub generate_cmd
{
	my @cmd;
	if ($opt{y}) {
		@cmd = (
		"show log messages | match $year | match \"$firstlogcheck\" | except mgd | except tlv | no-more",
		"show log messages.0.gz | match $year | match \"$firstlogcheck\" | except mgd | except tlv | no-more",
		"show log messages.1.gz | match $year | match \"$firstlogcheck\" | except mgd | except tlv | no-more"
		);
	} else {		
		@cmd = (
		"show log messages | match \"$firstlogcheck\" | except mgd | except tlv | no-more",
		"show log messages.0.gz | match \"$firstlogcheck\" | except mgd | except tlv |  no-more",
		"show log messages.1.gz | match \"$firstlogcheck\" | except mgd | except tlv | no-more"
		);
	}
	return @cmd;
}

sub get_fabric_drop
{
        my ($session,$name) = @_;
        my $drop;
        $session->send("show pfe statistics traffic | match fabric\n");
        $session->expect( $timeout , "-re" , $rtr_prompt );

        $session->send("\n");
        $session->expect( $timeout , "-re" , $rtr_prompt );
        my @result = $session->before();

        foreach my $val (@result) {
                if ( $val =~ /Fabric drops               :(\s+)(\d+)/) {
                        $drop = $2;
                }
        }
        return $drop;
}

sub getstats
{
	my ($session,$name) = @_;
	$session->send("show pfe statistics traffic | no-more\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );

	#$session->send("show interfaces detail | no-more\n");
	#$session->expect( $timeout , "-re" , $rtr_prompt );
	$session->send("\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	return;
}

sub getalarm
{
	my ($session,$name) = @_;
	#Added on 2012-11-01, get chassis alarm info and store to routername-alarm file
	$session->send("show chassis alarms | no-more\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	$session->send("show route summary | no-more\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	$session->send("show lacp interfaces | match detached | no-more\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	#Added over
	
	if ( $name =~ /TXP3D/ ) {
		$session->send("show chassis fabric optical-links | except up | except state\n");
		$session->expect( $timeout , "-re" , $rtr_prompt );
	}
	$session->send("\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	return;
}

#Function get data from router
sub getlog
{
	my ($session,$name,@command) = @_;	
	foreach my $command (@command) {
		chomp($command);
		$session->send("$command\n");
		$session->expect( $timeout , "-re" , $rtr_prompt );
	}
	$session->send("\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	return;
}

#Function get data from router
sub getlog_vc
{
	my ($session,$name,@command) = @_;	
	foreach my $command (@command) {
		chomp($command);
		$session->send("$command\n");
		$session->expect( $timeout , "-re" , $rtr_prompt );
	}
	
	$session->send("request routing-engine login member 0 master\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	
	foreach my $command (@command) {
		chomp($command);
		$session->send("$command\n");
		$session->expect( $timeout , "-re" , $rtr_prompt );
	}

	$session->send("exit\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );	
	$session->send("request routing-engine login member 1 master\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	foreach my $command (@command) {
		chomp($command);
		$session->send("$command\n");
		$session->expect( $timeout , "-re" , $rtr_prompt );
	}
	
	$session->send("\n");
	$session->expect( $timeout , "-re" , $rtr_prompt );
	return;
}


#Function extract syslog from file and put into database
sub process_log
{
	my ($name) = @_;
	my @syslog;
	if ($opt{y}){
		@syslog = `egrep '[0-9]+:[0-9]+:[0-9]+' $name | awk '{ for(i=1; i<=5; i++){ \$i="" }; print \$0 }' | sed 's/(PID .*)/(PID XXX)/g' | sort | uniq -c | tr -s " " | sed 's/^[ ]//g'`;
	} else {
		@syslog = `egrep '[0-9]+:[0-9]+:[0-9]+' $name | awk '{ for(i=1; i<=4; i++){ \$i="" }; print \$0 }' | sed 's/(PID .*)/(PID XXX)/g' | sort | uniq -c | tr -s " " | sed 's/^[ ]//g'`;
	}
	foreach my $syslog (@syslog) {
		chomp($syslog);
		$syslog =~ s/\s/\t/;
		my @log = split("\t",$syslog);
		my ($processid,$eventtype,$severity,$des,$kb) = syslog_analysis($log[1]);
		
		#if ( $processid ne "Undefined") {
			chomp($processid);
			chomp($eventtype);
			chomp($severity);
			chomp($des);
			chomp($kb);
			chomp($log[1]);

			#check interface/LDP/ISIS/RSVP flapping frequency.Ignore the log if less then threshold 
			if ( (($log[1] =~ /SNMP_TRAP_LINK_DOWN/)||($log[1] =~ /ADJDOWN/)||($log[1] =~ /NBRDOWN/)||($log[1] =~ /SESSIONDOWN/)) && ($log[0] < $flap_threshold) ) {
                                next;
                        }
			
			print FULL "$time\t$name\t$log[0]\t$log[1]\t$processid\t$eventtype\t$severity\t$des\t$kb\n";
		#}
	}
	return;
}

#Function gen_excel_log_text will create log.xls which contains logs that are filtered by following rules
sub gen_excel_log_text
{
	my $filename = $time."-log.xls";
	my $workbook  = Spreadsheet::WriteExcel->new($filename);
	local $red = $workbook->add_format(bg_color => 'red',border => 1, color => 'white',valign => 'vcenter');
	my $blue = $workbook->add_format(bg_color => 'blue',border => 1, color => 'white',align => 'center',valign => 'vcenter');
	local $normal = $workbook->add_format(border => 1,valign => 'vcenter');

	#Create Original worksheet
	my $original = $workbook->add_worksheet('Original');
		
	$original->write("A1", "Date", $blue);
	$original->write("B1", "Name", $blue);
	$original->write("C1", "Repeat", $blue);
	$original->write("D1", "Message", $blue);
	$original->write("E1", "processid", $blue);
	$original->write("F1", "eventtype", $blue);
	$original->write("G1", "severity", $blue);
	$original->write("H1", "description", $blue);
	$original->write("I1", "kb", $blue);

	$original->set_column(0,0, 10 );
	$original->set_column(1,1, 26 );
	$original->set_column(2,2, 4 );
	$original->set_column(3,3, 95 );
	$original->set_column(4,4, 9 );
	$original->set_column(5,5, 9 );
	$original->set_column(6,6, 4 );
	$original->set_column(7,7, 31 );
	$original->set_column(8,8, 8 );
	
	open(ORIGINAL,"$work_path/full_syslog.txt") or die "Cannot open file full_syslog.txt: $!";
	my (@syslog,$marker);
	my $n_o = 2;
	while (<ORIGINAL>) {
		chomp;
		@syslog = split("\t",$_);
		
		# only valid processID will be recorded in excel files. Other logs are regarded as unknown
		# and will be leave in full_syslog.txt
		if ( $syslog[4] ne "Undefined") {
			if (( $syslog[6] == 1 ) || ( $syslog[6] == 2 )) {
				$original->write("A$n_o", "$syslog[0]", $red);
				$original->write("B$n_o", "$syslog[1]", $red);
				$original->write("C$n_o", "$syslog[2]", $red);
				$original->write("D$n_o", "$syslog[3]", $red);
				$original->write("E$n_o", "$syslog[4]", $red);
				$original->write("F$n_o", "$syslog[5]", $red);
				$original->write("G$n_o", "$syslog[6]", $red);
				$original->write("H$n_o", "$syslog[7]", $red);
				$original->write("I$n_o", "$syslog[8]", $red);
				$n_o++;
			}
			else {
				$original->write("A$n_o", "$syslog[0]", $normal);
				$original->write("B$n_o", "$syslog[1]", $normal);
				$original->write("C$n_o", "$syslog[2]", $normal);
				$original->write("D$n_o", "$syslog[3]", $normal);
				$original->write("E$n_o", "$syslog[4]", $normal);
				$original->write("F$n_o", "$syslog[5]", $normal);
				$original->write("G$n_o", "$syslog[6]", $normal);
				$original->write("H$n_o", "$syslog[7]", $normal);
				$original->write("I$n_o", "$syslog[8]", $normal);
				$n_o++;
			}
		}
	}
	$workbook->close();
	return;
}

#Function syslog analysis, 
#EventId;ProcessId;EventType;Severity;EventDescription;KB_URL

sub syslog_analysis
{
	my ($log) = @_;
	my ($processid,$eventtype,$severity,$des,$kb);
	
	open(SIGNATURE,"$work_path/AISDB.TXT") or die "Cannot open file AISDB.TXT: $!";
	while (<SIGNATURE>) {
		my $line = $_;
		my @tab = split(";", $line);
		
		if ( $log =~ /$tab[0]/ ) {
			$processid = $tab[1];
			$eventtype = $tab[2];
			$severity = $tab[3];
			$des = $tab[4];
			$kb = $tab[5];
			last;
		}		
		else {$processid = "Undefined";$eventtype = "Undefined";$severity="Undefined";$des="Undefined";$kb="Undefined"}
	}
	return ($processid,$eventtype,$severity,$des,$kb);
}

#Function login router directly
sub login
{
	my ($ip) = @_;
	my $session = new Expect;
	$session->raw_pty(0);
	if ($opt{S}) {
		$session->spawn("ssh $username\@$ip\n") or return undef $session;
	} else {
		$session->spawn("telnet -K $ip\n") or return undef $session;
	}
	$session->log_stdout($logstdout_switch);
	$session->expect( $timeout, [ qr/$prompt/ ]);
	if ('you sure you want to continue' eq $session->exp_match) {
		$session->send("yes\n");
		$session->expect( $timeout , "assword:");
		$session->send("$passwd\n");
		$session->expect( $timeout , "-re" , $rtr_prompt );
		$session->send("$cli_width\n");
		return $session;
	} elsif ('sername:' eq $session->exp_match || 'ogin:' eq $session->exp_match) {
		$session->send("$username\n");
		$session->expect( $timeout , "assword:");
		$session->send("$passwd\n");
		$session->expect( $timeout , "-re" , $rtr_prompt );
		$session->send("$cli_width\n");
		return $session;
	}	elsif ('assword:' eq $session->exp_match) {
			$session->send("$passwd\n");
			$session->expect( $timeout , "-re" , $rtr_prompt );
			$session->send("$cli_width\n");
			return $session;
	} else {
		return undef $session;
	}
}

#Function login router through proxy server
sub login_proxy
{
	my ($ip) = @_;
	my $session = new Expect;
	$session->raw_pty(0);
	if ($opt{S} || $opt{s} eq "proxy") {
		$session->spawn("ssh $proxy_username\@$proxy_ip\n") or return undef $session;
	} elsif ($opt{T} || $opt{t} eq "proxy") {
		$session->spawn("telnet -K $proxy_ip\n") or return undef $session;
	}
	$session->log_stdout($logstdout_switch);
	$session->expect( $timeout, [ qr/$prompt/ ]);
	if ('you sure you want to continue' eq $session->exp_match) {
		$session->send("yes\n");
		$session->expect( $timeout , "assword: ");
		$session->send("$proxy_passwd\n");
		$session->expect( $timeout , "-re" , $proxy_prompt );
		if ($opt{S} || $opt{s} eq "router") {
			$session->send("ssh $username\@$ip\n");
		} elsif ($opt{T} || $opt{t} eq "router") {
			$session->send("telnet $ip\n");
		}
		$session->expect( $timeout, [ qr/$prompt/ ]);
		if ('you sure you want to continue' eq $session->exp_match) {
			$session->send("yes\n");
			$session->expect( $timeout , "assword:");
			$session->send("$passwd\n");
			$session->expect( $timeout , "-re" , $rtr_prompt );
			$session->send("$cli_width\n");
			return $session;
		} elsif ('sername:' eq $session->exp_match || 'ogin:' eq $session->exp_match) {
			$session->send("$username\n");
			$session->expect( $timeout , "assword:");
			$session->send("$passwd\n");
			$session->expect( $timeout , "-re" , $rtr_prompt );
			$session->send("$cli_width\n");
			return $session;
		}	elsif ('assword:' eq $session->exp_match) {
				$session->send("$passwd\n");
				$session->expect( $timeout , "-re" , $rtr_prompt );
				$session->send("$cli_width\n");
				return $session;
		} else {
			return undef $session;
		}
	} elsif ('sername:' eq $session->exp_match || 'ogin:' eq $session->exp_match) {
		$session->send("$proxy_username\n");
		$session->expect( $timeout , "assword:");
		$session->send("$proxy_passwd\n");
		$session->expect( $timeout , "-re" , $proxy_prompt );
		if ($opt{S} || $opt{s} eq "router") {
			$session->send("ssh $username\@$ip\n");
		} elsif ($opt{T} || $opt{t} eq "router") {
			$session->send("telnet $ip\n");
		}
		$session->expect( $timeout, [ qr/$prompt/ ]);
		if ('you sure you want to continue' eq $session->exp_match) {
			$session->send("yes\n");
			$session->expect( $timeout , "assword:");
			$session->send("$passwd\n");
			$session->expect( $timeout , "-re" , $rtr_prompt );
			$session->send("$cli_width\n");
			return $session;
		} elsif ('sername:' eq $session->exp_match || 'ogin:' eq $session->exp_match) {
			$session->send("$username\n");
			$session->expect( $timeout , "assword:");
			$session->send("$passwd\n");
			$session->expect( $timeout , "-re" , $rtr_prompt );
			$session->send("$cli_width\n");
			return $session;
		}	elsif ('assword:' eq $session->exp_match) {
				$session->send("$passwd\n");
				$session->expect( $timeout , "-re" , $rtr_prompt );
				$session->send("$cli_width\n");
				return $session;
		} else {
			return undef $session;
		}
	} elsif ('assword:' eq $session->exp_match) {
		$session->send("$proxy_passwd\n");
		$session->expect( $timeout , "-re" , $proxy_prompt );
		if ($opt{S} || $opt{s} eq "router") {
			$session->send("ssh $username\@$ip\n");
		} elsif ($opt{T} || $opt{t} eq "router") {
			$session->send("telnet $ip\n");
		}
		$session->expect( $timeout, [ qr/$prompt/ ]);
		if ('you sure you want to continue' eq $session->exp_match) {
			$session->send("yes\n");
			$session->expect( $timeout , "assword:");
			$session->send("$passwd\n");
			$session->expect( $timeout , "-re" , $rtr_prompt );
			$session->send("$cli_width\n");
			return $session;
		} elsif ('sername:' eq $session->exp_match || 'ogin:' eq $session->exp_match) {
			$session->send("$username\n");
			$session->expect( $timeout , "assword:");
			$session->send("$passwd\n");
			$session->expect( $timeout , "-re" , $rtr_prompt );
			$session->send("$cli_width\n");
			return $session;
		}	elsif ('assword:' eq $session->exp_match) {
				$session->send("$passwd\n");
				$session->expect( $timeout , "-re" , $rtr_prompt );
				$session->send("$cli_width\n");
				return $session;
		} else {
			return undef $session;
		}
	} else {
		return undef $session;
	}
}

#Function help
sub output_usage
{
	print "\n";
	my $usage = "Usage: $0 [options] [parameters]

Options:
  -h			Help
  -r			Read router list from file. This option is mutual exclusive with -q
  -d			Login routers directly
  -p			Login router through proxy
  -S			SSH to proxy *AND* server. Don't need to specify value
  -s			SSH to proxy *OR* server. Usable value: 'proxy' or 'router'
  -T			Telnet to proxy *AND* server. Don't need to specify value
  -t			Telnet to proxy *OR* server. Usable value: 'proxy' or 'router'
  -y			For the router which has \"time-format year\" configuration
  -w			work path, e.g. /asphc/customername

Example:
  $0 -d -r router.txt -S		Load router list from file router.txt and login router directly
  $0 -p -r router.txt -S		Load router list from file router.txt and login router through proxy server
  $0 -p -q -t proxy -s router		Telnet to proxy and SSH to router
  $0 -p -q -t router -s proxy		SSH to proxy and Telnet to router
  $0 -p -q -T				Telnet to proxy and router
  $0 -p -q -S				SSH to proxy and router

Format of router.txt:

  IP Address Space Router Name
  10.10.10.10 router_name\n
";

	print $usage;
}
