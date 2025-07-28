{
  description = "web chat frontend flake";

  inputs = {
    # nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      frontendApp = pkgs.stdenv.mkDerivation {
        name = "frontend";
        src = ./.;
        buildInputs = with pkgs; [
          nodejs
          typescript
        ];
        buildPhase = ''
          tsc
        '';
        installPhase = ''
          mkdir -p $out
          cp -p -r $src/* $out
        '';
      };
      nginxConfig = pkgs.writeText "nginx.conf" ''
        http {
          server {
            listen 80;
            location / {
              root ${frontendApp}
              try_files $uri $uri.html =404;
            }
          }
        }
      '';
    in
    {
      # TODO: add volume for logs
      packages.${system}."container" = pkgs.dockerTools.buildImage {
        name = "web-chat-front";
        tag = "latest";
        copyToRoot = [
          pkgs.nginx
          frontendApp
        ];
        config = {
          ExposedPorts = {
            "80" = { };
          };
          Cmd = [
            "nginx"
            "-g"
            "daemon off;"
          ];
        };
        extraCommands = ''
          mkdir -p etc/nginx
          cp ${nginxConfig} etc/nginx/nginx.conf

          mkdir -p var/log/nginx
        '';
      };
    };
}
