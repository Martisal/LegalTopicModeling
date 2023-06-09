# Legal Topic Modeling

This repository contains the code for replicating the experiments described in the paper:

> Martina Saletta, Chiara Gallese, Luca Manzoni and Alberto Bartoli. *Topic Models in Legal Texts: a Case Study on Italian Constitutional Court Judgments*. Submitted for peer review.

The dataset can be downloaded from: 
<https://gitlab.com/CIRSFID/cortecostituzionale-py>
in the directory `./data/sources/xml/all`

To run the code, first clone the repository and install the requirements:

```
git clone https://github.com/Martisal/LegalTopicModeling.git
cd LegalTopicModeling
pip3 install -r requirements.txt
```

### Preprocessing

To preprocess the dataset, run 

    python3 preprocess.py -d ./data/directory -o ./output/directory

To perform a test, just run `preprocess.py` without specifying any argument.
The script processes all the xml files in the data directory by performing all the preprocessing steps described in the paper, and saves the output in the specified directory.

### Topic modeling

To train the LDA models, modify the script `topic_modeling.py` by specifying the directory with the preprocessed data and run it.
The script trains and saves the models on the corpus from 3 to 20 topics, and also serialises and saves the corpus and the dictionary.

Other scripts:
* `coherence.py` computes and print the coherence of the saved models.
* `explore_topics.py` contains the code to compute the silhouette scores yielded by the topics on the tf-idf vectors (it is commented, since it takes some hours), and to perform the temporal analysis on shifting 5-years windows. Reaults are, by default, saved in the `./results` folder 

### Remarks

All the experiments have been performed on a Linux machine with Ubuntu 20.04 LTS. 
If you run the code on different operating systems, some requirements should be a bit different. If you are on Windows, paths must be expressed in Windows/DOS format, and backslashes sometimes need to be escaped.

### Citation

If you find this code useful for your work, please cite us:

```
@article{legaltm,
    author  =   {Martina Saletta and 
                Chiara Gallese and 
                Luca Manzoni and 
                Alberto Bartoli}, 
    title   =   {Topic Models in Legal Texts: a Case Study on Italian Constitutional Court Judgments},
    year    =   {2023}
    }  
``` 
