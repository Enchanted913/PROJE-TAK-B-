TurkTicaret Flutter App
=======================

This repository contains a minimal Flutter application scaffold that integrates with the existing TurkTicaret backend.

Supported platforms
- Android
- Web (Chrome)

Requirements for target machine
- Install Flutter SDK (stable channel). Follow: https://docs.flutter.dev/get-started/install
- Android SDK + emulator or a physical device for Android builds.
- Chrome for web debugging.

Quick setup
1. Clone/copy this project to the target machine.
2. Open a terminal and run:

```bash
flutter pub get
flutter run -d chrome   # for web
flutter run -d emulator # for android (or flutter run with a connected device)
```

Configuration
- API base URL and token are in `lib/config.dart`. The project currently uses the provided panel URL and API token.
- **Important:** Do not commit secrets to a public repo. Rotate the token before pushing if the repo will be shared.

GitHub setup
1. Create a new repository on GitHub.
2. On your local machine, run:

```bash
cd c:\Users\tunaa\Desktop\proje_flutter
git init
git add .
git commit -m "Initial Flutter TurkTicaret app scaffold"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

3. If you want to keep `lib/config.dart` secret, replace the token after push or use GitHub Secrets in CI.

Next steps to reach feature parity with the website
1. Share the site's API documentation (endpoints, request/response formats).
2. I will implement the remaining major screens and backend integrations.
3. Add authentication persistence, offline sync, and error handling.

Security note
- Rotate `API_TOKEN` if you previously committed it or if you plan to share the repo.
