{
  description = "web chat backend flake";

  inputs = {
    # TODO: come back to unstable when better internet
    # nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonModule =
        with pkgs;
        (python313.withPackages (
          python-pkgs: with python-pkgs; [
            fastapi
            fastapi-cli
            sqlalchemy
            sqlite
            psycopg2
            pytest
            httpx
            bcrypt
            passlib
            pyjwt
            python-multipart
            email-validator
            pydantic-settings
          ]
        ));
      backendApp = pkgs.stdenv.mkDerivation {
        name = "backend";
        src = ./app;
        installPhase = ''
          mkdir -p $out/app
          cp -r $src/* $out/app
        '';
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pythonModule ];
      };

      packages.${system}.container = pkgs.dockerTools.buildImage {
        name = "web-chat-backend";
        tag = "latest";
        copyToRoot = [
          backendApp
          pythonModule
        ];
        config = {
          ExposedPorts = {
            "8000" = { };
          };
          Cmd = [
            "${pythonModule}/bin/fastapi"
            "run"
            "${backendApp}/app/main.py"
            "--host"
            "0.0.0.0"
          ];
        };
      };
    };
}
