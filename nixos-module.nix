{ config, lib, self, pkgs, ... }:
let cfg = config.services.minitel-server;
in {
  options.services.minitel-server = with lib; {
    enable = mkEnableOption (lib.mdDoc "minitel-server");

    port = mkOption {
      type = types.port;
      default = 3615;
      description = lib.mdDoc "Listen port for minitel-server";
    };

    ip = mkOption {
      type = types.str;
      default = "127.0.0.1";
      description = lib.mdDoc "IP address to listen on for minitel-server";
    };

    dbPath = mkOption {
      type = types.str;
      default = "sqlite://";
      description = lib.mdDoc "Database path to connect to, in SQLAlchemy engine path format.";
    };

    dataDir = mkOption {
      type = types.str;
      default = "minitel-server";
      description = lib.mdDoc ''
          The directory below {file}`/var/lib` where minitel-server stores its data.
        '';
    };

    user = mkOption {
      type = types.str;
      default = "minitel-server";
      description = lib.mdDoc "User account under which minitel-server runs.";
    };

    group = mkOption {
      type = types.str;
      default = "minitel-server";
      description = lib.mdDoc "Group account under which minitel-server runs.";
    };

    openFirewall = mkOption {
      type = types.bool;
      default = false;
      description = lib.mdDoc ''
          Open ports in the firewall for minitel-server.
        '';
    };

    package = mkOption {
      type = types.package;
      default = pkgs.minitel-server;
      defaultText = literalExpression "pkgs.minitel-server";
      description = lib.mdDoc "minitel-server derivation to use";
    };
  };

  config = with lib; mkIf cfg.enable {
    nixpkgs.overlays = [
      self.overlays.default
    ];

    systemd.services.minitel-server = {
      description = "An applicative server for Minitel clients";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];

      serviceConfig = {
        Type = "simple";
        User = cfg.user;
        Group = cfg.group;

        StateDirectory = cfg.dataDir;

        # TODO ip, port, dbPath
        ExecStart = "${cfg.package}/bin/main.py";

        Restart = "on-failure";
      };
    };

    networking.firewall = mkIf cfg.openFirewall {
      allowedTCPPorts = [ cfg.port ];
    };

    users.users = mkIf (cfg.user == "minitel-server") {
      minitel-server = {
        isSystemUser = true;
        group = cfg.group;
      };
    };

    users.groups = mkIf (cfg.group == "minitel-server") {
      minitel-server = {};
    };
  };
}
