# Base image with Conda
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy your app files
COPY . /app

# Create the Conda environment and install all at once
RUN conda create -n comp_srch_env python=3.10 -y && \
    conda install -n comp_srch_env -c conda-forge rdkit -y && \
    /opt/conda/envs/comp_srch_env/bin/pip install --no-cache-dir \
        streamlit pandas==2.2.3 numpy==2.2.2 requests==2.32.3 \
        beautifulsoup4==4.13.1 openpyxl==3.1.5 xlsxwriter \
        googletrans==4.0.0rc1

# Expose Streamlit's port
EXPOSE 8501

# Run the app by explicitly using the environment's streamlit path
CMD ["/opt/conda/envs/comp_srch_env/bin/streamlit", "run", "src/app.py", "--server.port=8501", "--server.enableCORS=false"]
