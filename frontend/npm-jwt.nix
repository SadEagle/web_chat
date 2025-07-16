{
  pkgs,
}:

pkgs.buildNpmPackage (finalAttrs: {
  pname = "jwt-decode";
  version = "4.0.0";

  src = pkgs.fetchFromGitHub {
    owner = "auth0";
    repo = "jwt-decode";
    tag = "v${finalAttrs.version}";
    hash = "sha256-BlwnZGO+oofAtfIArJE+4NF9mX+nj8JJC37FvW4x5To=";
  };

  npmDepsHash = "sha256-JucRRK3+LEX9UbyNU1dn0yqN0uGsI12FuJ+mtveW1cI=";

  # The prepack script runs the build script, which we'd rather do in the build phase.
  npmPackFlags = [ "--ignore-scripts" ];

  NODE_OPTIONS = "--openssl-legacy-provider";
})
