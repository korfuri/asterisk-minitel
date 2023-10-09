{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils/main";
  };
  outputs = { self, nixpkgs, flake-utils, ... }@attrs:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in rec {
        devShells.default = pkgs.mkShell {
          shellHook = ''
buildserver() {
  nixos-rebuild --flake .#server build-vm
}
runserver() {
  env QEMU_NET_OPTS="hostfwd=tcp::2222-:22,hostfwd=tcp::5060-:5060,hostfwd=tcp::5061-:5061,hostfwd=udp::5060-:5060,hostfwd=udp::5061-:5061" ./result/bin/run-server-vm &
}
sshserver() {
  ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking no" -i ./server-ssh -p 2222 root@localhost
}
cleanserver() {
  rm server.qcow2
}
PS1="(asterisk-minitel)"$PS1
'';
        };
        packages.asterisk-softmodem = pkgs.asterisk.overrideAttrs (o: {
          buildInputs = o.buildInputs ++ [
            # packages.asterisk-softmodem-src
            pkgs.spandsp
          ];
          postPatch = o.postPatch + ''
cp ${./app_softmodem.c} ./apps/app_softmodem.c
'';
          enableParallelBuilding = true;
        });
      }) // {
        nixosConfigurations.server = nixpkgs.lib.nixosSystem {
          system = "x86_64-linux";
          specialArgs = attrs;
          modules = [ ./server.nix ];
        };
      };
}
