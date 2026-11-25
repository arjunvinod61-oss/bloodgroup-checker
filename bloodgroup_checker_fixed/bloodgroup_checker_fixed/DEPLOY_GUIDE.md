# Publish HemaCheck as a public website (Streamlit Community Cloud)

This is the recommended public-hosting route. Streamlit Community Cloud deploys directly from GitHub and assigns a public `*.streamlit.app` URL.

## A. Put the project on GitHub

1. Sign in to https://github.com/ (create an account if needed).
2. Click **New repository**.
3. Name it `bloodgroup-checker` (or another name).
4. Choose **Public**, then create the repository.
5. Open the empty repository and choose **Add file → Upload files**.
6. Extract `bloodgroup_checker_fixed.zip` on your computer.
7. Upload the *contents* of the `bloodgroup_checker_fixed` folder (not the enclosing folder itself). The repository root must contain `app.py`, `requirements.txt`, `bloodgroup_checker/`, and `tests/`.
8. Commit the uploaded files.

## B. Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/
2. Choose **Continue with GitHub** and authorize Streamlit.
3. Click **Create app**.
4. Select your GitHub repository, branch `main`, and main file path `app.py`.
5. Optionally choose a memorable app subdomain.
6. Click **Deploy** and wait for the build to finish.
7. Streamlit will provide a public URL such as `https://your-app-name.streamlit.app/`. Share that URL.

No API keys or secrets are required by this project.

## C. Update the website later

Edit the relevant files in GitHub and commit the changes. Community Cloud watches the repository and redeploys updates.

## Troubleshooting

- **ModuleNotFoundError: bloodgroup_checker**: confirm the `bloodgroup_checker` folder is at the repository root beside `app.py`.
- **Missing dependency**: confirm `requirements.txt` is at the repository root and includes `streamlit` and `pandas`.
- **App fails to start**: open the app's Manage app / logs view in Community Cloud and inspect the first Python traceback.
- **Wrong entrypoint**: set the main file path to exactly `app.py`.

Official deployment documentation: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
