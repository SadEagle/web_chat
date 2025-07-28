{
  description = "web chat frontend flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { nixpkgs }@inputs:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {

      packages.${system}."docker" = pkgs.dockerTools.buildImage {
        name = "web_chat_back";
        tag = "latest";
      };
    };
}
