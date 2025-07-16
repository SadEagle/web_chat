# shell.nix
{
  pkgs ? import <nixpkgs> { },
}:

let
  # jwtdecode = import ./npm-jwt.nix { inherit pkgs; };
  jwtdecode = pkgs.callPackage ./npm-jwt.nix { };
in
pkgs.mkShell {
  packages = with pkgs; [
    nodejs_24
    jwtdecode
  ];
}
