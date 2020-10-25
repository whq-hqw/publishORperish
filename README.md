# publishORperish  
Simple python scripts to help you find information you need from Google Scholar

## Description
One common problem is when doing research is verifying your proposal has been experimented before or not. Conventionally, the pipeline would be:
1. prepare a list of papers.
2. find all the citing work from this list.
3. see if there's any paper that cited all of them.
4. Read those paper to see check if they proposed same thing as you do.  

This could be a time-consuming task. Fortunately, here's a solution that do step 1~3 automatically for you. 

We use a software called **Publish or Perish** to help you retrieve all the search results from several academic websites including **Google Scholar**, **CrossRef**, **PubMed**, etc. And this repo offer some scripts help retrieving useful information from the result you got.

## How to Use
1. Download and install **Publish or Perish** from [here](https://harzing.com/resources/publish-or-perish).
2. Install `Levenshtein`, `pandas` and `numpy` for your Python environment.
3. Follow this 3-min [tutorial](https://www.youtube.com/watch?v=c-xQ9IaF2gE)  and search for something that you are interested.
4. ***Right click*** on one of the papers in the search result and click ***Retrieve Citing Works in Publish or Perish***.
5. Have a cup of tea or coffee(sometimes you need to prove Google you are not bot)
6. Select all the citing works by ***CMD+A*** or ***CTRL+A***.
7. ***Right click*** and select ***Save Result*** and then ***Results as CSV...***
8. You can save the result under `./citation_csv` or anywhere you want, but remember to give it a discriminative name, e.g. `bert_citation.csv`.
9. Run the script below
 
Note: In the below example, we will use the CSV files under `./citation_csv`, by default, there's only 2 files: `deepsets.csv`, `pointnet.csv`. If you save your CSV file to somewhere else, you can add `--root YOUR_CSV_FOLDER` to switch the loading directory from `./citation_csv` to `YOUR_CSV_FOLDER`.
#### 1. find_common_citation.py
This script help you to extract the common citing works from multiple list of csv_files.

    python find_common_citation.py --names deepsets pointnet --leven_thres 5
    # Less strict on Levenshtein distance for paper name
    python find_common_citation.py --names deepsets pointnet --leven_thres 10

As sometimes `/`, `-`, *white space* or *case sensitive* may cause the paper's name be not exactly same, that's why I use Levenshtein distance to calculate distance of 2 paper title, if distance of 2 paper is above `--leven_thres`, they will not be considered as same paper.
In the second case, console output will be:

    Levenshtein distance: 7
    Pointcnn: Convolution on x-transformed points
    ==> PointCNN: Convolution On -Transformed Points
    ...
    Levenshtein distance: 7
    PointCNN: Convolution On -Transformed Points
    ==> Pointcnn: Convolution on x-transformed points
    
    0: Deep Neural Networks for 3D Processing and High-Dimensional Filtering
    0: Learning with Aggregate Data
    0: Meta-Learning One-Class Classification with DeepSets: Application in the Milky Way
    0: PointMixup: Augmentation for Point Clouds
    1: 3D Object Recognition with Ensemble Learning—A Study of Point Cloud-Based Deep Learning Models
    1: A Review on Deep Learning Approaches for 3D Data Representations in Retrieval and Classifications
    ...
    157: Pointwise convolutional neural networks
    185: Spidercnn: Deep learning on point sets with parameterized convolutional filters
    244: Foldingnet: Point cloud auto-encoder via deep grid deformation
    278: Splatnet: Sparse lattice networks for point cloud processing
    303: So-net: Self-organizing network for point cloud analysis
    432: Pointcnn: Convolution on x-transformed points
    Common citation between: deepsets, pointnet is 76

The former part will show you all the paper whose Levenshtein distance is not 0, the later part will show you the `Citation: Paper name`.

#### 2. rank_author.py

    # Rank author by total citations
    python rank_author.py --names deepsets --rank_by citation --topk 3
    # Rank author by total number of papers
    python rank_author.py --names deepsets --rank_by paper --topk 3
    # Rank author by position(the more first futhor, it higher score it will be)
    python rank_author.py --names deepsets --rank_by position --topk 3
    
   The output will be something like:

    python3 rank_author.py --name deepsets --rank_by position --topk 3
    -------------------------------
    | X Chen, Paper num: 5  |
    | Total Citation: 7 |
    | Author Position Rank: 9.60  |
    -------------------------------
    Particle Flow Bayes' Rule, citation: 5
    Meta Particle Flow for Sequential Bayesian Inference., citation: 1
    Ordinary differential equations for deep learning, citation: 1
      
    -------------------------------
    | J Han, Paper num: 6 |
    | Total Citation: 66  |
    | Author Position Rank: 9.33  |
    -------------------------------
    End-to-end symmetry preserving inter-atomic potential energy model for finite and extended systems, citation: 44
    Uniformly accurate machine learning-based hydrodynamic models for kinetic equations, citation: 16
    Universal approximation of symmetric and anti-symmetric functions, citation: 2
      
    -------------------------------
    | H Sun, Paper num: 5 |
    | Total Citation: 6 |
    | Author Position Rank: 9.20  |
    -------------------------------
    Learning to learn kernels with variational random features, citation: 3
    Guessing What's Plausible But Remembering What's True: Accurate Neural Reasoning for Question-Answering, citation: 1
    Learning to learn kernels with variational random features, citation: 1
