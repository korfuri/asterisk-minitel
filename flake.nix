{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils/main";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in rec {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [ ];
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
      });
}
