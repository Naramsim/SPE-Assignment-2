# Simulation and Performance Evaluation Assignment 2

### Installing

```sh
git clone https://github.com/Naramsim/SPE-Assignment-2.git
```

### Run

#### (Python already present | Python not installed) && R installed
```sh
make
make run
make model

# To analyze data
Rscript ./analysis/analyse.r
```

#### Containerized (Docker-compose installed)
```sh
docker-compose up -d
docker exec -it ubuntu bash
make
make run
make model

# To analyze data in Rstudio
# open localhost:8787  with usr:pass rstudio:rstudio

# To analyze data with R
docker exec -it studio bash
Rscript ./analysis/analyse.r
```

