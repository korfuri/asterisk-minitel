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
  };
  services.openssh = {
    enable = true;
    settings.PermitRootLogin = "without-password";
  };
  users.users.root.openssh.authorizedKeys.keys = [
    (builtins.readFile ./server-ssh.pub)
  ];
  system.stateVersion = "23.11";
}
