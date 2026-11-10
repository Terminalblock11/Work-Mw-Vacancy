# WorkMw Vacancies (Android)

The WorkMw Vacancy Generator (`www/index.html`) wrapped as an Android app with Capacitor.
Files are saved/shared through the native Android share sheet (Filesystem + Share plugins).

## Get the APK
1. Create a new GitHub repository and upload everything in this folder (keep the `.github` folder).
2. Open the **Actions** tab -> **Build Android APK**. It runs automatically on push; you can also press **Run workflow**.
3. When it finishes (about 5-8 minutes), open the run and download **WorkMw-Vacancies-APK** under *Artifacts*.
4. Unzip it, send `WorkMw-Vacancies.apk` to your phone, and install it (allow "Install unknown apps" if asked).

## Updating the app
Replace `www/index.html` with the new version and push. A new APK is built automatically.
