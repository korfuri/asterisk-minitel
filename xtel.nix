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
    imake


    xorg.gccmakedep
    xorg.bdftopcf
    xorg.xbitmaps
    xorg.libXmu
    xorg.libXaw
    xorg.libXext
    xorg.mkfontdir
    
    
    ### Debian deps
    

    # ??? # x11-common #        X Window System (X.Org) infrastructure 

    glibc # libc6 # (>= 2.34) [not alpha, ia64, sh4]
    # GNU C Library: Shared libraries
    #        also a virtual package provided by libc6-udeb 

    # libc6.1 # (>= 2.34) [alpha]  #??
      #  GNU C Library: Shared libraries
      #  also a virtual package provided by libc6.1-udeb 

    # libice6 # (>= 1:1.0.0) [sparc64]  # ??
    # X11 Inter-Client Exchange library 

    libjpeg_turbo #  libjpeg62-turbo #(>= 1.3.1)
    #libjpeg-turbo JPEG runtime library 

    # libsm6 # [sparc64]  # ??
    # X11 Session Management library 

    xorg.libX11  # libx11-6 #       X11 client-side library 
    # libxext6 # [sparc64]  # ??
    # X11 miscellaneous extension library 

    motif # libxm4 # (>= 2.3.4)     Motif - X/Motif shared library 

    xorg.libXpm  # libxpm4 #     X11 pixmap library 

    xorg.libXt  #    libxt6 #     X11 toolkit intrinsics library 

    netpbm #        Graphics conversion tools between image formats 

    xinetd # openbsd-inetd      OpenBSD Internet Superserver 
    # or inet-superserver
    # virtual package provided by inetutils-inetd, openbsd-inetd, rlinetd, xinetd 

    xorg.fontutil # fonts-utils #    X Window System font utility programs 




    #### Freshports deps:
    # bdftopcf # : x11-fonts/bdftopcf
    # mkfontdir # : x11-fonts/mkfontdir
    # mkfontscale # : x11-fonts/mkfontscale
    # imake # : devel/imake
    # xaw7.pc # : x11-toolkits/libXaw
    # xbitmaps.pc # : x11/xbitmaps
    # # Runtime dependencies:
    # xaw7.pc # : x11-toolkits/libXaw
    # xbitmaps.pc # : x11/xbitmaps
    # # Library dependencies:
    # jpeg.11 # : graphics/jpeg
  ];

  patches = [
    ./xtel-build.patch
  ];

  # preConfigure = ''
  #   sed -e 's@outpath@'"$out"'@' -i Imakefile
  # '';
  
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
