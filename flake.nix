{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils/main";
  };
  outputs = { self, nixpkgs, flake-utils, ... }@attrs:
    (flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
          pythonInputs = with pkgs; [
            python3Packages.absl-py
            python3Packages.pillow
            python3Packages.sqlalchemy
            python3Packages.flask
            # python3Packages.flask-admin
            python3Packages.websockets
          ];
      in rec {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Toosl to run stuff
            bash
            python3
            sqlite
            python3Packages.setuptools

            # Development tools/testing utils
            socat
            sox
            twinkle

            # Gadgets for forking apps
            cowsay
            figlet
            libcaca
            lynx
            nethack
          ] ++ pythonInputs;
          shellHook = ''
buildserver() {
  nixos-rebuild --flake .#server build-vm
}
runserver() {
  env QEMU_NET_OPTS="hostfwd=tcp::2222-:22,hostfwd=tcp::5060-:5060,hostfwd=tcp::5061-:5061,hostfwd=udp::5060-:5060,hostfwd=udp::5061-:5061" ./result/bin/run-server-vm &
}
sshserver() {
  ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking no" -i ./vm/server-ssh -p 2222 root@localhost
}
cleanserver() {
  rm server.qcow2
}
xtelsocket() {
  sudo socat -ls -lh -x TCP4:127.0.0.1:3615  PTY,link=/var/run/xtel/socket,user=xtel,group=xtel
}
runxtel() {
  # port 1313 is "bmc-patroldb" in /etc/services, let's go with that
  xtel -serveur localhost -service bmc-patroldb
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
cp ${./app_softmodem/app_softmodem.c} ./apps/app_softmodem.c
'';
          enableParallelBuilding = true;
        });
        packages.minitel-server = pkgs.python3Packages.buildPythonApplication {
          pname = "minitel-server";
          version = "0.0.1";
          propagatedBuildInputs = pythonInputs;
          src = ./.;
          postInstall =''
            ln -s $out/lib/python3*/site-packages/minitel/assets $out/assets
          '';
          doCheck = false;
        };
        packages.xtel = pkgs.callPackage ./xtel.nix {};
      }) // {
        overlays = {
          default = final: prev: {
            minitel-server = self.packages."${final.system}".minitel-server;
            asterisk-softmodem = self.packages."${final.system}".asterisk-softmodem;
            xtel = self.packages."${final.system}".xtel;
          };
          minitel-server = final: prev: {
            minitel-server = self.packages."${final.system}".minitel-server;
            asterisk-softmodem = self.packages."${final.system}".asterisk-softmodem;
          };
          xtel = final: prev: {
            xtel = self.packages."${final.system}".xtel;
          };
        };
        nixosModules.minitel-server = import ./minitel-server-module.nix;
        nixosModules.xtel = import ./xtel-module.nix;
        nixosConfigurations.server = nixpkgs.lib.nixosSystem {
          system = "x86_64-linux";
          specialArgs = attrs;
          modules = [
            ./vm/server.nix
          ];
        };
      });
}
