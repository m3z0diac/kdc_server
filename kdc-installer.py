import subprocess
import os

# Configuration Variables
REALM = "EXAMPLE.COM"
KDC_HOSTNAME = "kali"
ADMIN_PRINCIPAL = "admin/admin"
CONFIG_TEMPLATE = f"""
[libdefaults]
    default_realm = CYBER.LOCAL
    dns_lookup_realm = false
    dns_lookup_kdc = false
    ticket_lifetime = 24h
    renew_lifetime = 7d
    forwardable = true
    proxiable = true
    rdns = false
    ccache_type = 4
    kdc_timesync = 1
    fcc-mit-ticketflags = true

[realms]
    CYBER.LOCAL = {
        kdc = localhost
        admin_server = localhost
    }

[domain_realm]
    .cyber.local = CYBER.LOCAL
    cyber.local = CYBER.LOCAL

    example.com = {REALM}
"""

def run_command(command, input_text=None):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, input=input_text, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error:\n{result.stderr}")
    else:
        print(f"Success:\n{result.stdout}")
    return result

def install_packages():
    run_command("apt update")
    run_command("apt install -y krb5-kdc krb5-admin-server")

def configure_kerberos():
    print("Writing /etc/krb5.conf...")
    with open("/etc/krb5.conf", "w") as conf_file:
        conf_file.write(CONFIG_TEMPLATE)

def create_kdc_database():
    run_command("krb5_newrealm")

def create_admin_principal():
    print("Creating admin principal...")
    addprinc_cmd = f"addprinc {ADMIN_PRINCIPAL}"
    run_command("kadmin.local", input_text=f"{addprinc_cmd}\n")

def manage_services():
    run_command("systemctl start krb5-admin-server")
    run_command("systemctl enable krb5-admin-server")
    run_command("systemctl restart krb5-admin-server")
    run_command("systemctl status krb5-admin-server")

def main():
    install_packages()
    configure_kerberos()
    create_kdc_database()
    create_admin_principal()
    manage_services()
    print("\nKerberos KDC installation and configuration completed!")

if __name__ == "__main__":
    main()
