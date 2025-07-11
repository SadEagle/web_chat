# shell.nix
{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
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
}
