{
  description = "web chat frontend flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      frontendApp = pkgs.stdenv.mkDerivation {
        name = "web-chat-frontend";
        src = ./.;
        buildInputs = with pkgs; [
          typescript
        ];
        buildPhase = ''
          tsc
        '';
        installPhase = ''
          mkdir -p $out
          cp -r ./web/* $out
        '';
      };
      nginxConf = pkgs.writeText "nginx.conf" ''
        user nobody nobody;
        daemon off;
        error_log /dev/stdout info;
        pid /dev/null;
        events {}
        http {
          access_log /dev/stdout;
          server {
            listen 80;
            root ${frontendApp};
            location = / {
              return 302 $scheme://$http_host/home;
            }
            location / {
              try_files $uri $uri.html =404;
            }
            location /css/ {
              add_header Content-Type text/css;
            }
            location /js/ {
              add_header Content-Type application/javascript;
            }
          }
        }
      '';

    in
    {
      # TODO: add volume for logs
      packages.${system}."container" = pkgs.dockerTools.buildImage {
        name = "web-chat-frontend";
        tag = "latest";
        copyToRoot = with pkgs; [
          fakeNss
          nginx
          frontendApp
        ];
        config = {
          ExposedPorts = {
            "80/tcp" = { };
          };
          Cmd = [
            "nginx"
            "-c"
            nginxConf
          ];
        };
        runAsRoot = ''
          mkdir -p tmp/nginx_client_body

          # nginx still tries to read this directory even if error_log
          # directive is specifying another file :/
          mkdir -p var/log/nginx
        '';
      };
    };
}
