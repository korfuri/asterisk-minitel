{ config, lib, self, pkgs, ... }:
let cfg = config.services.xtel;
in {
  options.services.xtel = with lib; {
    enable = mkEnableOption (lib.mdDoc "xtel");

    port = mkOption {
      type = types.port;
      default = 1313;
      description = lib.mdDoc "Listen port for xteld";
    };

    package = mkOption {
      type = types.package;
      default = pkgs.xtel;
      defaultText = literalExpression "pkgs.xtel";
      description = lib.mdDoc "xtel derivation to use";
    };

    user = mkOption {
      type = types.str;
      default = "xtel";
      description = lib.mdDoc "User account under which xteld runs.";
    };
  };

  config = with lib; mkIf cfg.enable {
    nixpkgs.overlays = [
      self.overlays.xtel
    ];

    services.xinetd = {
      enable = true;
      services = [
        {
          name = "xteld";
          port = cfg.port;
          server = "${cfg.package}/bin/xteld";
          unlisted = true;
          user = cfg.user;
        }
      ];
    };

    users.users = mkIf (cfg.user == "xtel") {
      xtel = {
        isSystemUser = true;
        group = "xtel";
      };
    };
    users.groups = mkIf (cfg.user == "xtel") {
      xtel = {};
    };

    environment.etc."xtel/xtel.lignes" = mkDefault {
      source = "${cfg.package}/etc/xtel.lignes";
    };
    environment.etc."xtel/xtel.services" = mkDefault {
      source = "${cfg.package}/etc/xtel.services";
    };
    systemd.tmpfiles.rules = [
      "d /run/xtel 0700 ${cfg.user} nogroup -"
    ];
  };
}
