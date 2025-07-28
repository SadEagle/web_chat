{
  description = "web chat backend flake";

  inputs = {
    # TODO: come back to unstable when better internet
    # nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs =
    { nixpkgs, ... }@inputs:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pkgsModule =
        with pkgs;
        (python313.withPackages (
          python-pkgs: with python-pkgs; [
            sqlite
            psycopg2

            bcrypt
            pyjwt
            passlib
            pytest
            celery
            fastapi
            pydantic-settings
            fastapi-cli
            sqlalchemy
            httpx

            python-multipart
            email-validator
          ]
        ));
      backendApp = pkgs.stdenv.mkDerivation {
        name = "backend";
        src = ./app;
        installPhase = ''
          mkdir -p $out/app
          cp -r $src/* $out/app/
        '';
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pkgsModule ];
      };

      packages.${system}.container = pkgs.dockerTools.buildImage {
        name = "web_chat_backend";
        tag = "latest";
        copyToRoot = [
          pkgsModule
          backendApp
        ];
        config = {
          Expose = "8000";
          Cmd = [
            "${pkgsModule}/bin/fastapi"
            "run"
            "${backendApp}/app/main.py"
            "--host"
            "0.0.0.0"
          ];
        };
      };
    };
}
