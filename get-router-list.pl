#!/usr/bin/perl
use lib "/home/hfzhang/perl5/lib/perl5";

#Author: hfzhang
#It's used for daily crontab to get CMNET all Juniper router list.
#Usage: ./get-router-list.pl 218.200.250.17

#Load module
use Expect;
use FindBin '$Bin';
use Getopt::Std;

#Usage: perl ./get-router-list.pl 218.200.250.17

#Parameters for routers
$username = "JuniperCheck";
$passwd = "Pcsw\&\$csV5";
$rtr_prompt = "JuniperCheck.*>";

#Parameters for Proxy server
$proxy_ip = "218.200.250.31";
$proxy_username = "JuniperCheck";
$proxy_passwd = "Pcsw\&\$csV5";
$proxy_prompt = ">";

#Others parameters
$timeout = 30;
$logstdout_switch = 1;
$prompt = '(assword:)|(id_[dr]sa\':)|(you sure you want to continue)|(sername:)|(ogin:)';
$work_path = $Bin;


#Generate command
@command = generate_cmd();

#Function generate cmd by date
sub generate_cmd
{
        my @cmd;
        @cmd = (
            "show isis hostname | match \"M320|T1600|T4000|TXP|MX960\" | no-more"
        );
        return @cmd;
}


#Function login router through proxy server
sub login_proxy
{
        my ($ip) = @_;
        my $session = new Expect;
        $session->raw_pty(0);
 	$session->spawn("telnet $proxy_ip\n") or return undef $session;
        $session->log_stdout($logstdout_switch);
        $session->expect( $timeout, [ qr/$prompt/ ]);
        if ('you sure you want to continue' eq $session->exp_match) {
                $session->send("yes\n");
                $session->expect( $timeout , "assword:");
                $session->send("$proxy_passwd\n");
                $session->expect( $timeout , "-re" , $proxy_prompt );
                $session->send("telnet $ip\n");
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
                }       elsif ('assword:' eq $session->exp_match) {
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
                $session->send("telnet $ip\n");
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
                }       elsif ('assword:' eq $session->exp_match) {
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
                $session->send("telnet $ip\n");
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
                }       elsif ('assword:' eq $session->exp_match) {
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

#Function get data from router
sub getdata
{
        my ($session,@command) = @_;
	open (STDOUT, "| tee -i $work_path/cmnet-all-routers-dynamic.log");
#        $session->log_file("$work_path/cmnet-all-router-dynamic.log","w");
        foreach my $command (@command) {
                chomp($command);
                $session->expect( $timeout , "-re" , $rtr_prompt );
                $session->send("$command\n");
        }
        $session->expect( $timeout , "-re" , $rtr_prompt );
        $session->send("exit\n");
        $session->log_file( undef );
        $session->expect( $timeout , "-re" , $proxy_prompt );
        $session->send("exit\n");
        $session->hard_close();
        return;
}


#Main Program
#Login router and get data

$session = login_proxy($ARGV[0]);

if (!defined($session)) {
        print "Can not login router \n";
} else {
        getdata($session,@command);
}

`/asphc/cmnet/parse.sh`;

