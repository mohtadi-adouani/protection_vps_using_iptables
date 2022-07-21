# -*- coding: utf-8 -*-
"""
Using https://portal-clienti.dedicatserver.ro/knowledgebase/1/SetariorSettings-firewall---iptable.html
"""
SSH_PORT = 22     # ssh port
FTP_PORT = 21
HTTP_PORT = 80
HTTPS_PORT = 443
SMTP1_PORT = 25
SMTP2_PORT = 465
POP31_PORT = 143
POP32_PORT = 993
DNS_PORT = 53
MYSQL_PORT = 3306
SAMP_PORT = 7777
MINECRAFT_PORT = 25565
import os


def execute(cmd:str,sudo=True):
    """
    Execute shell cmd wit sudo or not
    """
    if sudo:
        os.system('sudo '+cmd)
    else:
        os.system(cmd)


def ssh(port=SSH_PORT):
    """Allow SSH connections on tcp port 22"""
    execute("iptables –A INPUT –p tcp –-dpor t"+ str(port) +" –j ACCEPT")
    

def set_default_policies():
    """Set default policies for INPUT, FORWARD and OUTPUT chains"""
    execute("iptables –P INPUT DROP")
    execute("iptables –P FORWARD DROP")
    execute("iptables –P OUTPUT ACCEPT")

def set_access_localhost():
    """Set access for localhost"""
    execute("iptables –A INPUT –i lo –j ACCEPT")

def set_established_and_related():
    """ACCEPT packets belonging to established and related connections"""
    execute("iptables –A INPUT –m state –-state ESTABLISHED,RELATED –j ACCEPT")

def ftp(port=FTP_PORT):
    """FTP"""
    execute("iptables –A INPUT –p tcp –-dport "+str(port)+" -j ACCEPT")

def http(http_port=HTTP_PORT,https_port=HTTPS_PORT):
    """HTTP/s"""
    execute("iptables -A INPUT -p tcp --dport "+str(http_port)+" -j ACCEPT")
    execute("iptables -A INPUT -p tcp --dport "+str(https_port)+" -j ACCEPT")

def smtp(smtp1_port=SMTP1_PORT,smtp2_port=SMTP2_PORT):
    """SMTP"""
    execute("iptables -A INPUT -p tcp --dport "+str(smtp1_port)+" -j ACCEPT")
    execute("iptables -A INPUT -p tcp --dport "+str(smtp2_port)+" -j ACCEPT")


def pop3(pop31_port = POP31_PORT,pop32_port = POP32_PORT):
    """POP3"""
    execute("iptables -A INPUT -p tcp --dport "+str(pop31_port)+" -j ACCEPT")
    execute("iptables -A INPUT -p tcp --dport "+str(pop32_port)+" -j ACCEPT")

def dns(dns_port= DNS_PORT):
    """DNS"""
    execute("iptables -A INPUT -p tcp,udp --dport "+str(dns_port)+" -j ACCEPT")

def mysql(mysql_port= MYSQL_PORT):
    """MySql"""
    execute("iptables -A INPUT -p tcp --dport "+str(mysql_port)+" -j ACCEPT")


def counter_strike_and_steam():
    """COUNTER STRIKE/STEAM and Steam Friends Service"""
    execute("iptables -A INPUT -p udp --dport 1200 -j ACCEPT")
    execute("iptables -A INPUT -p udp --dport 4380 -j ACCEPT")

    """STEAM MAIN UDP"""
    execute("iptables -A INPUT -p udp --dport 27000:27015 -j ACCEPT")
    execute("iptables -A INPUT -p udp --dport 27015:27030 -j ACCEPT")
    execute("iptables -A INPUT -p tcp --dport 27014:27050 -j ACCEPT")


def teamspeak():
    """TEAMSPEAK"""
    execute("iptables -A INPUT -p udp --dport 9987 -j ACCEPT")     #Voice
    execute("iptables -I INPUT -p tcp --dport 30033 -j ACCEPT")     #Data
    execute("iptables -I INPUT -p tcp --dport 41144 -j ACCEPT")     #TSDNS
    execute("iptables -I INPUT -p udp --dport 10011 -j ACCEPT")     #Query
    execute("iptables -A INPUT -p udp --dport 2011:2110 -j ACCEPT")     #Weblist, Accouting Server /licences)

def samp_protection(samp_port=SAMP_PORT):
    """SA:MP (+Protection)"""
    execute("iptables -N SAMP-DDOS")
    execute("iptables -A INPUT -p udp --dport "+str(samp_port)+" -m ttl --ttl-eq=128 -j SAMP-DDOS")
    execute("iptables -A SAMP-DDOS -p udp --dport "+str(samp_port)+" -m length --length 17:604 -j DROP")
    execute("iptables -A INPUT -p udp -m ttl --ttl-eq=128 -j DROP")
    execute("iptables -A INPUT -p udp --dport "+str(samp_port)+" -m limit --limit 6/s --limit-burst 12 -j DROP")

def samp_without_protection(samp_port=SAMP_PORT):
    """SA:MP (without Protection)"""
    execute("iptables -A INPUT -p udp --dport "+str(samp_port)+" -j ACCEPT")

def metin():
    """METIN"""
    execute("iptables -A INPUT -p tcp -m tcp --dport 1022 -j ACCEPT")


def minecraft(minecraft_port=MINECRAFT_PORT):
    """Minecraft default port"""
    execute("iptables -A INPUT -p tcp --dport "+str(minecraft_port)+" -j ACCEPT")


def syn_flood():
    """PROTECTION
    SYN-FLOOD This will detect all new TCP connections and will not allow not more than 1 new connections per second.
    This value can be edited as needed."""
    execute("iptables -A INPUT -p tcp --syn -m limit --limit 1/s -j ACCEPT")

def port_scan():
    """Furtive port scanner"""
    execute("iptables -A INPUT -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 2/s --limit-burst 2 -j ACCEPT")

def ping():
    """ACCEPT") INCOMING PING (first 2 rules for protection smurf attacks/ping of death)"""
    execute("iptables -A INPUT -p icmp -m icmp --icmp-type address-mask-request -j DROP")
    execute("iptables -A INPUT -p icmp -m icmp --icmp-type timestamp-request -j DROP")
    execute("iptables -A INPUT -p icmp -m icmp -m limit --limit 1/second -j ACCEPT")

def drop_invalid_packets():
    """ Droping all invalid packets"""
    execute("iptables -A INPUT -m state --state INVALID -j DROP")
    execute("iptables -A FORWARD -m state --state INVALID -j DROP")
    execute("iptables -A OUTPUT -m state --state INVALID -j DROP")


def protection_portscans():
    """ Protecting portscans
    Attacking IP will be locked for 24 hours (3600 x 24 = 86400 Seconds)"""
    execute("iptables -A INPUT -m recent --name portscan --rcheck --seconds 86400 -j DROP")

def remove_protection_portscans():
    """ Remove attacking IP after 24 hours"""
    execute("iptables -A INPUT -m recent --name portscan --remove")

def save():
    """SAVE iptables"""
    execute("service iptables save")

def restart():
    """RESTART iptables"""
    execute("service iptables restart")

def show_list():
    """List iptables"""
    execute("iptables -L --line-numbers")
