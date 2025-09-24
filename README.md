### Install Dependencies
* Package manager: UV
```{bash}
pip install uv
```
* Other Dependencies: data science libraries and langchain and langgraph.
```{bash}
uv pip install numpy pandas matplotlib seaborn
uv pip install langchain langchain_community langchain_openai langchain_experimental
uv pip install langgraph 
uv pip install langchain-google-genai
uv pip install langchain-groq
```
* Gradio for testing:
```{bash}
uv pip install gradio
```
* Backend Dependencies
```{bash}
uv pip install fastapi[all] sqlalchemy uvicorn psycopg2-binary
```
* Frontend Dependencies
Create frontend folder in the root direcotry and enter into it: `mkdir frontend`, `cd frontend` 
```{bash}
npm create vite@5.1.0 . -- --template react
```