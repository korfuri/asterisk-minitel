{ self, ... }:
{
  # This is a demo config using asterisk-softmodem.
  #
  # Easiest way to play around with it:
  #  $ nixos-rebuild --flake .#server build-vm
  #  $ QEMU_NET_OPTS="hostfwd=tcp::2222-:22" ./result/bin/run-server-vm &
  #  $ ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking no" -i ./server-ssh -p 2222 root@localhost
  # Convenience aliases for 
  networking.hostName = "server";

  services.asterisk = {
    enable = true;
    package = self.packages."x86_64-linux".asterisk-softmodem;
    confFiles = {
      "extensions.conf" = (builtins.readFile ./server/extensions.conf);
      "pjsip.conf" = (builtins.readFile ./server/pjsip.conf);      
    };
    useTheseDefaultConfFiles = [
      
    ];
  };
  services.openssh = {
    enable = true;
    settings.PermitRootLogin = "without-password";
  };
  users.users.root = {
    initialPassword = "server";
    openssh.authorizedKeys.keys = [
      (builtins.readFile ./server-ssh.pub)
    ];
  };
  system.stateVersion = "23.11";
}
