# Use miniconda with RDKit pre-installed
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy the whole project
COPY . /app

# Create and activate the conda environment, install dependencies
RUN conda update -n base -c defaults conda && \
    conda create -n comp_srch_env python=3.10 -y && \
    echo "conda activate comp_srch_env" >> ~/.bashrc && \
    /bin/bash -c "source ~/.bashrc && conda activate comp_srch_env && \
        conda install -c conda-forge rdkit && \
        pip install streamlit pandas==2.2.3 numpy==2.2.2 requests==2.32.3 \
        beautifulsoup4==4.13.1 openpyxl==3.1.5 xlsxwriter googletrans==4.0.0rc1"

# Expose the default Streamlit port
EXPOSE 8501

# Set the entrypoint
CMD ["/bin/bash", "-c", "source activate comp_srch_env && streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0"]
