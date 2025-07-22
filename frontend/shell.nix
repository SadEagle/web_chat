# shell.nix
{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  packages = with pkgs; [
    # nodejs_24
    nodejs

    # WARN: need only for fast wrighting web part with fastapi
    (python313.withPackages (
      python-pkgs: with python-pkgs; [
        fastapi
        fastapi-cli
      ]
    ))

  ];

  # NOTE: cant install npm in nixos way and dont want to spend more time then alread spend
  shellHook = ''
    if [ ! -d "node_modules" ]; then
      npm init -y --silent
      npm install typescript
      # npx tsc --init
      npm install jwt-decode
    fi
  '';
}
