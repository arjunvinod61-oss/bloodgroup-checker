# Run HemaCheck in Google Colab

1. Open https://colab.research.google.com/
2. Create a **New notebook**.
3. Upload `bloodgroup_checker_fixed.zip` using the Files (folder) panel or run:

```python
from google.colab import files
uploaded = files.upload()  # choose bloodgroup_checker_fixed.zip
```

4. Extract the project:

```python
import zipfile
with zipfile.ZipFile("bloodgroup_checker_fixed.zip") as z:
    z.extractall("/content")
%cd /content/bloodgroup_checker_fixed
```

5. Install the dependencies:

```python
!pip -q install -r requirements.txt
```

6. Run the automated tests (optional but recommended):

```python
!pytest -q
```

7. Start the dashboard:

```python
!streamlit run app.py --server.port 8501 --server.headless true > /content/streamlit.log 2>&1 &
```

8. Display the app inside Colab:

```python
from google.colab import output
output.serve_kernel_port_as_window(8501)
```

The dashboard opens in a Colab-served window. The Colab runtime is temporary and may disconnect; this is for testing, not permanent public hosting. For a stable shareable website, use `DEPLOY_GUIDE.md`.
