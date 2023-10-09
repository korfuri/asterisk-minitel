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
        packages.asterisk-softmodem-src = pkgs.fetchFromGitHub {
          owner = "billsimon";
          repo = "asterisk-Softmodem";
          rev = "fc9c92249bc43657687d95a8b731ab8be158e687";
          # sha256 = "sha256-SLh9bNhjYOKOOT34v8zlW+qiYEl1i0AHFrzSvGoBBDY=";
          sha256 = "sha256-5NkvwI8v7Gi8GUflp2vajT79TK1EjMv1WeAKXoxLoOs=";
        };
        packages.asterisk-softmodem = pkgs.asterisk.overrideAttrs (o: {
          buildInputs = o.buildInputs ++ [
            # packages.asterisk-softmodem-src
            pkgs.spandsp
          ];
          postPatch = o.postPatch + ''
cp ${packages.asterisk-softmodem-src}/app_softmodem.c ./apps/app_softmodem.c
'';
        });
      });
}
