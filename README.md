### About the project

It's **dummy project** and representation of my current skills.

Current project is a simple attempt of web-chat application implementation. Main target is to make something basic full-stack like and understand all development processes, file structure and instruments.

Plans:
 - [x] FastAPI backend
 - [x] SQLAlchemy database
 - [x] Simple HTML/CSS/TS frontend
 - [x] JWT auth
 - [x] Docker/Compose with traefik and nginx (localhost only)
 - [ ] Proper pytests (now only part of integration tests some routes)
 - [ ] CI/CD integration
 - [ ] Async functions
 - [ ] Proper User work. Now user may chat only with itself
 - [ ] Proper user/message/chat communication with db
 - [ ] Message communication with websocket between active users

File structure source:
- [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)

This project  previously was written with NixOS instruments. It looks that make dev containers in NixOS is impossible, so it was duplicate with ubuntu based docker/compose. I.e. `.nix` files aren't influence on project itself and left here for now.
