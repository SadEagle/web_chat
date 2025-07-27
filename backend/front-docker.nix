{
  pkgs ? import <nixpkgs> { },
  pkgsLinux ? import <nixpkgs> { system = "x86_64-linux"; },
}:

pkgs.dockerTools.buildImage {

  name = "chat-front";
  tag = [
    "latest"
    "0.1"
  ];

  config = {

    Cmd = [ "${pkgsLinux.hello}/bin/hello" ];
  };

}
