{
  description = "web chat backend flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs =
    { nixpkgs, ... }@inputs:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
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
          ))
        ];
      };

    };
}
