git rm --cached # retrieve and install project in development mode
git clone https://github.com/uma-pi1/kge.git
cd kge
pip install -e .

# download and preprocess datasets
cd data
sh download_all.sh
cd ..

# train an example model on toy dataset (you can omit '--job.device cpu' when you have a gpu)
kge start examples/toy-complex-train.yaml --job.device cpu
