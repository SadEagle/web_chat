{
  description = "web chat frontend flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
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
        fromImage = pkgs.dockerTools.pullImage {
          imageName = "nginx";
          imageDigest = "sha256:ae4d4425caf0466532f4c0baf12a55070e827898b4584b8bc181adca9453d3af";
          finalImageTag = "alpine";
          sha256 = "sha256:ae4d4425caf0466532f4c0baf12a55070e827898b4584b8bc181adca9453d3af";
        };
        copyToRoot = [
          frontendApp
        ];
        runAsRoot = ''
          cp ${nginxConfig} /etc/nginx/nginx.config
        '';
        config = {
          ExposedPorts = {
            "80" = { };
          };
        };
      };
    };
}
