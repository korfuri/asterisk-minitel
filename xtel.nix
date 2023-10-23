{ lib
, stdenv
, fetchurl
, imake

, glibc
, libjpeg_turbo
, motif
, netpbm
, xinetd
, xorg
}:
stdenv.mkDerivation rec {
  pname = "xtel";
  version = "3.3.0-26";

  src = fetchurl {
    url = "https://salsa.debian.org/debian/xtel/-/archive/master/xtel-master.tar.gz";
    sha256 = "sha256-aNQSVWVHfZoYUYJmucBxIX98mUAId/2V/RKAkx3DiFw=";
  };

  buildInputs = [
    glibc
    imake
    libjpeg_turbo
    motif
    netpbm
    xinetd
    xorg.bdftopcf
    xorg.fontutil
    xorg.gccmakedep
    xorg.libX11
    xorg.libXaw
    xorg.libXext
    xorg.libXmu
    xorg.libXpm
    xorg.libXt
    xorg.mkfontdir
    xorg.xbitmaps
  ];

  patches = [
    ./xtel-build.patch
    ./xtel-lignes.patch
  ];

   configurePhase = ''
    imake -DUseInstalled -I/nix/store/lzq8ly43klcnvfiqcsc7770cvzr773s6-imake-1.0.9/lib/X11/config
  '';
  
  buildPhase = ''
  	xmkmf
    make Xtel
  '';

  preInstall = ''
    mkdir -p $out/bin
    mkdir -p $out/etc
  '';

  installPhase = ''
    runHook preInstall
    cp xteld $out/bin
    cp xtel $out/bin
    cp xtel.lignes $out/etc
    cp xtel.services $out/etc
    runHook postInstall
  '';
}
